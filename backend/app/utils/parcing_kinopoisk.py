import time

import requests
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.utils import timezone

from config import settings
from titles.models import ContentRating, Criterion, SimilarTitle, Title, TypeCriterion


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
        if data['name'] and data['genres'] and data['year'] and data['rating'] and data['votes'] and \
                data['countries'] and data['persons']:
            return True
    return False


def check_constraints(data: dict) -> bool:
    """
    Проверка ограничений полей для БД
    :param data: словарь с одним фильмом
    :return: bool
    """
    if 1896 <= data['year'] <= timezone.now().year and 0 <= data['rating']['imdb'] <= 10 and data['votes']['imdb'] >= 0:
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
        if seasons_count == 0:
            seasons_count = data['seasonsInfo'][-2]['number']

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


def add_persons(data: dict, title: Title) -> None:
    """
    Добавление актеров и режиссеров и их связей с фильмом в БД
    :param data: словарь с одним экземпляром
    :param title: экземпляр фильма
    :return:
    """
    cnt = 0
    for person in data:
        if person['profession'] in ['актеры', 'режиссеры'] and person['name']:
            if person['profession'] == 'актеры':
                if cnt == 3:
                    continue
                criterion_type, _ = TypeCriterion.objects.get_or_create(title='actors')
                cnt += 1
            else:
                criterion_type, _ = TypeCriterion.objects.get_or_create(title='directors')
            try:
                criterion = Criterion.objects.get(title=person['id'])
            except ObjectDoesNotExist:
                criterion, _ = Criterion.objects.get_or_create(title=person['name'], type=criterion_type)

            title.criterion.add(criterion)


def add_title_content_rating(data: dict, title: Title) -> None:
    """
    Добавление возрастного ограничения и его связи с фильмом в БД
    :param data: словарь с одним экземпляром
    :param title: экземпляр фильма
    :return:
    """
    if data:
        age_rating, _ = ContentRating.objects.get_or_create(
            value=data,
        )
        title.content_rating = age_rating
        title.save()


def add_criteria(data: dict) -> None:
    """
    Добавление критериев и их связей с фильмом в БД
    :param data: словарь с одним экземпляром
    :return:
    """
    title = Title.objects.get(id=data['id'])
    for type_criterion in data.keys():
        if type_criterion in ['genres', 'countries']:
            criterion_type, _ = TypeCriterion.objects.get_or_create(title=type_criterion)
            for criterion in data[type_criterion]:
                criterion, _ = Criterion.objects.get_or_create(title=criterion['name'], type=criterion_type)
                title.criterion.add(criterion)
        elif type_criterion == 'persons':
            add_persons(data[type_criterion], title)
        elif type_criterion == 'ageRating':
            add_title_content_rating(data[type_criterion], title)


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
        except ObjectDoesNotExist:
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
        add_title(data)
        add_criteria(data)
        add_similar_titles(data, update_mode, cnt_changes)
        print(f"Фильм {data['name']} - успешно добавлен!")
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
        film_id = film['id']
        try:
            Title.objects.get(id=film_id)
            if check_constraints(film):
                cnt_changes = fill_database(film, update_mode, cnt_changes)
        except ObjectDoesNotExist:
            pass
    else:
        try:
            title = Title.objects.get(id=film['id'])
            print(f'[INFO] Фильм {title.title} - уже существует!')
        except ObjectDoesNotExist:
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
    if check_params(film) and check_duration(film) and check_seasons(film):
        cnt_changes = add_film_to_database(film, cnt, update_mode, cnt_changes)
    else:
        if not update_mode:
            if 'name' in film:
                film_name = film['name']
                print(f'[ERROR] Недостаточно данных для добавления фильма {film_name}!')
            else:
                print('[ERROR] Недостаточно данных для добавления фильма None!')
    return cnt_changes


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
    update_mode = settings.UPDATE

    for page in range(start_page, end_page + 1):
        url = 'https://api.kinopoisk.dev/v1.3/movie?selectFields=id name similarMovies.id isSeries ' \
              'year rating.imdb votes.imdb movieLength countries ageRating director persons.id seasonsInfo ' \
              f'persons.name persons.profession genres&limit={limit}&page={page}'

        headers = {'x-api-key': token}

        data = read_data_from_kinopoisk(url, headers)
        cnt_changes = 0
        for film in data['docs']:
            cnt_changes = add_film(film, cnt, update_mode, cnt_changes)
            cnt += 1
        if update_mode:
            print(f'Для {limit} фильмов добавлено {cnt_changes} похожих!')


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time() - start
    print(f'\nВремя выполнения программы - {round(end, 2)} сек')
