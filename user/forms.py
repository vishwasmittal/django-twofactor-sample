from user.models import KoinUser
from django import forms


class UserAuthForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = KoinUser
        fields = ['username', 'email', 'password']


class UserLoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)


class TwoFactorForm(forms.Form):
    OTP = forms.IntegerField(required=True)
