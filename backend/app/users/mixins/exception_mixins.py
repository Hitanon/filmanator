from rest_framework.exceptions import APIException


class BaseExceptionMixin(APIException):
    status_code = None
    default_detail = None

    def __init__(self, **kwargs):
        self.default_detail.update(kwargs)
        super().__init__(self.default_detail, self.status_code)
