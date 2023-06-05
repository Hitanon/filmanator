import time

from config import settings

from django.core.exceptions import ObjectDoesNotExist

import requests

from titles.models import Actor, ContentRating, Country, Director, Genre, SimilarTitle, Title


def read_data_from_kinopoisk(url: str, headers: dict) -> dict:
    """
    Чтение данных с api кинопоиска
    :param url: адрес для нужного запроса к api
    :param headers: заголовок запроса с указанием токена
    :return: data - словарь со списком фильмов
    """
    response = requests.get(url, headers=headers)
    data = response.json()
    return data


def check_params(data: dict) -> bool:
    """
    Проверка значений необходимых полей для БД
    :param data: словарь с одним фильмом
    :return: bool
    """
    if 'id' in data:
        if data['name'] and data['genres'] and data['year'] and data['rating'] and data['votes'] and \
                data['countries'] and data['persons']:
            return True
    return False


def check_duration(data: dict) -> bool:
    """
    Проверка того что фильм имеет продолжительность
    :param data: словарь с одним фильмом
    :return: bool
    """
    if not data['isSeries'] and not data['movieLength']:
        return False
    return True


def check_seasons(data: dict) -> bool:
    """
    Проверка того что сериал имеет сезоны
    :param data: словарь с одним фильмом
    :return: bool
    """
    if data['isSeries'] and not data['seasonsInfo']:
        return False
    return True


def add_title(data: dict) -> None:
    """
    Добавление фильма или сериала в БД
    :param data: словарь с одним экземпляром
    :return:
    """
    if data['isSeries']:
        seasons_count = data['seasonsInfo'][-1]['number']

        title, _ = Title.objects.get_or_create(
            id=data['id'],
            title=data['name'],
            year=data['year'],
            imdb_rating=data['rating']['imdb'],
            votes_count=data['votes']['imdb'],
            is_movie=False,
            seasons_count=seasons_count,
        )
    else:
        title, _ = Title.objects.get_or_create(
            id=data['id'],
            title=data['name'],
            year=data['year'],
            imdb_rating=data['rating']['imdb'],
            votes_count=data['votes']['imdb'],
            is_movie=True,
            duration=data['movieLength'],
        )


def add_title_genres(data):
    """
    Добавление жанров и их связей с фильмом в БД
    :param data: словарь с одним экземпляром
    :return:
    """
    title = Title.objects.get(id=data['id'])
    for genre in data['genres']:
        genre, _ = Genre.objects.get_or_create(title=genre['name'])

        genre.titles.add(title)


def add_title_directors(data):
    """
    Добавление режиссеров и их связей с фильмом в БД
    :param data: словарь с одним экземпляром
    :return:
    """
    title = Title.objects.get(id=data['id'])
    for director in data['persons']:
        if director['profession'] == 'режиссеры' and director['name']:
            try:
                director = Director.objects.get(id=director['id'])
            except ObjectDoesNotExist:
                director, _ = Director.objects.get_or_create(id=director['id'], name=director['name'])

            director.titles.add(title)


def add_title_countries(data):
    """
    Добавление стран и их связей с фильмом в БД
    :param data: словарь с одним экземпляром
    :return:
    """
    title = Title.objects.get(id=data['id'])
    for country in data['countries']:
        country, _ = Country.objects.get_or_create(title=country['name'])

        country.titles.add(title)


def add_title_actors(data):
    """
    Добавление актера и их связей с фильмом в БД
    :param data: словарь с одним экземпляром
    :return:
    """
    title = Title.objects.get(id=data['id'])
    cnt = 0
    for actor in data['persons']:
        if actor['profession'] == 'актеры' and actor['name']:
            if cnt == 3:
                break
            try:
                actor = Actor.objects.get(id=actor['id'])
            except ObjectDoesNotExist:
                actor, _ = Actor.objects.get_or_create(id=actor['id'], name=actor['name'])

            actor.titles.add(title)
            cnt += 1


def add_title_content_rating(data):
    """
    Добавление возрастного ограничения и его связи с фильмом в БД
    :param data: словарь с одним экземпляром
    :return:
    """
    title = Title.objects.get(id=data['id'])
    if data['ageRating']:
        age_rating, _ = ContentRating.objects.get_or_create(
            value=data['ageRating'],
        )
        age_rating.titles.add(title)


def add_similar_titles(data):
    """
    Добавление похожих фильмов и их связей с фильмом в БД
    :param data: словарь с одним экземпляром
    :return:
    """
    title = Title.objects.get(id=data['id'])
    for title in data['simularTitles']:
        try:
            Title.objects.get(id=title['id'])

            SimilarTitle.objects.update_or_create(
                title_id=data['id'],
                simular_title_id=title['id'],
            )
        except ObjectDoesNotExist:
            SimilarTitle.objects.update_or_create(
                title_id=data['id'],
                simular_title_id=None,
            )


def add_film_to_database(data):
    """
    Добавление фильма в БД
    :param data: словарь с одним экземпляром
    :return:
    """
    add_title(data)
    add_title_genres(data)
    add_title_countries(data)
    add_title_actors(data)
    add_title_directors(data)
    add_title_content_rating(data)
    # add_similar_titles(data)

    print(f"Фильм {data['name']} - успешно добавлен!")


def add_film(film, cnt):
    """
    Добавление фильма в БД
    :param film: словарь с одним экземпляром
    :param cnt: порядковый номер загружаемого фильма
    :return:
    """
    if check_params(film) and check_duration(film) and check_seasons(film):
        try:
            title = Title.objects.get(id=film['id'])
            print(f'[INFO] Фильм {title.title} - уже существует!')
        except ObjectDoesNotExist:
            print(f'[{cnt}] ', sep='', end='')
            add_film_to_database(film)
    else:
        if 'name' in film:
            film_name = film['name']
            print(f'[ERROR] Недостаточно данных для добавления фильма {film_name}!')
        else:
            print('[ERROR] Недостаточно данных для добавления фильма None!')


def main():
    """
    Получение списка фильмов через api кинопоиска и их добавление в БД
    :param:
    :return:
    """
    cnt = 1
    start_page = settings.START_PAGE
    end_page = settings.END_PAGE
    limit = settings.LIMIT
    token = settings.TOKEN

    for page in range(start_page, end_page + 1):
        url = 'https://api.kinopoisk.dev/v1.3/movie?selectFields=id name similarMovies.id isSeries ' \
              'year rating.imdb votes.imdb movieLength countries ageRating director persons.id seasonsInfo ' \
              f'persons.name persons.profession genres&sortField=id&sortType=1&limit={limit}&page={page}'

        headers = {'x-api-key': token}

        data = read_data_from_kinopoisk(url, headers)
        for film in data['docs']:
            add_film(film, cnt)
            cnt += 1


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time() - start
    print(f'\nВремя выполнения программы - {round(end, 2)} сек')
