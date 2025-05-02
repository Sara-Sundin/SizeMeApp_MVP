from .forms import ContactForm

def global_context(request):
    return {
        "contact_form": ContactForm(prefix='contact'),
        "show_success_modal": request.session.get("show_success_modal", False),
    }
