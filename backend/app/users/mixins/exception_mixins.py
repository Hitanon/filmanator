from rest_framework.exceptions import APIException


class BaseExceptionMixin(APIException):
    status_code = None
    default_detail = None
    alternative_detail = None

    def __init__(self, **kwargs):
        code = kwargs.get('code', None)
        self.default_detail.update(kwargs)
        if code and code == 'unique':
            self.default_detail['detail'] = self.alternative_detail
        super().__init__(self.default_detail, self.status_code)
