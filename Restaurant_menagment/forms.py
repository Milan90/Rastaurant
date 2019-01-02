from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import *

"""
class ColectOrderForm(ModelForm):
    class Meta:
        model = Orders
        fields = ['description']
        widgets = {'details': forms.Textarea}
"""

class RegisterForm(ModelForm):
    repeat_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'groups',
                  'password'
                  )
        widgets = {'password': forms.PasswordInput}

    def clean(self):
        """
        In here you can validate the two fields
        raise ValidationError if you see anything goes wrong.
        for example if you want to make sure that field1 != field2
        """
        cleaned_data = super().clean()

        field1 = cleaned_data.get('password')
        field2 = cleaned_data.get('repeat_password')

        username = cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            self.add_error("username", "Ten użytkownik już jest w bazie!")

        if field1 != field2:
            # This will raise the error in repeat_password errors. not across all the form
            self.add_error("repeat_password", "Password i repeat password muszą być takie same")

        return cleaned_data


class LogInForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
