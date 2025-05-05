from django import forms
import re


# Contact form displayed in the site footer
class ContactForm(forms.Form):
    """
    Basic contact form with name, email, and message fields.
    Used to allow users to reach out via the footer form.
    """

    name = forms.CharField(label="Name", max_length=100)
    email = forms.EmailField(label="Email")
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={"rows": 5})
    )

    def __init__(self, *args, **kwargs):
        """
        Custom initialization to remove the default colon (:)
        or asterisk (*) label suffix for required fields.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ""  # Remove default suffix like '*'

    def clean_email(self):
        """
        Additional validation for the email field:
        - Ensures the field is not empty.
        - Performs a basic structural check for '@' and
        a dot in the domain part.
        """
        email = self.cleaned_data.get('email')

        # Ensure email field is not empty (though EmailField already does this)
        if not email:
            raise forms.ValidationError("Please enter a valid email address.")

        # Extra check: must include '@' and a dot after '@'
        if '@' not in email or '.' not in email.split('@')[-1]:
            raise forms.ValidationError("Please enter a valid email address.")

        return email
