from users.exceptions import (
    IncorrectUsernameField,
)


def validate_username(username):
    symbols = '!@#$%^&*()-=/\\,.`~+\'"'
    for symbol in symbols:
        if username.find(symbol) != -1:
            raise IncorrectUsernameField()
