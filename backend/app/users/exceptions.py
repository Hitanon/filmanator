from rest_framework.exceptions import APIException

from users.mixins.exception_mixins import BaseExceptionMixin


class CustomValidationError(BaseExceptionMixin):
    status_code = 400
    default_detail = {}


class IncorrectEmailField(BaseExceptionMixin):
    status_code = 400
    default_detail = {
        'code': 'incorrect email field',
        'detail': 'Неверный email',
    }
    alternative_detail = 'Пользователь с таким email уже существует'


class IncorrectUsernameField(BaseExceptionMixin):
    status_code = 400
    default_detail = {
        'code': 'incorrect username field',
        'detail': 'Неверный username',
    }
    alternative_detail = 'Пользователь с таким username уже существует'


class IncorrectPasswordField(BaseExceptionMixin):
    status_code = 400
    default_detail = {
        'code': 'incorrect password field',
        'detail': 'Неверный password',
    }


class IncorrectUserData(BaseExceptionMixin):
    status_code = 400
    default_detail = {
        'code': 'incorrect user data',
        'detail': 'Неправильные данные',
    }


class AlreadyAuthorized(APIException):
    status_code = 401
    default_detail = {
        'detail': 'Вы уже авторизованы. Пожалуйста, сначала выйдете из аккаунта',
    }


class IsAnonymous(APIException):
    status_code = 401
    default_detail = {
        'detail': 'Вы не авторизованы. В доступе отказано',
    }
