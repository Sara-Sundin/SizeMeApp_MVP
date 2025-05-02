from .forms import ContactForm

def global_context(request):
    """
    Provides global context variables to all templates.

    Includes:
    - A contact form instance with a 'contact' prefix, used in the footer.
    - A flag to show the contact success modal if the session indicates a message was sent.
    """
    return {
        # Reusable contact form shown in the footer of all templates
        "contact_form": ContactForm(prefix='contact'),

        # Flag used to trigger a "Message sent" modal
        "show_success_modal": request.session.get("show_success_modal", False),
    }
