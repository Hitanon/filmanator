from questionnaire.models import Result

from utils.questionnaire.config import LIMITED_CRITERIONS, UNLIMITED_CRITERIONS


class ResultCriterions:
    def __init__(self):
        self._data = {}
        self.criterions = LIMITED_CRITERIONS.copy()
        self.criterions.update(UNLIMITED_CRITERIONS)

    @property
    def data(self):
        return self._data

    def get_data(self):
        for key, value in self._data.items():
            self._data[key] = list(set(self._data[key]))
        return self._data

    def update_data(self, key, value):
        if key in self.data:
            self.data[key].append(value)
        elif type(value) == tuple:
            self.data[key] = value
        else:
            self.data[key] = [value]

    def get_limited_criterion(self, criterion):
        return criterion.more, criterion.less

    def get_unlimited_criterion(self, criterion):
        if criterion.title == 'director' or criterion.title == 'actor':
            return self.criterions[criterion.title].objects.get(name=criterion.body).id
        return self.criterions[criterion.title].objects.get(title=criterion.body).id

    def get_single_criterion(self, criterion):
        if criterion.has_limits:
            return self.get_limited_criterion(criterion)
        return self.get_unlimited_criterion(criterion)

    def add_result(self, result: Result):
        criterions = result.criterion.all()
        for criterion in criterions:
            data = self.get_single_criterion(criterion)
            self.update_data(criterion.title, data)
