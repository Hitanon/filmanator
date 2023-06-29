from questionnaire.models import Result

from utils.questionnaire.config import LIMITED_CRITERIONS, UNLIMITED_CRITERIONS


class ResultCriterions:
    def __init__(self):
        self._data = {}
        self.criterions = LIMITED_CRITERIONS.copy()
        self.criterions.update(UNLIMITED_CRITERIONS)

    # Trash property
    @property
    def data(self):
        return self._data

    def get_limited_criterion(self, criterion):
        return criterion.more, criterion.less

    def get_unlimited_criterion(self, criterion):
        return [self.criterions[criterion.title].objects.get(title=criterion.body).id]

    def get_single_criterion(self, criterion):
        if criterion.has_limits:
            return self.get_limited_criterion(criterion)
        return self.get_unlimited_criterion(criterion)

    def add_result(self, result: Result):
        key = result.category.title
        criterions = result.criterion.all()
        if criterions.count() == 1:
            value = self.get_single_criterion(criterions[0])
        else:
            value = [self.criterions[criterion.title].objects.get(title=criterion.body).id for criterion in criterions]
        self.data[key] = value
