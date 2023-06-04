import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.app.config.settings")
django.setup()

import environ
import requests
from backend.app.titles.models import *

env = environ.Env(
    TOKEN=(str, 'TOKEN'),
    START_PAGE=(int, 1),
    END_PAGE=(int, 5),
    LIMIT=(int, 10)
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
        if data['name'] and data['genres'] and data['year'] and data['rating'] and data['votes'] and data['type'] and \
                data['movieLength'] and data['countries'] and data['ageRating'] and data['persons']:
            return True
    return False


def add_title(data):
    is_movie = False
    if data['type'] == 'movie':
        is_movie = True

    title, _ = Title.objects.get_or_create(
        id=data['id'],
        title=data['name'],
        year=data['year'],
        imdb_rating=data['rating']['imdb'],
        votes_count=data['votes']['imdb'],
        is_movie=is_movie,
        runtime=data['movieLength'],
        seasons_count=0
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
            director, _ = Director.objects.get_or_create(id=director['id'], name=director['name'])

            director.titles.add(title)


def add_title_countries(data):
    title = Title.objects.get(id=data['id'])
    for country in data['countries']:
        country, _ = Country.objects.get_or_create(title=country['name'])

        country.titles.add(title)


def add_title_actors(data):
    title = Title.objects.get(id=data['id'])
    for actor in data['persons']:
        if actor['profession'] == 'актеры' and actor['name']:
            actor, _ = Actor.objects.get_or_create(id=actor['id'], name=actor['name'])

            actor.titles.add(title)


def add_title_content_rating(data):
    title = Title.objects.get(id=data['id'])
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

    for page in range(env('START_PAGE'), env('END_PAGE')+1):
        url = 'https://api.kinopoisk.dev/v1.3/movie?selectFields=id name similarMovies.id ' \
              'year rating.imdb votes.imdb type movieLength countries ageRating director persons.id ' \
              f'persons.name persons.profession genres&sortField=id&sortType=1&limit={env("LIMIT")}&page={page}'

        headers = {'x-api-key': env('TOKEN')}

        data = read_data_from_kinopoisk(url, headers)
        for film in data['docs']:
            if check_params(film):
                try:
                    Title.objects.get(id=film['id'])
                    print(f"[ОШИБКА] Фильм {film['name']} - уже существует!")
                except:
                    print(f"[{cnt}] ", sep='', end='')
                    add_film(film)
            else:
                if 'name' in film:
                    print(f"[ОШИБКА] Недостаточно данных для добавления фильма {film['name']}!")
                else:
                    print("[ОШИБКА] Недостаточно данных для добавления фильма None!")
            cnt += 1


if __name__ == "__main__":
    main()
