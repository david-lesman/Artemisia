from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "input is-medium",
                "placeholder": "Password",
            }
        ),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "input is-medium",
                "placeholder": "Confirm Password",
            }
        ),
    )


class MyResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        label="",
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "class": "input is-medium",
                "placeholder": "Email",
                "required": "true",
            }
        ),
    )
