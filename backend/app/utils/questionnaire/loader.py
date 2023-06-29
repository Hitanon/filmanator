import json
from os import listdir
from pathlib import Path

from config.settings import QUESTIONNAIRE_FILE_PATH

from questionnaire import models

from utils.questionnaire.config import DEFAULT_CUSTOM_QUESTION_PRIORITY


class QuestionnaireLoader:
    def _read_json_data(self, file_name):
        if not QUESTIONNAIRE_FILE_PATH:
            return []
        with open(Path(QUESTIONNAIRE_FILE_PATH, file_name), 'r') as file:
            return json.loads(file.read())

    def _create_criterion(self, **data):
        criterion, _ = models.Criterion.objects.get_or_create(**data)
        return criterion

    def _create_answer(self, **data):
        del data['criterions']
        answer, _ = models.Answer.objects.get_or_create(**data)
        answer.criterion.set(self.current_criterions)
        return answer

    def _create_question(self, **data):
        del data['answers']
        data.setdefault('priority', DEFAULT_CUSTOM_QUESTION_PRIORITY)
        question, _ = models.Question.objects.get_or_create(**data)
        question.answer.set(self.current_answers)
        return question

    def _create_category(self, **data):
        del data['questions']
        category, _ = models.Category.objects.get_or_create(**data)
        category.question.set(self.current_questions)
        return category

    def load(self):
        for file_name in listdir(QUESTIONNAIRE_FILE_PATH):
            for data in self._read_json_data(file_name):
                self.current_questions = []
                for question in data['questions']:
                    self.current_answers = []
                    for answer in question['answers']:
                        self.current_criterions = []
                        for criterion in answer['criterions']:
                            self.current_criterions.append(self._create_criterion(**criterion))
                        self.current_answers.append(self._create_answer(**answer))
                    self.current_questions.append(self._create_question(**question))
                self._create_category(**data)
