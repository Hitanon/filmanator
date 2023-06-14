import random

from titles.models import Title
from titles.serializers import TitleSerializer


# приоритет категорий
priority = {
    'seasons_count': 5,
    'actor': 5,
    'director': 10,
    'duration': 10,
    'country': 15,
    'votes_count': 15,
    'imdb_rating': 20,
    'viewing_method': 20,
    'viewing_time': 20,
    'audience': 20,
    'narrative_method': 20,
    'acting': 20,
    'amount_of_dialogue': 20,
    'graphics': 20,
    'intellectuality': 30,
    'visual_atmosphere': 30,
    'mood': 30,
    'year': 30,
    'content_rating': 30,
    'is_movie': 40,
    'genre': 50,
}


def apply_basic_filters(queryset, criteria, sum_points):
    """
    Применение к списку фильмов базовых фильтров
    """
    if 'genre' in criteria:
        for value in criteria['genre']:
            queryset = queryset.filter(genre=value)
            sum_points += priority['genre']
    if 'director' in criteria:
        for value in criteria['director']:
            queryset = queryset.filter(director=value)
            sum_points += priority['director']
    if 'country' in criteria:
        for value in criteria['country']:
            queryset = queryset.filter(country=value)
            sum_points += priority['country']
    if 'actor' in criteria:
        for value in criteria['actor']:
            queryset = queryset.filter(actor=value)
            sum_points += priority['actor']
    if 'content_rating' in criteria:
        queryset = queryset.filter(content_rating=criteria['content_rating'])
        sum_points += priority['content_rating']
    if 'is_movie' in criteria:
        queryset = queryset.filter(is_movie=criteria['is_movie'])
        sum_points += priority['is_movie']
    if 'year' in criteria:
        if 'more' in criteria['year']:
            queryset = queryset.filter(year__gt=criteria['year']['more'])
            sum_points += priority['year']
        if 'less' in criteria['year']:
            queryset = queryset.filter(year__lt=criteria['year']['less'])
            sum_points += priority['year']
    if 'imdb_rating' in criteria:
        if 'more' in criteria['imdb_rating']:
            queryset = queryset.filter(imdb_rating__gt=criteria['imdb_rating']['more'])
            sum_points += priority['imdb_rating']
        if 'less' in criteria['imdb_rating']:
            queryset = queryset.filter(imdb_rating__lt=criteria['imdb_rating']['less'])
            sum_points += priority['imdb_rating']
    if 'votes_count' in criteria:
        if 'more' in criteria['votes_count']:
            queryset = queryset.filter(votes_count__gt=criteria['votes_count']['more'])
            sum_points += priority['votes_count']
        if 'less' in criteria['votes_count']:
            queryset = queryset.filter(votes_count__lt=criteria['votes_count']['less'])
            sum_points += priority['votes_count']
    if 'duration' in criteria:
        if 'more' in criteria['duration']:
            queryset = queryset.filter(duration__gt=criteria['duration']['more'])
            sum_points += priority['duration']
        if 'less' in criteria['duration']:
            queryset = queryset.filter(duration__lt=criteria['duration']['less'])
            sum_points += priority['duration']
    if 'seasons_count' in criteria:
        if 'more' in criteria['seasons_count']:
            queryset = queryset.filter(seasons_count__gt=criteria['seasons_count']['more'])
            sum_points += priority['seasons_count']
        if 'less' in criteria['seasons_count']:
            queryset = queryset.filter(seasons_count__lt=criteria['seasons_count']['less'])
            sum_points += priority['seasons_count']

    return queryset, sum_points


def apply_additional_filters(queryset, criteria, sum_points):
    """
    Применение к списку фильмов дополнительных фильтров
    """
    if 'mood' in criteria:
        for value in criteria['mood']:
            queryset = queryset.filter(mood=value)
            sum_points += priority['mood']
    if 'viewing_method' in criteria:
        for value in criteria['viewing_method']:
            queryset = queryset.filter(viewing_method=value)
            sum_points += priority['viewing_method']
    if 'viewing_time' in criteria:
        for value in criteria['viewing_time']:
            queryset = queryset.filter(viewing_time=value)
            sum_points += priority['viewing_time']
    if 'visual_atmosphere' in criteria:
        for value in criteria['visual_atmosphere']:
            queryset = queryset.filter(visual_atmosphere=value)
            sum_points += priority['visual_atmosphere']
    if 'audience' in criteria:
        for value in criteria['audience']:
            queryset = queryset.filter(audience=value)
            sum_points += priority['audience']
    if 'intellectuality' in criteria:
        for value in criteria['intellectuality']:
            queryset = queryset.filter(intellectuality=value)
            sum_points += priority['intellectuality']
    if 'narrative_method' in criteria:
        for value in criteria['narrative_method']:
            queryset = queryset.filter(narrative_method=value)
            sum_points += priority['narrative_method']
    if 'acting' in criteria:
        for value in criteria['acting']:
            queryset = queryset.filter(acting=value)
            sum_points += priority['acting']
    if 'amount_of_dialogue' in criteria:
        for value in criteria['amount_of_dialogue']:
            queryset = queryset.filter(amount_of_dialogue=value)
            sum_points += priority['amount_of_dialogue']
    if 'graphics' in criteria:
        for value in criteria['graphics']:
            queryset = queryset.filter(graphics=value)
            sum_points += priority['graphics']

    return queryset, sum_points


def apply_filters(queryset, criteria, sum_points=0):
    """
    Применение к списку фильмов базовых и дополнительных фильтров
    """
    queryset, sum_points = apply_basic_filters(queryset, criteria, sum_points)
    queryset, sum_points = apply_additional_filters(queryset, criteria, sum_points)

    return queryset, sum_points


def remove_filter(criteria):
    """
    Удаление одного фильтра с наименьшим приоритетом
    """
    for key in priority.keys():
        if key in criteria.keys():
            if type(criteria[key]) == bool:
                del criteria[key]
            elif 'more' in criteria[key]:
                del criteria[key]['more']
            elif 'less' in criteria[key]:
                del criteria[key]['less']
            elif type(criteria[key]) == list:
                criteria[key].pop()
                if not criteria[key]:
                    del criteria[key]
            else:
                del criteria[key]
            return criteria


def get_titles_by_attrs(criteria):
    """
    Получение словаря с отборными фильмами
    """
    title_output = {'100': {'length': 0, 'data': []}, '85': {'length': 0, 'data': []}}
    titles = Title.objects.all()
    sum_points = 0
    # отборка для 100% совпадения
    filtered_titles_to_100, sum_points = apply_filters(titles, criteria, sum_points)
    selected_titles = filtered_titles_to_100
    serialized_titles_to_100 = []
    while len(serialized_titles_to_100) < 10 and filtered_titles_to_100:
        random_element = random.choice(filtered_titles_to_100)
        filtered_titles_to_100 = filtered_titles_to_100.exclude(id=random_element.id)
        serializer = TitleSerializer(random_element)
        serializer_data = serializer.data
        serializer_data['match_percentage'] = 100
        serialized_titles_to_100.append(serializer_data)
    length_to_100 = len(serialized_titles_to_100)

    title_output['100']['length'] = length_to_100
    title_output['100']['data'] = serialized_titles_to_100

    # отборка для меньшего совпадения
    serialized_titles_to_85 = []

    while length_to_100 + len(serialized_titles_to_85) < 10:
        criteria = remove_filter(criteria)
        points = 0

        filtered_titles_to_85, points = apply_filters(titles, criteria, points)
        filtered_titles_to_85 = filtered_titles_to_85.exclude(pk__in=[title.pk for title in selected_titles])
        while len(serialized_titles_to_85) < 10-length_to_100 and filtered_titles_to_85:
            random_element = random.choice(filtered_titles_to_85)
            filtered_titles_to_85 = filtered_titles_to_85.exclude(id=random_element.id)
            serializer = TitleSerializer(random_element)
            serializer_data = serializer.data
            serializer_data['match_percentage'] = round(points/sum_points*100)
            serialized_titles_to_85.append(serializer_data)
        selected_titles = selected_titles.union(filtered_titles_to_85)

    title_output['85']['length'] = len(serialized_titles_to_85)
    title_output['85']['data'] = serialized_titles_to_85

    return title_output
