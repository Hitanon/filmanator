from rest_framework.exceptions import APIException


class SessionIdNotFound(APIException):
    status_code = 400
    default_code = 'session id not found'
    default_detail = {
        'details': 'session id not found in request body',
    }


class SessionNotFound(APIException):
    status_code = 404
    default_code = 'session not found'
    default_detail = {
        'details': 'session not found',
    }


class QuestionIdNotFound(APIException):
    status_code = 400
    default_code = 'question id not found'
    default_detail = {
        'details': 'question id not found in request body',
    }


class QuestionNotFound(APIException):
    status_code = 404
    default_code = 'question not found'
    default_detail = {
        'details': 'question not found',
    }


class AnswerIdNotFound(APIException):
    status_code = 400
    default_code = 'answer id not found'
    default_detail = {
        'details': 'answer id not found in request body',
    }


class AnswerNotFound(APIException):
    status_code = 404
    default_code = 'answer not found'
    default_detail = {
        'details': 'answer not found',
    }
