from users import exceptions


class ExceptionParserMixin:
    def _get_exception_keys(self, exc):
        return tuple(exc.args[0].keys())

    def _get_exception_code(self, exc, key):
        return exc.args[0][key][0].code

    def _get_detail(self, code, key):
        return {
            'detail': f'пользователь с таким {key} уже существует',
            'code': code,
        } if code == 'unique' else {
            'detail': f'Неверный {key}',
            'code': 'incorrect',
        }

    def _raise_exception(self, exc, key):
        exception_classes = {
            'email': exceptions.IncorrectEmailField,
            'username': exceptions.IncorrectUsernameField,
            'password': exceptions.IncorrectPasswordField,
        }
        code = self._get_exception_code(exc, key)
        details = self._get_detail(code, key)
        raise exception_classes[key](**details)

    def _parse_exception(self, exc):
        keys = self._get_exception_keys(exc)
        if len(keys) == 1:
            self._raise_exception(exc, keys[0])

        details = {}
        for key in keys:
            code = self._get_exception_code(exc, key)
            details[key] = self._get_detail(code, key)
        raise exceptions.CustomValidationError(**details)
