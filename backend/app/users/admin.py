from django.contrib import admin

from users import models, forms


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    """
    Административная панель пользователей
    """
    form = forms.UserAdminForm
    list_display = ('username', 'email', 'is_staff', 'is_active')


@admin.register(models.History)
class HistoryAdmin(admin.ModelAdmin):
    """
    Административная панель историй опросов
    """
    pass


@admin.register(models.LikedTitle)
class LikedTitleAdmin(admin.ModelAdmin):
    """
    Административная панель понравившихся произведений
    """
    pass


@admin.register(models.DislikedTitle)
class DislikedTitleAdmin(admin.ModelAdmin):
    """
    Административная панель не понравившихся произведений
    """
    pass


@admin.register(models.PreferredGenre)
class PreferredGenreAdmin(admin.ModelAdmin):
    """
    Административная панель предпочитаемых жанров
    """
    pass
