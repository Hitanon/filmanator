from random import choice, choices
from unittest import TestCase

from django.utils import timezone

from parameterized import parameterized

from titles.models import Title
from titles.services import get_all_history_titles, remove_filter

from users.models import History
from users.models import User


class FilmSelectionUnitTests(TestCase):

    @parameterized.expand([
        ({'genre': [1, 2, 3]}, {'genre': [1, 2]}),
        ({'genre': [1, 2, 3], 'mood': [1, 2]}, {'genre': [1, 2, 3], 'mood': [1]}),
        ({'mood': [1], 'genre': [1, 2, 3]}, {'genre': [1, 2, 3]}),
        ({'year': [2000, 2015]}, {'year': [2000, None]}),
        ({'year': [2000, None]}, {}),
    ])
    def test_remove_filter(self, criteria, result):
        remove_filter(criteria)
        self.assertEqual(criteria, result)


class FilmSelectionAPITests(TestCase):
    def setUp(self):
        self._create_user()
        self._init_titles()
        self._init_history()

    def tearDown(self):
        self.user.delete()

    def _init_titles(self):
        self.titles = Title.objects.bulk_create([
              Title(
                  title=f'Title {i}',
                  year=2000 + i,
                  imdb_rating=2.0 + i,
                  votes_count=10000 * i,
                  is_movie=True,
                  duration=100 + 10 * i,
              ) for i in range(1, 6)
          ])
        self.title_id = choice(Title.objects.all()).id

    def _init_history(self):
        self.histories = History.objects.bulk_create([
            History(
                date=timezone.now(),
                user=self.user,
            ) for _ in range(1, 4)
        ])
        for history in self.histories:
            history.title.set(choices(Title.objects.all(), k=3))

    def _create_user(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='user@test.com',
            password='testpassword',
        )

    def test_get_all_history_titles(self):
        history_id = set()
        history_id = get_all_history_titles(self.histories, history_id)
        self.assertEqual(len(history_id), 9)
