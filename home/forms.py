from django import forms
import re

# Contact form for footer
class ContactForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100)
    email = forms.EmailField(label="Email")
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={"rows": 5})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ""  # Remove * for required fields


    def clean_email(self):
        email = self.cleaned_data.get('email')

        # First basic check
        if not email:
            raise forms.ValidationError("Please enter a valid email address.")

        # Stricter manual check: must have '@' and a '.' after it
        if '@' not in email or '.' not in email.split('@')[-1]:
            raise forms.ValidationError("Please enter a valid email address.")

        return email

