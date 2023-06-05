from django.contrib import admin

from users import models
from users.forms import UserAdminForm


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ('username', 'email', 'is_staff', 'is_active')
