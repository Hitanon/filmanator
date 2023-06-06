from rest_framework.exceptions import APIException


class IncorrectUserData(APIException):
    status_code = 400
    default_detail = {
        'status': 'fail',
        'detail': 'Неправильные данные',
    }


class AlreadyAuthorized(APIException):
    status_code = 401
    default_detail = {
        'status': 'fail',
        'detail': 'Вы уже авторизованы. Пожалуйста, сначала выйдете из аккаунта',
    }


class UserNotFound(APIException):
    status_code = 404
    default_detail = {
        'status': 'fail',
        'detail': 'Пользователь не найден',
    }
