from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Plan
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages


def index(request):
    form = ContactForm()
    show_account_deleted_modal = request.session.pop("show_account_deleted_modal", False)
    show_logged_out_modal = request.session.pop("show_logged_out_modal", False)
    show_success_modal = request.session.pop("show_success_modal", False)

    return render(request, 'home/index.html', {
        "form": form,
        "show_account_deleted_modal": show_account_deleted_modal,
        "show_logged_out_modal": show_logged_out_modal,
        "show_success_modal": show_success_modal,
    })


def plan_view(request):
    focus = request.GET.get('focus', 'starter')  # fallback to starter
    plans = Plan.objects.all()
    return render(request, 'home/plan.html', {
        'plans': plans,
        'focus': focus,
    })


def contact(request):
    form = ContactForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        try:
            send_mail(
                subject=f"New Contact Form Submission from {name}",
                message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                from_email="noreply@sizemeapp.se",
                recipient_list=["sara@sizemeapp.se"],
                fail_silently=False,
            )
            request.session['show_success_modal'] = True
        except BadHeaderError:
            messages.error(request, "Invalid header found.")
        except Exception:
            messages.error(request, "Something went wrong. Please try again later.")

        return redirect(request.META.get('HTTP_REFERER', '/'))

