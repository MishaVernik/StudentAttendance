from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='First name')
    last_name = forms.CharField(max_length=30, required=True, help_text='Last name')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.')
    group = forms.CharField(max_length=10, required=True, help_text='Your group (ex: КВ-71)')
    github = forms.CharField(max_length=254, required=False, help_text='Optional')
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name','email','group','github', 'password1', 'password2', )