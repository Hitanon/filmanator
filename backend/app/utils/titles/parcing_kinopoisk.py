import time

from config import settings

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.utils import DataError
from django.utils import timezone

import requests

from titles.models import Actor, ContentRating, Country, Director, Genre, SimilarTitle, Title


def read_data_from_kinopoisk(url: str, headers: dict) -> dict:
    """
    Чтение данных с api кинопоиска
    :param url: адрес для нужного запроса к api
    :param headers: заголовок запроса с указанием токена
    :return: data - словарь со списком фильмов
    """
    while True:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.HTTPError:
            time.sleep(5)


def check_params(data: dict) -> bool:
    """
    Проверка значений необходимых полей для БД
    :param data: словарь с одним фильмом
    :return: bool
    """
    if 'id' in data:
        if (data['name'] or data['alternativeName'] or data['enName']) and data['year']:
            return True
    return False


def check_constraints(data: dict) -> bool:
    """
    Проверка ограничений полей для БД
    :param data: словарь с одним фильмом
    :return: bool
    """
    if 'imdb' in data['rating']:
        if data['rating']['imdb'] is None:
            data['rating']['imdb'] = 0
    if 'imdb' in data['votes']:
        if data['votes']['imdb'] is None:
            data['votes']['imdb'] = 0
    if 1896 <= data['year'] <= timezone.now().year and 0 <= data['rating']['imdb'] <= 10 and data['votes']['imdb'] >= 0:
        return True
    return False


def change_name(data: dict) -> dict:
    """
    Изменение основного названия фильма
    :param data: словарь с одним экземпляром
    :return:
    """
    if data['name']:
        pass
    elif data['alternativeName']:
        data['name'] = data['alternativeName']
    else:
        data['name'] = data['enName']
    return data


def add_title(data: dict) -> Title:
    """
    Добавление фильма или сериала в БД
    :param data: словарь с одним экземпляром
    :return:
    """
    data = change_name(data)

    if 'movieLength' in data:
        duration = data['movieLength']
    else:
        duration = None

    if data['isSeries']:
        if data['seasonsInfo']:
            seasons_count = data['seasonsInfo'][-1]['number']
            if seasons_count == 0 and len(data['seasonsInfo']) > 1:
                seasons_count = data['seasonsInfo'][-2]['number']
        else:
            seasons_count = None

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
            duration=duration,
        )
    return title


def add_title_genres(data: dict, title: Title) -> None:
    """
    Добавление жанров и их связей с фильмом в БД
    :param data: словарь с одним экземпляром
    :param title: экземпляр фильма
    :return:
    """
    for genre in data['genres']:
        try:
            genre, _ = Genre.objects.get_or_create(title=genre['name'])
            title.genre.add(genre)
        except DataError:
            pass


def add_director(director: dict, title: Title) -> None:
    """
    Добавление режиссера и его связи с фильмом в БД
    :param director: словарь с одним режиссером
    :param title: экземпляр фильма
    :return:
    """
    if director['profession'] == 'режиссеры' and director['name']:
        try:
            director = Director.objects.get(id=director['id'])
        except ObjectDoesNotExist:

            director, _ = Director.objects.get_or_create(id=director['id'],
                                                         name=director['name'],
                                                         count_awards=None,
                                                         )
        title.director.add(director)


def add_title_directors(data: dict, title: Title) -> None:
    """
    Добавление режиссеров и их связей с фильмом в БД
    :param data: словарь с одним экземпляром
    :param title: экземпляр фильма
    :return:
    """
    for director in data['persons']:
        try:
            add_director(director, title)
        except DataError:
            pass


def add_title_countries(data: dict, title: Title) -> None:
    """
    Добавление стран и их связей с фильмом в БД
    :param data: словарь с одним экземпляром
    :param title: экземпляр фильма
    :return:
    """
    for country in data['countries']:
        try:
            country, _ = Country.objects.get_or_create(title=country['name'])
            title.country.add(country)
        except DataError:
            pass


def add_actor(actor: dict, title: Title) -> None:
    """
    Добавление актера и их связей с фильмом в БД
    :param actor: словарь с одним актером
    :param title: экземпляр фильма
    :return:
    """
    try:
        actor = Actor.objects.get(id=actor['id'])
    except ObjectDoesNotExist:
        actor, _ = Actor.objects.get_or_create(id=actor['id'],
                                               name=actor['name'],
                                               count_awards=None,
                                               )
    title.actor.add(actor)


def add_title_actors(data: dict, title: Title) -> None:
    """
    Добавление актера и их связей с фильмом в БД
    :param data: словарь с одним экземпляром
    :param title: экземпляр фильма
    :return:
    """
    cnt = 0
    for actor in data['persons']:
        if actor['profession'] == 'актеры' and actor['name']:
            if cnt == 3:
                break
            try:
                add_actor(actor, title)
                cnt += 1
            except DataError:
                pass


def add_title_content_rating(data: dict, title: Title) -> None:
    """
    Добавление возрастного ограничения и его связи с фильмом в БД
    :param data: словарь с одним экземпляром
    :param title: экземпляр фильма
    :return:
    """
    if data['ageRating']:
        try:
            age_rating, _ = ContentRating.objects.get_or_create(
                value=data['ageRating'],
            )
            title.content_rating = age_rating
            title.save()
        except DataError:
            pass


def add_similar_title(data: dict, update_mode: bool, similar_title: dict, cnt_changes: int) -> int:
    """
    Добавление одного похожего фильма в БД
    :param data: словарь с одним экземпляром
    :param update_mode: режим обновления или добавления похожих фильмов
    :param similar_title: словарь с данными об одном похожем фильме
    :param cnt_changes: кол-во добавленных похожих фильмов
    :return:
    """
    Title.objects.get(id=similar_title['id'])
    if update_mode:
        try:
            SimilarTitle.objects.create(
                title_id=data['id'],
                similar_title_id=similar_title['id'],
            )
            cnt_changes += 1
        except IntegrityError:
            pass
    else:
        SimilarTitle.objects.update_or_create(
            title_id=data['id'],
            similar_title_id=similar_title['id'],
        )
    return cnt_changes


def add_similar_titles(data: dict, update_mode: bool, cnt_changes: int) -> int:
    """
    Добавление похожих фильмов и их связей с фильмом в БД
    :param data: словарь с одним экземпляром
    :param update_mode: режим обновления или добавления похожих фильмов
    :param cnt_changes: кол-во добавленных похожих фильмов
    :return:
    """
    for similar_title in data['similarMovies']:
        try:
            cnt_changes = add_similar_title(data, update_mode, similar_title, cnt_changes)
        except Title.DoesNotExist:
            pass
    return cnt_changes


def fill_database(data: dict, update_mode: bool, cnt_changes: int) -> int:
    """
    Добавление фильма в БД
    :param data: словарь с одним экземпляром
    :param update_mode: режим обновления или добавления похожих фильмов
    :param cnt_changes: кол-во добавленных похожих фильмов
    :return:
    """
    if update_mode:
        cnt_changes = add_similar_titles(data, update_mode, cnt_changes)
    else:
        try:
            title = add_title(data)
        except (IndexError, DataError):
            if 'name' in data:
                film_name = data['name']
                print(f'[ERROR] Недостаточно данных для добавления фильма {film_name}!')
            else:
                print('[ERROR] Недостаточно данных для добавления фильма None!')
            return cnt_changes

        add_title_genres(data, title)
        add_title_countries(data, title)
        add_title_actors(data, title)
        add_title_directors(data, title)
        add_title_content_rating(data, title)
        add_similar_titles(data, update_mode, cnt_changes)
        print(f"Фильм {data['name']} - успешно добавлен!")

    return cnt_changes


def add_film_to_database_update_mode(film: dict, update_mode: bool, cnt_changes: int) -> int:
    """
    Добавление фильма в БД в режиме обновления
    :param film: словарь с одним экземпляром
    :param update_mode: режим обновления или добавления похожих фильмов
    :param cnt_changes: кол-во добавленных похожих фильмов
    :return:
    """
    film_id = film['id']
    try:
        Title.objects.get(id=film_id)
        if check_constraints(film):
            cnt_changes = fill_database(film, update_mode, cnt_changes)
    except Title.DoesNotExist:
        pass
    return cnt_changes


def add_film_to_database(film: dict, cnt: int, update_mode: bool, cnt_changes: int) -> int:
    """
    Добавление фильма в БД
    :param film: словарь с одним экземпляром
    :param cnt: порядковый номер загружаемого фильма
    :param update_mode: режим обновления или добавления похожих фильмов
    :param cnt_changes: кол-во добавленных похожих фильмов
    :return:
    """
    if update_mode:
        cnt_changes = add_film_to_database_update_mode(film, update_mode, cnt_changes)
    else:
        try:
            title = Title.objects.get(id=film['id'])
            print(f'[INFO] Фильм {title.title} - уже существует!')
        except Title.DoesNotExist:
            print(f'[{cnt}] ', sep='', end='')
            if check_constraints(film):
                fill_database(film, update_mode, cnt_changes)
            else:
                print(f"Фильм {film['name']} - не соответствуют ограничениям!")
    return cnt_changes


def add_film(film: dict, cnt: int, update_mode: bool, cnt_changes: int) -> int:
    """
    Проверка корректности полученных данных о фильме и добавление фильма
    :param film: словарь с одним экземпляром
    :param cnt: порядковый номер загружаемого фильма
    :param update_mode: режим обновления или добавления похожих фильмов
    :param cnt_changes: кол-во добавленных похожих фильмов
    :return:
    """
    if check_params(film):
        cnt_changes = add_film_to_database(film, cnt, update_mode, cnt_changes)
    else:
        if not update_mode:
            if 'name' in film:
                film_name = film['name']
                print(f'[ERROR] Недостаточно данных для добавления фильма {film_name}!')
            else:
                print('[ERROR] Недостаточно данных для добавления фильма None!')
    return cnt_changes


def add_count_awards_to_database(headers: dict, model, list_persons, count_people: int) -> None:
    """
    Добавление кол-ва наград определенному кол-ву человек
    :param headers: заголовок запроса
    :param model: модель персонажей (актеры или режиссеры)
    :param list_persons: список персонажей
    :param count_people: кол-во персонажей
    :return:
    """
    url = f'https://api.kinopoisk.dev/v1/person?selectFields=id countAwards&limit={count_people + 1}'
    for person in list_persons:
        url += '&id=' + str(person.pk)
    data = read_data_from_kinopoisk(url, headers)
    persons = data['docs']
    for person in persons:
        try:
            element = model.objects.get(id=person['id'])
            element.count_awards = person['countAwards']
            element.save()
        except (ObjectDoesNotExist, KeyError):
            pass


def add_count_awards_to_persons(headers: dict, model) -> None:
    """
    Добавление кол-ва наград определенной модели людей
    :param headers: заголовок запроса
    :param model: модель персонажей (актеры или режиссеры)
    :return:
    """
    count_people = 1000
    start_num = 0
    end_num = count_people
    all_persons = model.objects.all()
    try:
        list_persons = all_persons[start_num:end_num]
    except IndexError:
        list_persons = all_persons[start_num:]
    while len(list_persons) and len(list_persons) != 1:
        add_count_awards_to_database(headers, model, list_persons, count_people)
        start_num += count_people
        end_num += count_people
        print(f'{len(list_persons)} персонажей обработано!')
        try:
            list_persons = all_persons[start_num-1:end_num]
        except IndexError:
            list_persons = all_persons[start_num-1:]


def add_count_awards(headers: dict) -> None:
    """
    Добавление кол-ва наград
    :param headers: заголовок запроса
    :return:
    """
    model_list = [Actor, Director]
    for model in model_list:
        add_count_awards_to_persons(headers, model)


def add_seasons_count_to_database(limit: int, page: int, headers: dict) -> None:
    """
    Добавление кол-ва сезонов
    :param limit: кол-во получаемых из api сериалов за один раз
    :param page: номер страницы из api с сериалами
    :param headers: заголовок запроса
    :return:
    """
    url = f'https://api.kinopoisk.dev/v1/season?selectFields=movieId number&sortField=number&sortType=1&' \
          f'limit={limit}&page={page}'
    data = read_data_from_kinopoisk(url, headers)
    serials = data['docs']
    for serial in serials:
        try:
            title = Title.objects.get(pk=serial['movieId'])
            title.seasons_count = serial['number']
            title.save()
        except (Title.DoesNotExist, KeyError):
            pass


def read_and_write_films(limit: int, page: int, update_mode: bool, headers: dict, cnt: int) -> int:
    """
    Чтение и запись в базу данных фильмов
    :param limit: кол-во получаемых из api фильмов за один раз
    :param page: номер страницы из api с фильмами
    :param update_mode: режим записи фильмов
    :param headers: заголовок запроса к api
    :param cnt: номер обработанного фильма
    :return:
    """
    url = 'https://api.kinopoisk.dev/v1.3/movie?selectFields=id name enName alternativeName similarMovies.id ' \
          'isSeries year rating.imdb votes.imdb movieLength countries ageRating persons.id seasonsInfo ' \
          f'persons.name persons.profession genres&limit={limit}&page={page}'

    data = read_data_from_kinopoisk(url, headers)
    cnt_changes = 0
    for film in data['docs']:
        try:
            cnt_changes = add_film(film, cnt, update_mode, cnt_changes)
        except KeyError:
            pass
        cnt += 1
    if update_mode:
        print(f'Добавлено {cnt_changes} похожих фильмов!')
    return cnt


def main():
    """
    Получение списка фильмов через api кинопоиска и их добавление в БД
    :param:
    :return:
    """
    start_page = settings.START_PAGE
    end_page = settings.END_PAGE
    limit = settings.LIMIT
    token = settings.TOKEN
    update_mode = settings.UPDATE
    headers = {'x-api-key': token}
    cnt = 1
    if update_mode:
        print('---Началось заполнение кол-во наград актеров и режиссеров---')
        add_count_awards(headers)
        print('---Закончилось заполнение кол-во наград актеров и режиссеров---')

        print('---Началось заполнение кол-во сезонов сериалов---')
        for page in range(start_page, end_page + 1):
            add_seasons_count_to_database(limit, page, headers)
        print('---Закончилось заполнение кол-во сезонов сериалов---')

    for page in range(start_page, end_page + 1):
        cnt = read_and_write_films(limit, page, update_mode, headers, cnt)


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time() - start
    print(f'\nВремя выполнения программы - {round(end, 2)} сек')
