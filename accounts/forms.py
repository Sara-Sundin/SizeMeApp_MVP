"""
Forms for user creation, authentication, and update using the CustomUser model.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class CustomSignupForm(UserCreationForm):
    """
    A custom user signup form that includes only full_name, email, and
    password1.

    This form excludes the password2 field and ensures the username is set
    to the email to comply with unique constraints on username.
    """
    full_name = forms.CharField(
        max_length=255,
        required=True,
        label="Full Name",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your full name",
            "autofocus": "autofocus",
        }),
    )

    class Meta:
        model = CustomUser
        fields = ("full_name", "email", "password1")
        widgets = {
            "password1": forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Password",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "password2" in self.fields:
            del self.fields["password2"]

        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter your email",
        })

        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Password (min. 8 characters)",
        })

        self.fields["email"].widget.attrs.pop("autofocus", None)
        self.fields["password1"].widget.attrs.pop("autofocus", None)

    def save(self, commit=True):
        """
        Save the user, assigning full_name and setting username to email.
        """
        user = super().save(commit=False)
        user.full_name = self.cleaned_data.get("full_name")
        user.username = self.cleaned_data.get("email")
        if commit:
            user.save()
        return user

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        try:
            validate_password(password)
        except ValidationError as e:
            self.add_error('password1', e)
        return password


class CustomLoginForm(AuthenticationForm):
    """
    A customized login form that uses email instead of username.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].label = "Email"
        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter your email",
        })

        self.fields["password"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Password",
        })


class CustomUserUpdateForm(UserChangeForm):
    """
    A form for updating user fields, excluding password.
    """
    password = None  # Hide password field

    class Meta:
        model = CustomUser
        fields = [
            "full_name",
            "email",
        ]


class MeasurementUpdateForm(forms.ModelForm):
    """
    A form for updating the user's body measurements.
    """

    class Meta:
        model = CustomUser
        fields = ['chest', 'waist', 'hips', 'shoulders']
        widgets = {
            'chest': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 20,
                'max': 200,
                'step': 0.1,
                'required': 'required',
            }),
            'waist': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 20,
                'max': 200,
                'step': 0.1,
                'required': 'required',
            }),
            'hips': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 20,
                'max': 200,
                'step': 0.1,
                'required': 'required',
            }),
            'shoulders': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 10,
                'max': 70,
                'step': 0.1,
                'required': 'required',
            }),
        }
