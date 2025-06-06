from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """
    Form for collecting customer order information during checkout.

    This form customizes field attributes by:
    - Setting placeholders for user guidance
    - Styling input fields with a custom class
    - Removing default labels for a cleaner UI
    - Setting autofocus on the full name field
    """

    class Meta:
        model = Order
        fields = (
            'full_name', 'email', 'phone_number',
            'street_address1', 'street_address2',
            'town_or_city', 'postcode', 'country',
            'county',
        )
        labels = {
            'country': 'Country',
        }

    def __init__(self, *args, **kwargs):
        """
        Customize form fields:
        - Add placeholders and styling
        - Set autofocus on the first field
        - Remove auto-generated labels
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True

        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder

            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
