from django.shortcuts import render
from .forms import ContactForm
from .models import Plan


def index(request):
    form = ContactForm()
    show_account_deleted_modal = request.session.pop("show_account_deleted_modal", False)
    show_logged_out_modal = request.session.pop("show_logged_out_modal", False)
    return render(request, 'home/index.html', {
        "form": form,
        "show_account_deleted_modal": show_account_deleted_modal,
        "show_logged_out_modal": show_logged_out_modal,
    })

def plan_view(request):
    focus = request.GET.get('focus', 'starter')  # fallback to starter
    plans = Plan.objects.all()
    return render(request, 'home/plan.html', {
        'plans': plans,
        'focus': focus,
    })






