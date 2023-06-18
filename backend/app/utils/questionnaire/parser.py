from questionnaire import models

from utils.questionnaire import config


class QuestionnaireParser:
    def __init__(self):
        self._clean_up()
        self.criterions = config.CRITERIONS
        self.named_attrs = config.NAMED_CRITERIONS
        self.criterion_titles = config.CRITERION_TITLES
        self.questions = config.QUESTIONS
        self.categories = config.CATEGORIES

    def _clean_up(self):
        questionnaire_models = [
            models.Criterion,
            models.Answer,
            models.Question,
            models.Category,
        ]
        for model in questionnaire_models:
            model.objects.all().delete()

    def _init_limited_criterion(self, title, model):
        entities = model.objects.all()
        for entity in entities:
            body = ''.join((str(entity.value), '+'))
            models.Criterion.objects.get_or_create(
                title=title,
                body=body,
                has_limits=True,
                more=entity.value,
                less=None,
            )

    def _init_unlimited_criterion(self, title, model, is_named=False):
        entities = model.objects.all()
        for entity in entities:
            models.Criterion.objects.get_or_create(
                title=title,
                body=entity.name if is_named else entity.title,
                has_limits=False,
                more=None,
                less=None,
            )

    def _init_criterions(self):
        for is_limited, data in self.criterions.items():
            for key, model in data.items():
                if is_limited:
                    self._init_limited_criterion(key, model)
                else:
                    is_named = key in self.named_attrs
                    self._init_unlimited_criterion(key, model, is_named)

    def _split_to_approximately_equal_parts(self, items):
        splitted_items = []
        start, step = 0, 4
        items_count = items.count()
        if items_count <= step:
            splitted_items.append(items)
            return splitted_items
        while (items_count - start) // step - 1:
            splitted_items.append(items[start:start+step])
            start += step
        if step + start == items_count:
            splitted_items.append(items[start:])
        else:
            mid = (start + items_count) // 2
            splitted_items.append(items[start:mid])
            splitted_items.append(items[mid:])
        return splitted_items

    def _init_skip_answer(self, body='Не интересует'):
        answer, _ = models.Answer.objects.get_or_create(
            body=body,
            is_skip=True,
        )
        return answer

    def _init_answers(self):
        for criterion_title in self.criterion_titles:
            criterions = models.Criterion.objects.filter(title=criterion_title)
            for criterion in criterions:
                answer, _ = models.Answer.objects.get_or_create(
                    body=criterion.body.title(),
                )
                answer.criterion.set([criterion])

    def _init_questions(self):
        for skip_answer_body, data in self.questions.items():
            skip_answer = self._init_skip_answer(body=skip_answer_body)
            for criterion_title, question_body in data.items():
                answers = models.Answer.objects.filter(criterion__title=criterion_title)
                splitted_answers = self._split_to_approximately_equal_parts(answers)
                for answers in splitted_answers:
                    question = models.Question.objects.create(
                        body=question_body,
                    )
                    answers = list(answers)
                    answers.append(skip_answer)
                    question.answer.set(answers)

    def _init_categories(self):
        for category_title, priority in self.categories.items():
            category, _ = models.Category.objects.get_or_create(
                title=category_title,
                priority=priority,
            )
            questions = models.Question.objects.filter(answer__criterion__title=category_title)
            category.question.set(questions)

    def parse(self):
        self._init_criterions()
        self._init_answers()
        self._init_questions()
        self._init_categories()
