from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from account.models import Account
from .models import Bike, Station
from django.contrib.auth import authenticate


class TopUpForm(forms.Form):
    money = forms.FloatField(label='Top Up Amount', max_value=100.0, min_value=5.0)


class PayBalanceForm(forms.Form):
    money = forms.FloatField(label='Payment Amount')


class LocationForm(forms.ModelForm):
    locations = forms.ModelChoiceField(queryset=Station.objects.all(), label='Station Location')

    class Meta:
        model = Station
        fields = ['locations']


class RegistrationForm(UserCreationForm):

    ROLE_CHOICES = (
        ('Customer', 'Customer'),
        ('Operator', 'Operator'),
        ('Manager', 'Manager'),
    )
    email = forms.EmailField(max_length=60, help_text='Add valid email address')

    class Meta:
        model = Account
        fields = ["username", "email", "password1", "password2"]


class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('username', 'password')

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not authenticate(username=username, password=password):
            raise forms.ValidationError('Invalid Login')

