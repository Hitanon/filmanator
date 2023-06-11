
import { makeAutoObservable } from "mobx";


class QuestionStore {
    questionNumber = 1;
    questionText = "Фильмы какого жанра тебе нравятся больше?"
    answers = ['Комедии', 'Документальные', 'Ужасы', 'Исторические', 'Другое'];

    constructor() {
        makeAutoObservable(this);
    }

    setQuestionNumber(number) {
        this.questionNumber = number;
    }

    setQuestionText(text) {
        this.questionText = text;
    }

    setAnswers (answers) {
        this.answers = answers;
    }
}

const questionStore = new QuestionStore();
export default questionStore;