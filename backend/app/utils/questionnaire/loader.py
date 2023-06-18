import json

from config.settings import QUESTIONNAIRE_FILE_PATH

from questionnaire import models


class QuestionnaireLoader:
    def _read_json_data(self):
        with open(QUESTIONNAIRE_FILE_PATH, 'r') as file:
            return json.loads(file.read())

    def _create_criterion(self, **data):
        return models.Criterion.objects.create(**data)

    def _create_answer(self, **data):
        del data['criterions']
        answer, _ = models.Answer.objects.get_or_create(**data)
        return answer

    def _create_question(self, **data):
        del data['answers']
        question, _ = models.Question.objects.get_or_create(**data)
        return question

    def _create_category(self, **data):
        del data['questions']
        category, _ = models.Category.objects.get_or_create(**data)
        return category

    def load(self):
        for data in self._read_json_data():
            current_questions = []
            for question in data['questions']:
                current_answers = []
                for answer in question['answers']:
                    current_criterions = []
                    for criterion in answer['criterions']:
                        current_criterions.append(self._create_criterion(**criterion))
                    answer = self._create_answer(**answer)
                    answer.criterion.set(current_criterions)
                    current_answers.append(answer)
                    current_answers.append(answer)
                current_question = self._create_question(**question)
                current_question.answer.set(current_answers)
                current_questions.append(current_question)
            category = self._create_category(**data)
            category.question.set(current_questions)
