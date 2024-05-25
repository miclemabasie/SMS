from django import forms


class VerifyPinForm(forms.Form):
    email = forms.EmailField(
        label="Password",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
    )
    pin = forms.CharField(
        label="Password",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "PIN"}),
    )
