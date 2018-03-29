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


FIELD_NAME_MAPPING = {
    'OTP': 'OTP',
    'g_recaptcha_response': 'g-recaptcha-response'
}


class TwoFactorForm(forms.Form):
    OTP = forms.IntegerField(required=True)
    g_recaptcha_response = forms.CharField(max_length=500)

    def add_prefix(self, field_name):
        field_name = FIELD_NAME_MAPPING.get(field_name, field_name)
        return super(TwoFactorForm, self).add_prefix(field_name)
