import { makeAutoObservable, runInAction } from "mobx";

import axios from 'axios';

import { QUESTIONNAIRE_REQUEST } from "../utils/Consts";
import { filmInfoStore } from './FilmInfoStore';



class QuestionStore {
    constructor() {
        this.isComplete = false
        this.session = null;
        this.question = null;
        this.answers = [];
        this.questionNumber = 0;
        makeAutoObservable(this);
    }

    async fetchQuestion() {
        try {
            const response = await axios.get(QUESTIONNAIRE_REQUEST);
            const data = response.data;
            runInAction(() => {
                this.session = data.session;
                this.question = data.question.body;
                this.answers = data.question.answers;
                this.questionNumber += 1;
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
                    this.question = data.question.body;
                    this.answers = data.question.answers;
                    this.questionNumber += 1;
                });
            } else if (Array.isArray(data)) {
                filmInfoStore.loadMovies(data);
                runInAction(() => {
                    this.isComplete = true;
                    this.session = null;
                    this.question = null;
                    this.answers = [];
                    this.questionNumber = 0;
                });
            } else {
                throw new Error('Invalid response data');
            }
        } catch (error) {
            console.error(error);
            // need display an error message to the user
        }
    }
    



}


const questionStore = new QuestionStore();
export default questionStore;
