from .forms import ContactForm

def global_context(request):
    return {
        "form": ContactForm(),
        "show_success_modal": request.session.pop("show_success_modal", False),
    }
