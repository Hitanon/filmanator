import random

from titles.models import Title, SimilarTitle
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


def apply_content_rating(queryset, values):
    """
    Применение фильтра к возрастному ограничению
    """
    id_content_rating = {16: 1, 18: 2, 12: 3, 6: 4}
    all_list = [6, 12, 16, 18]

    if values[0] in all_list:
        all_list = all_list[all_list.index(values[0]):]

    if values[1] in all_list:
        all_list = all_list[:all_list.index(values[1]) + 1]

    id_list = []
    for item in all_list:
        id_list.append(id_content_rating[item])
    id_list.append(None)
    queryset = queryset.filter(content_rating__in=id_list)

    return queryset


def apply_range_filters(queryset, values, key):
    """
    Применение фильтров к критериям с диапазоном значений
    """
    if values[0]:
        queryset = queryset.filter(**{key + '__gte': values[0]})
    if values[1]:
        queryset = queryset.filter(**{key + '__lte': values[1]})
    return queryset


def apply_basic_filters(queryset, criteria, sum_points):
    """
    Применение к списку фильмов базовых фильтров
    """
    for key, values in criteria.items():
        if key == 'is_movie':
            queryset = queryset.filter(**{key: values})
        elif key == 'content_rating':
            queryset = apply_content_rating(queryset, values)
        elif key in ['year', 'imdb_rating', 'votes_count', 'duration', 'seasons_count']:
            queryset = apply_range_filters(queryset, values, key)
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
            queryset = queryset.filter(**{key + '__in': values})
            sum_points += priority[key]

    return queryset, sum_points


def apply_filters(queryset, criteria, sum_points):
    """
    Применение к списку фильмов базовых и дополнительных фильтров
    """
    queryset, sum_points = apply_basic_filters(queryset, criteria, sum_points)
    queryset, sum_points = apply_additional_filters(queryset, criteria, sum_points)

    return queryset, sum_points


def remove_two_values(criteria, key, value):
    """
    Удаление одного значения из двух
    """
    if value[1]:
        criteria[key] = [value[0], None]
    else:
        del criteria[key]
    return criteria


def remove_list_values(criteria, key, value):
    """
    Удаление одного значения из списка
    """
    criteria[key] = value[:-1] if value else None
    if not criteria[key]:
        del criteria[key]
    return criteria


def remove_filter(criteria):
    """
    Удаление одного фильтра с наименьшим приоритетом
    """
    criteries = ['year', 'imdb_rating', 'votes_count', 'duration', 'seasons_count', 'content_rating']
    for category in priority.keys():
        if category in criteria:
            key, value = category, criteria[category]
            if isinstance(value, bool):
                del criteria[key]
            elif key in criteries:
                criteria = remove_two_values(criteria, key, value)
            elif isinstance(value, list):
                criteria = remove_list_values(criteria, key, value)
            return criteria


def get_titles_by_attrs(criteria, history):
    """
    Получение словаря с отборными фильмами
    """
    title_output = []
    titles = Title.objects.all()
    sum_points = 0
    # похожие фильмы на уже просмотренные
    similar_similar_titles = SimilarTitle.objects.none()
    for title in history:
        similar_similar_titles = similar_similar_titles.union(title.similar_titles.all())
    similar_titles = Title.objects.all()
    print(similar_similar_titles)
    similar_titles = similar_titles.filter(pk__in=[title.title.pk for title in similar_similar_titles])

    # отборка для 100% совпадения
    filtered_titles_to_100, sum_points = apply_filters(titles, criteria, sum_points)
    # исключаем все ранее просмотренные фильмы
    filtered_titles_to_100 = filtered_titles_to_100.exclude(pk__in=[title.pk for title in history])
    selected_titles = filtered_titles_to_100
    selected_titles = selected_titles.union(history)
    serialized_titles_to_100 = []
    # добавление похожих фильмов
    print(filtered_titles_to_100)
    print(similar_titles)
    similar_filtered_titles = filtered_titles_to_100.filter(pk__in=[title.pk for title in similar_titles])
    if similar_filtered_titles:
        while len(serialized_titles_to_100) < 10 and similar_filtered_titles:
            random_element = random.choice(similar_filtered_titles)
            similar_filtered_titles = similar_filtered_titles.exclude(id=random_element.id)
            serializer = TitleSerializer(random_element)
            serializer_data = serializer.data
            serializer_data['match_percentage'] = 100
            serialized_titles_to_100.append(serializer_data)

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
