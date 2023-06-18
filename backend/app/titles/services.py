import random

from config import settings

from titles.models import SimilarTitle, Title
from titles.serializers import TitleOutputSerializer


# приоритет категорий
from utils.parcing_kinopoisk import read_data_from_kinopoisk

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


def add_similar_titles(serialized_titles_to_100, filtered_titles_to_100, similar_titles):
    similar_filtered_titles = filtered_titles_to_100.filter(pk__in=[title.pk for title in similar_titles])
    if similar_filtered_titles:
        while len(serialized_titles_to_100) < 10 and similar_filtered_titles:
            random_element = random.choice(similar_filtered_titles)
            similar_filtered_titles = similar_filtered_titles.exclude(id=random_element.id)
            serializer = TitleOutputSerializer(random_element)
            serializer_data = serializer.data
            serializer_data['match_percentage'] = 100
            serialized_titles_to_100.append(serializer_data)
    return serialized_titles_to_100


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
    serialized_titles_to_100 = add_similar_titles(serialized_titles_to_100, filtered_titles_to_100, similar_titles)

    while len(serialized_titles_to_100) < 10 and filtered_titles_to_100:
        random_element = random.choice(filtered_titles_to_100)
        filtered_titles_to_100 = filtered_titles_to_100.exclude(id=random_element.id)
        serializer = TitleOutputSerializer(random_element)
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
            serializer = TitleOutputSerializer(random_element)
            serializer_data = serializer.data
            serializer_data['match_percentage'] = round(points/sum_points*100)
            serialized_titles_to_85.append(serializer_data)
        selected_titles = selected_titles.union(filtered_titles_to_85)

    title_output += serialized_titles_to_85

    return title_output


def many_trailers_to_one(film):
    """
    Сокращение кол-ва трейлеров до одного
    """
    if not film['videos'] or not film['videos']['trailers']:
        del film['videos']
        film['trailer'] = None
    else:
        film['trailer'] = film['videos']['trailers'][-1]
        del film['videos']
    return film


def check_data(film):
    """
    Проверка наличия всех полей для полной информации
    """
    needed_data = ['id', 'name', 'alternativeName', 'isSeries', 'year', 'rating', 'rating', 'votes', 'movieLength',
                   'countries', 'ageRating', 'persons', 'seasonsInfo', 'persons', 'genres', 'shortDescription',
                   'description', 'budget', 'fees', 'similarMovies', 'videos', 'poster']
    for need in needed_data:
        if need not in film or not film[need]:
            film[need] = None
    film = many_trailers_to_one(film)
    if not film['fees'] or not film['fees']['world']:
        film['fees'] = None
    if film['ageRating'] is None:
        film['ageRating'] = 0

    return film


def compare_with_ratings(ratings, similar_title):
    """
    Добавление рейтинга к похожему фильму
    """
    similar_id = similar_title['id']
    for rating in ratings:
        if rating['id'] == similar_id:
            if 'rating' in rating:
                if 'kp' in rating['rating']:
                    similar_title['rating'] = rating['rating']['kp']
                    break
                elif 'imdb' in rating['rating']:
                    similar_title['rating'] = rating['rating']['imdb']
                    break
    else:
        similar_title['rating'] = None
    return similar_title


def add_link_and_rating_to_similar(headers, data):
    """
    Добавление ссылки на фильм и рейтинга к похожим
    """
    url = 'https://api.kinopoisk.dev/v1.3/movie?selectFields=id rating.kp rating.imdb'
    base_link = 'https://www.kinopoisk.ru/film/'
    for title in data:
        title['link'] = base_link + str(title['id'])
        for similar_title in title['similarMovies']:
            url += f'&id={similar_title["id"]}'
    url += '&limit=10000'
    all_ratings = read_data_from_kinopoisk(url, headers)
    ratings = all_ratings['docs']
    for title in data:
        for similar_title in title['similarMovies']:
            similar_title = compare_with_ratings(ratings, similar_title)
    return data


def remove_key_persons(film, output_actors, output_directors):
    """
    Удаление ключа persons и добавление actors и directors
    """
    del film['persons']
    film['actors'] = output_actors
    film['directors'] = output_directors
    if not output_actors:
        film['actors'] = None
    if not output_directors:
        film['directors'] = None
    return film


def reduce_persons(film):
    """
    Сокращение кол-ва актеров до 10
    """
    output_actors = []
    output_directors = []
    for person in film['persons']:
        if person['profession'] == 'актеры':
            if len(output_actors) < 10:
                output_actors.append(person['name'])
        elif person['profession'] == 'режиссеры':
            output_directors.append(person['name'])
    film = remove_key_persons(film, output_actors, output_directors)
    return film


def add_match_percentage(data, titles):
    """
    Добавление в полную информацию процента совпадения
    """
    for i in range(len(data)):
        data[i]['match_percentage'] = titles[i]['match_percentage']
    return data


def seasons_info(film):
    """
    Изменение информации для сериалов
    """
    if film['isSeries']:
        if film['seasonsInfo']:
            seasons_count = film['seasonsInfo'][-1]['number']
            if seasons_count == 0:
                seasons_count = film['seasonsInfo'][-2]['number']
            film['seasons_count'] = seasons_count
    else:
        film['isSeries'] = False
        film['seasons_count'] = None
    del film['seasonsInfo']
    return film


def get_full_info_about_titles(titles):
    """
    Получение полной информации о фильмах
    """
    token = settings.TOKEN
    url = 'https://api.kinopoisk.dev/v1.3/movie?selectFields=id name alternativeName isSeries year rating.imdb ' \
          'rating.kp movieLength countries ageRating persons.id seasonsInfo persons.name ' \
          'persons.profession genres shortDescription description budget fees.world similarMovies.id ' \
          'similarMovies.name similarMovies.poster.previewUrl videos.trailers.url poster.previewUrl'
    for title in titles:
        url += f'&id={title["id"]}'
    headers = {'x-api-key': token}
    all_data = read_data_from_kinopoisk(url, headers)
    data = all_data['docs']
    data = add_link_and_rating_to_similar(headers, data)
    for film in data:
        film = check_data(film)
        film = reduce_persons(film)
        film = seasons_info(film)
    add_match_percentage(data, titles)
    return data


def select_titles(criteria, history):
    """
    Выборка фильмов и получение инфы о них
    """
    titles = get_titles_by_attrs(criteria, history)
    full_info = get_full_info_about_titles(titles)
    return full_info
