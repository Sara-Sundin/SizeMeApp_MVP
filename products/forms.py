from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category


class ProductForm(forms.ModelForm):
    """
    Form for creating and updating Product instances
    in the admin or custom views.
    Overrides the default image widget and customizes
    the category choices and styling.
    """

    # Override the image field to use a custom widget
    image = forms.ImageField(
        label='Image',
        required=False,
        widget=CustomClearableFileInput
    )

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
        Customize the form on initialization:
        - Replace category choices with friendly names
        - Add consistent styling to all form fields
        """
        super().__init__(*args, **kwargs)

        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        self.fields['category'].choices = friendly_names

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
