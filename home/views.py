from django.shortcuts import render
from .forms import ContactForm


def home_view(request):
    form = ContactForm()
    show_account_deleted_modal = request.session.pop("show_account_deleted_modal", False)
    show_logged_out_modal = request.session.pop("show_logged_out_modal", False)
    return render(request, 'home/index.html', {
        "form": form,
        "show_account_deleted_modal": show_account_deleted_modal,
        "show_logged_out_modal": show_logged_out_modal,
    })

def starter_plan(request):
    """
    Display the Starter Plan page.
    """
    return render(request, "home/starter_plan.html")


