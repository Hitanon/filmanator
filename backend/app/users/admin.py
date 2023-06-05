from django.contrib import admin

from users import models
from users.forms import UserAdminForm


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ('username', 'email', 'is_staff', 'is_active')


@admin.register(models.History)
class HistoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.LikedTitle)
class LikedTitleAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DislikedTitle)
class DislikedTitleAdmin(admin.ModelAdmin):
    pass


@admin.register(models.PreferredGenre)
class PreferredGenreAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DisfavoredGenre)
class DisfavoredGenreAdmin(admin.ModelAdmin):
    pass
