import { makeAutoObservable } from "mobx";


class QuestionStore {
    constructor() {
        this.questionNumber = 1;
        this.questionText = "Фильмы какого жанра тебе нравятся больше?"
        this.answers = ['Комедии', 'Документальные', 'Ужасы', 'Исторические', 'Другое'];
        makeAutoObservable(this);
    }

    setQuestionNumber(number) {
        this.questionNumber = number;
    }

    setQuestionText(text) {
        this.questionText = text;
    }

    setAnswers(answers) {
        this.answers = answers;
    }
}

const questionStore = new QuestionStore();
export default questionStore;