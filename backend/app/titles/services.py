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
        result_queryset = queryset
        for value in criteria['genre']:
            queryset = queryset.filter(genre=value)
            result_queryset.union(queryset)
            sum_points += priority['genre']
        queryset = result_queryset
    if 'director' in criteria:
        result_queryset = queryset
        for value in criteria['director']:
            queryset = queryset.filter(director=value)
            result_queryset.union(queryset)
            sum_points += priority['director']
        queryset = result_queryset
    if 'country' in criteria:
        result_queryset = queryset
        for value in criteria['country']:
            queryset = queryset.filter(country=value)
            result_queryset.union(queryset)
            sum_points += priority['country']
        queryset = result_queryset
    if 'actor' in criteria:
        result_queryset = queryset
        for value in criteria['actor']:
            queryset = queryset.filter(actor=value)
            result_queryset.union(queryset)
            sum_points += priority['actor']
        queryset = result_queryset
    if 'content_rating' in criteria:
        result_queryset = queryset
        for value in criteria['content_rating']:
            queryset = queryset.filter(content_rating=value)
            result_queryset.union(queryset)
            sum_points += priority['content_rating']
        queryset = result_queryset
        queryset = queryset.filter()
        sum_points += priority['content_rating']
    if 'is_movie' in criteria:
        queryset = queryset.filter(is_movie=criteria['is_movie'])
        sum_points += priority['is_movie']
    if 'year' in criteria:
        if criteria['year'][0]:
            queryset = queryset.filter(year__gt=criteria['year'][0])
            sum_points += priority['year']
        if criteria['year'][1]:
            queryset = queryset.filter(year__lt=criteria['year'][1])
            sum_points += priority['year']
    if 'imdb_rating' in criteria:
        if criteria['imdb_rating'][0]:
            queryset = queryset.filter(imdb_rating__gt=criteria['imdb_rating'][0])
            sum_points += priority['imdb_rating']
        if criteria['imdb_rating'][1]:
            queryset = queryset.filter(imdb_rating__lt=criteria['imdb_rating'][1])
            sum_points += priority['imdb_rating']
    if 'votes_count' in criteria:
        if criteria['votes_count'][0]:
            queryset = queryset.filter(votes_count__gt=criteria['votes_count'][0])
            sum_points += priority['votes_count']
        if criteria['votes_count'][1]:
            queryset = queryset.filter(votes_count__lt=criteria['votes_count'][1])
            sum_points += priority['votes_count']
    if 'duration' in criteria:
        if criteria['duration'][0]:
            queryset = queryset.filter(duration__gt=criteria['duration'][0])
            sum_points += priority['duration']
        if criteria['duration'][1]:
            queryset = queryset.filter(duration__lt=criteria['duration'][1])
            sum_points += priority['duration']
    if 'seasons_count' in criteria:
        if criteria['seasons_count'][0]:
            queryset = queryset.filter(seasons_count__gt=criteria['seasons_count'][0])
            sum_points += priority['seasons_count']
        if criteria['seasons_count'][1]:
            queryset = queryset.filter(seasons_count__lt=criteria['seasons_count'][1])
            sum_points += priority['seasons_count']

    return queryset, sum_points


def apply_additional_filters(queryset, criteria, sum_points):
    """
    Применение к списку фильмов дополнительных фильтров
    """
    if 'mood' in criteria:
        result_queryset = queryset
        for value in criteria['mood']:
            queryset = queryset.filter(mood=value)
            result_queryset.union(queryset)
            sum_points += priority['mood']
        queryset = result_queryset
    if 'viewing_method' in criteria:
        result_queryset = queryset
        for value in criteria['viewing_method']:
            queryset = queryset.filter(viewing_method=value)
            result_queryset.union(queryset)
            sum_points += priority['viewing_method']
        queryset = result_queryset
    if 'viewing_time' in criteria:
        result_queryset = queryset
        for value in criteria['viewing_time']:
            queryset = queryset.filter(viewing_time=value)
            result_queryset.union(queryset)
            sum_points += priority['viewing_time']
        queryset = result_queryset
    if 'visual_atmosphere' in criteria:
        result_queryset = queryset
        for value in criteria['visual_atmosphere']:
            queryset = queryset.filter(visual_atmosphere=value)
            result_queryset.union(queryset)
            sum_points += priority['visual_atmosphere']
        queryset = result_queryset
    if 'audience' in criteria:
        result_queryset = queryset
        for value in criteria['audience']:
            queryset = queryset.filter(audience=value)
            result_queryset.union(queryset)
            sum_points += priority['audience']
        queryset = result_queryset
    if 'intellectuality' in criteria:
        result_queryset = queryset
        for value in criteria['intellectuality']:
            queryset = queryset.filter(intellectuality=value)
            result_queryset.union(queryset)
            sum_points += priority['intellectuality']
        queryset = result_queryset
    if 'narrative_method' in criteria:
        result_queryset = queryset
        for value in criteria['narrative_method']:
            queryset = queryset.filter(narrative_method=value)
            result_queryset.union(queryset)
            sum_points += priority['narrative_method']
        queryset = result_queryset
    if 'acting' in criteria:
        result_queryset = queryset
        for value in criteria['acting']:
            queryset = queryset.filter(acting=value)
            result_queryset.union(queryset)
            sum_points += priority['acting']
        queryset = result_queryset
    if 'amount_of_dialogue' in criteria:
        result_queryset = queryset
        for value in criteria['amount_of_dialogue']:
            queryset = queryset.filter(amount_of_dialogue=value)
            result_queryset.union(queryset)
            sum_points += priority['amount_of_dialogue']
        queryset = result_queryset
    if 'graphics' in criteria:
        result_queryset = queryset
        for value in criteria['graphics']:
            queryset = queryset.filter(graphics=value)
            result_queryset.union(queryset)
            sum_points += priority['graphics']
        queryset = result_queryset

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
            elif key in ['year', 'imdb_rating', 'votes_count', 'duration', 'seasons_count']:
                if criteria[key][1]:
                    criteria[key][1] = None
                elif criteria[key][0]:
                    criteria[key][0] = None
                if not criteria[key][0] and not criteria[key][1]:
                    del criteria[key]
            elif type(criteria[key]) == list:
                criteria[key].pop()
                if not criteria[key]:
                    del criteria[key]
            return criteria


def get_titles_by_attrs(criteria):
    """
    Получение словаря с отборными фильмами
    """
    title_output = [{'match_percentage': 85, 'length': 0, 'titles': []}, {'match_percentage': 100, 'length': 0, 'titles': []}]
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

    title_output[1]['length'] = length_to_100
    title_output[1]['titles'] = serialized_titles_to_100

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

    title_output[0]['length'] = len(serialized_titles_to_85)
    title_output[0]['titles'] = serialized_titles_to_85

    return title_output
