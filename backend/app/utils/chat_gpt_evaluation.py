import time

from django.core.exceptions import ObjectDoesNotExist

from config import settings

import ast

from titles.models import Acting, AmountOfDialogue, Audience, Graphics, Intellectuality, Mood, NarrativeMethod, \
    Title, ViewingMethod, ViewingTime, VisualAtmosphere


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


def add_additional_criteria(film_dict: dict, title: Title, criteria_name: str, criteria_class) -> None:
    """
    Добавления связи фильма с одним из его параметров
    :param film_dict: словарь с параметрами по одному фильму
    :param title: экземпляр фильма
    :param criteria_name: названия параметра
    :param criteria_class: класс параметра
    :return:
    """
    if film_dict[criteria_name]:
        for property_id in film_dict[criteria_name]:
            if property_id and str(property_id).isdigit():
                property_obj = criteria_class.objects.get(id=property_id)
                property_obj.titles.add(title)


def add_additional_criteries(film_dict: dict, title: Title):
    """
    Добавления связей фильма со всеми его параметров
    :param film_dict: словарь с параметрами по одному фильму
    :param title: экземпляр фильма
    :return:
    """
    add_additional_criteria(film_dict, title, 'mood', Mood)
    add_additional_criteria(film_dict, title, 'viewing_method', ViewingMethod)
    add_additional_criteria(film_dict, title, 'viewing_time', ViewingTime)
    add_additional_criteria(film_dict, title, 'visual_atmosphere', VisualAtmosphere)
    add_additional_criteria(film_dict, title, 'audience', Audience)
    add_additional_criteria(film_dict, title, 'intellectuality', Intellectuality)
    add_additional_criteria(film_dict, title, 'narrative_method', NarrativeMethod)
    add_additional_criteria(film_dict, title, 'acting', Acting)
    add_additional_criteria(film_dict, title, 'amount_of_dialogue', AmountOfDialogue)
    add_additional_criteria(film_dict, title, 'graphics', Graphics)


def main():
    file_path = settings.FULL_PATH_TO_FILES
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


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time() - start
    print(f'\nВремя выполнения программы - {round(end, 2)} сек')
