import random

from django.db.models import Q

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
    for key, values in criteria.items():
        if key == 'is_movie':
            queryset = queryset.filter(**{key: values})
        elif key in ['year', 'imdb_rating', 'votes_count', 'duration', 'seasons_count']:
            if values[0]:
                queryset = queryset.filter(**{key + '__gte': values[0]})
            if values[1]:
                queryset = queryset.filter(**{key + '__lte': values[1]})
        else:
            queryset = queryset.filter(**{key + '__in': values})
        sum_points += priority[key]
    return queryset, sum_points


def apply_additional_filters(queryset, criteria, sum_points):
    """
    Применение к списку фильмов дополнительных фильтров
    """
    for key, values in criteria.items():
        if key in ['mood', 'viewing_method', 'viewing_time', 'visual_atmosphere', 'audience', 'intellectuality',
                   'narrative_method', 'acting', 'amount_of_dialogue', 'graphics']:
            filters = Q()
            for value in values:
                filter_q = Q(**{key: value})
                filters |= filter_q
            queryset = queryset.filter(filters)
            sum_points += priority[key]

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
    type_handlers = {
        bool: lambda value: None,
        list: lambda value: value[:-1] if value else None,
        'year': lambda value: [None if v is not None else None for v in value] if any(value) else None,
        'imdb_rating': lambda value: [None if v is not None else None for v in value] if any(value) else None,
        'votes_count': lambda value: [None if v is not None else None for v in value] if any(value) else None,
        'duration': lambda value: [None if v is not None else None for v in value] if any(value) else None,
        'seasons_count': lambda value: [None if v is not None else None for v in value] if any(value) else None,
    }

    for key, value in criteria.items():
        if isinstance(value, bool):
            del criteria[key]
        elif key in type_handlers:
            handler = type_handlers[key]
            criteria[key] = handler(value)
        elif isinstance(value, list):
            criteria[key] = value[:-1] if value else None
            if not criteria[key]:
                del criteria[key]

        return criteria


def get_titles_by_attrs(criteria):
    """
    Получение словаря с отборными фильмами
    """
    title_output = []
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

    title_output += serialized_titles_to_100

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

    title_output += serialized_titles_to_85

    return title_output
