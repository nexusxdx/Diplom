from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Submit, Layout


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Имэйл", required=True)
    password1 = forms.CharField(label="Нууц үг", strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label="Нууц үг баталгаажуулах", strip=False, widget=forms.PasswordInput)
    error_messages = {
        'password_mismatch': "Нууц үг болон баталгаажуулах нууц үг буруу байна."
    }

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username', 'email', 'password1', 'password2',
            ButtonHolder(
                Submit('signup', 'Бүртгүүлэх')
            )
        )


class LoginForm(AuthenticationForm):
    password = forms.CharField(
        label='Нууц Үг',
        strip=False,
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username', 'password',
            ButtonHolder(
                Submit('login', 'Нэвтрэх')
            )
        )



