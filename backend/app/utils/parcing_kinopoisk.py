import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.app.config.settings")
django.setup()

import environ
import requests
from titles.models import *
import time

env = environ.Env(
    TOKEN=(str, 'TOKEN'),
    START_PAGE=(int, 1),
    END_PAGE=(int, 10),
    LIMIT=(int, 1000)
)


def read_data_from_kinopoisk(url: str, headers: dict) -> dict:
    """
    Чтение данных с api кинопоиска
    :param url: адрес для нужного запроса к api
    :param headers: заголовок запроса с указанием токена
    :return data: словарь со списком фильмов
    """
    response = requests.get(url, headers=headers)
    data = response.json()
    return data


def check_params(data: dict) -> bool:
    """
    Проверка значений необходимых полей для БД
    :param data: словарь с одним фильмом
    :return bool:
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
    :return bool:
    """
    if not data['isSeries'] and not data['movieLength']:
        return False
    return True


def check_seasons(data: dict) -> bool:
    """
    Проверка того что сериал имеет сезоны
    :param data: словарь с одним фильмом
    :return bool:
    """
    if data['isSeries'] and not data['seasonsInfo']:
        return False
    return True


def add_title(data):
    if data['isSeries']:
        seasons_count = data['seasonsInfo'][-1]['number']

        title, _ = Title.objects.get_or_create(
            id=data['id'],
            title=data['name'],
            year=data['year'],
            imdb_rating=data['rating']['imdb'],
            votes_count=data['votes']['imdb'],
            is_movie=False,
            seasons_count=seasons_count
        )
    else:
        title, _ = Title.objects.get_or_create(
            id=data['id'],
            title=data['name'],
            year=data['year'],
            imdb_rating=data['rating']['imdb'],
            votes_count=data['votes']['imdb'],
            is_movie=True,
            duration=data['movieLength']
        )


def add_title_genres(data):
    title = Title.objects.get(id=data['id'])
    for genre in data['genres']:
        genre, _ = Genre.objects.get_or_create(title=genre['name'])

        genre.titles.add(title)


def add_title_directors(data):
    title = Title.objects.get(id=data['id'])
    for director in data['persons']:
        if director['profession'] == 'режиссеры' and director['name']:
            try:
                director = Director.objects.get(id=director['id'])
            except:
                director, _ = Director.objects.get_or_create(id=director['id'], name=director['name'])

            director.titles.add(title)


def add_title_countries(data):
    title = Title.objects.get(id=data['id'])
    for country in data['countries']:
        country, _ = Country.objects.get_or_create(title=country['name'])

        country.titles.add(title)


def add_title_actors(data):
    title = Title.objects.get(id=data['id'])
    cnt = 0
    for actor in data['persons']:
        if actor['profession'] == 'актеры' and actor['name']:
            if cnt == 3:
                break
            try:
                actor = Actor.objects.get(id=actor['id'])
            except:
                actor, _ = Actor.objects.get_or_create(id=actor['id'], name=actor['name'])

            actor.titles.add(title)
            cnt += 1


def add_title_content_rating(data):
    title = Title.objects.get(id=data['id'])
    if data['ageRating']:
        age_rating, _ = ContentRating.objects.get_or_create(
            value=data['ageRating']
        )
        age_rating.titles.add(title)


def add_similar_titles(data):
    title = Title.objects.get(id=data['id'])
    for title in data['simularTitles']:
        try:
            Title.objects.get(id=title['id'])

            SimilarTitle.objects.update_or_create(
                title_id=data['id'],
                simular_title_id=title['id']
            )
        except:
            SimilarTitle.objects.update_or_create(
                title_id=data['id'],
                simular_title_id=None
            )


def add_film(data):
    add_title(data)
    add_title_genres(data)
    add_title_countries(data)
    add_title_actors(data)
    add_title_directors(data)
    add_title_content_rating(data)
    # add_similar_titles(data)

    print(f"Фильм {data['name']} - успешно добавлен!")


def main():
    cnt = 1

    for page in range(env('START_PAGE'), env('END_PAGE') + 1):
        url = 'https://api.kinopoisk.dev/v1.3/movie?selectFields=id name similarMovies.id isSeries ' \
              'year rating.imdb votes.imdb movieLength countries ageRating director persons.id seasonsInfo ' \
              f'persons.name persons.profession genres&sortField=id&sortType=1&limit={env("LIMIT")}&page={page}'

        headers = {'x-api-key': env('TOKEN')}

        data = read_data_from_kinopoisk(url, headers)
        for film in data['docs']:
            if check_params(film) and check_duration(film) and check_seasons(film):
                try:
                    Title.objects.get(id=film['id'])
                    print(f"[INFO] Фильм {film['name']} - уже существует!")
                except:
                    print(f"[{cnt}] ", sep='', end='')
                    add_film(film)
            else:
                if 'name' in film:
                    print(f"[ERROR] Недостаточно данных для добавления фильма {film['name']}!")
                else:
                    print("[ERROR] Недостаточно данных для добавления фильма None!")
            cnt += 1


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time() - start
    print(f'\nВремя выполнения программы - {round(end, 2)} сек')
