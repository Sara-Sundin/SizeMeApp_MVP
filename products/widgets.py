from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _


class CustomClearableFileInput(ClearableFileInput):
    """
    A custom file input widget that overrides the default ClearableFileInput.
    Used for image uploads with cleaner text and a custom template.
    """

    # Text for the checkbox to remove the current file
    clear_checkbox_label = _('Remove')

    # Label to show the currently uploaded file
    initial_text = _('Current Image')

    # Label for the input field itself (left blank here)
    input_text = _('')

    # Path to the custom template for rendering the file input
    template_name = (
            'products/custom_widget_templates/'
            'custom_clearable_file_input.html'
            )
