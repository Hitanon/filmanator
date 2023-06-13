import ast
import os
import time

from config import settings

from django.core.exceptions import ObjectDoesNotExist

from titles.models import Criterion, Title


def read_dicts_from_file(file_path: str) -> list:
    """
    Чтение словарей с параметрами фильмов из файла
    :param file_path: полный путь до файла
    :return: films - список словарей с параметрами по каждому фильму
    """
    with open(file_path, 'r') as file:
        content = file.readlines()
        films = []
        for line in content:
            film = ast.literal_eval(line)
            films.append(film)
    return films


def add_additional_criteries(film_dict: dict, title: Title):
    """
    Добавления связей фильма со всеми его параметрами
    :param film_dict: словарь с параметрами по одному фильму
    :param title: экземпляр фильма
    :return:
    """
    if film_dict['criteria']:
        for criterion_id in film_dict['criteria']:
            if criterion_id and str(criterion_id).isdigit():
                criterion = Criterion.objects.get(id=criterion_id)
                title.criterion.add(criterion)


def main():
    files_path = settings.FULL_PATH_TO_FILES
    num_file = 1
    file_path = files_path + f'rating_of_films{num_file}.txt'
    while os.path.isfile(file_path):
        my_films = read_dicts_from_file(file_path)
        for film_dict in my_films:
            if 'id' in film_dict and str(film_dict['id']).isdigit():
                title_id = film_dict['id']
                try:
                    title = Title.objects.get(id=title_id)
                    add_additional_criteries(film_dict, title)
                    print(f'Критерии добавлены для фильма с id - {title_id}!')
                except ObjectDoesNotExist:
                    print(f'Фильм с id - {title_id} нет в базе!')
        print(f'{num_file} файл успешно загружен!')
        num_file += 1
        file_path = files_path + f'rating_of_films{num_file}.txt'


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time() - start
    print(f'\nВремя выполнения программы - {round(end, 2)} сек')
