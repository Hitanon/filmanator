from rest_framework.test import APITestCase


class UserViewTests(APITestCase):
    """
    Тесты
    Создание пользователя
    1) Успешное создание пользователя
    2) Некорректная почта
    3) Некорректный username
    4) Некорректный пароль
    5) Пользователь с таким email уже существует
    6) Пользователь с таким username уже существует
    7) Пользователь уже авторизован

    Получение токена
    1) Успешное получение токена
    2) Отсутсвует email
    3) Отсутсвует password

    Удаление пользователя
    1) Удачное удаление пользователя
    2) Пользователь неавторизован
    """
    pass