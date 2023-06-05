from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    Менеджер модели пользователя
    """
    def _create_user(
        self,
        username,
        email,
        password,
        is_staff,
        is_superuser,
        **extra_fields,
    ):
        if not username:
            raise ValueError('Username must be set')
        if not email:
            raise ValueError('Email must be set')
        if not password:
            raise ValueError('Password must be set')

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(
        self,
        username,
        email,
        password,
        **extra_fields,
    ):
        return self._create_user(
            username=username,
            email=email,
            password=password,
            is_staff=False,
            is_superuser=False,
            **extra_fields,
        )

    def create_superuser(
        self,
        username,
        email,
        password,
        **extra_fields,
    ):
        return self._create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
            **extra_fields,
        )
