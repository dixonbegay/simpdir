from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import LDAPuser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = LDAPuser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = LDAPuser
        fields = ('email',)