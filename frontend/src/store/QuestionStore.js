import { makeAutoObservable, runInAction } from "mobx";

import axios from 'axios';

import { QUESTIONNAIRE_REQUEST } from "../utils/Consts";
import { filmInfoStore } from './FilmInfoStore';



class QuestionStore {
    constructor() {
        this.isComplete = false;
        this.session = null;
        this.question = null;
        this.answers = [];
        this.questionNumber = 0;
        makeAutoObservable(this);
    }

    async fetchQuestion() {
        this.reset();
        try {
            const response = await axios.get(QUESTIONNAIRE_REQUEST);
            const data = response.data;
            runInAction(() => {
                this.session = data.session;
                this.updateQuestion(data.question.body, data.question.answers)
            });
        } catch (error) {
            console.error(error);
            // need display an error message to the user
        }
    }

    async submitAnswer(answerId) {
        try {
            const requestData = {
                session: [this.session],
                answer: [answerId],
            };
            const response = await axios.post(QUESTIONNAIRE_REQUEST, requestData);
            const data = response.data;
            if (data.question) {
                runInAction(() => {
                    this.updateQuestion(data.question.body, data.question.answers)
                });
            } else if (Array.isArray(data)) {
                console.log(data);
                filmInfoStore.clearLocalStorage();
                filmInfoStore.loadMovies(data);
                runInAction(() => {
                    this.isComplete = true;
                });
            } else {
                throw new Error('Invalid response data');
            }
        } catch (error) {
            console.error(error);
            // need display an error message to the user
        }
    }

    updateQuestion(question, answers) {
        this.question = question;
        this.answers = answers;
        this.questionNumber += 1;
    }

    reset() {
        runInAction(() => {
            this.session = null;
            this.question = null;
            this.answers = [];
            this.questionNumber = 0;
            this.isComplete = false;
        });
    }




}


const questionStore = new QuestionStore();
export default questionStore;
