from questionnaire.models import Result

from titles import models as t_models


class ResultCriterions:
    def __init__(self):
        self._data = {}
        self.criterions = {
          'content_rating': t_models.ContentRating,
          'acting': t_models.Acting,
          # 'actor': models.Actor,
          'amount_of_dialogue': t_models.AmountOfDialogue,
          'audience': t_models.Audience,
          # 'country': t_models.Country,
          # 'director': models.Director,
          'genre': t_models.Genre,
          'graphics': t_models.Graphics,
          'intellectuality': t_models.Intellectuality,
          'mood': t_models.Mood,
          'narrative_method': t_models.NarrativeMethod,
          'viewing_method': t_models.ViewingMethod,
          'viewing_time': t_models.ViewingTime,
          'visual_atmosphere': t_models.VisualAtmosphere,
        }

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
