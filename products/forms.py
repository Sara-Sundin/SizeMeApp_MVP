from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category


class ProductForm(forms.ModelForm):
    """
    Form for creating and updating Product instances in the admin or custom views.
    Overrides the default image widget and customizes the category choices and styling.
    """

    # Override the image field to use a custom widget
    image = forms.ImageField(
        label='Image',
        required=False,
        widget=CustomClearableFileInput
    )

    class Meta:
        model = Product
        fields = '__all__'  # Include all fields from the Product model

        image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        """
        Customize the form on initialization:
        - Replace category choices with friendly names
        - Add consistent styling to all form fields
        """
        super().__init__(*args, **kwargs)

        # Fetch all categories and create a list of (id, friendly name) tuples
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        # Replace default category choices with friendly names
        self.fields['category'].choices = friendly_names

        # Add CSS classes to each form field for styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
