from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserChangeForm


class CustomSignupForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=255,
        required=True,
        label="Full Name",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your full name",
            "autofocus": "autofocus",  # Keep focus here
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

        # Remove unwanted autofocus
        self.fields["email"].widget.attrs.pop("autofocus", None)
        self.fields["password1"].widget.attrs.pop("autofocus", None)


    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data.get("full_name")
        # Ensure username is populated with email to avoid unique constraint error
        user.username = self.cleaned_data.get("email")
        if commit:
            user.save()
        return user


class CustomLoginForm(AuthenticationForm):
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
    password = None  # hide password field

    class Meta:
        model = CustomUser
        fields = [
            "full_name",
            "email",
        ]
