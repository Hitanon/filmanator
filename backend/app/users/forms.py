from django import forms

from users import models


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ('username', 'email', 'is_staff', 'is_active')
