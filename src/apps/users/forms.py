from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ["email", "username", "first_name", "last_name"]
        error_class = "error"


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name"]
        error_class = "error"



# this

class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Password",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )

    # def __init__(self, *args, **kwargs):
    #     super(LoginForm, self).__init__(*args, **kwargs)
    #     # self.helper = FormHelper()
    #     # self.helper.form_class = "form-horizontal"
    #     # self.helper.label_class = "col-lg-2"
    #     # self.helper.field_class = "col-lg-8"
    #     self.helper.add_input(Submit("submit", "Login"))

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        # Add custom validation logic here, for example:
        # if not email_is_valid(email):
        #     self.add_error('email', 'Invalid email')

        # if not password_is_valid(password):
        #     self.add_error('password', 'Invalid password')

        return cleaned_data


