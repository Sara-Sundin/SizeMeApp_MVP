from .forms import ContactForm

def contact_form(request):
    return {
        "form": ContactForm()
    }
