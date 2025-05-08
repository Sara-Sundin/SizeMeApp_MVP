from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Plan
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import logout


def index(request):
    """
    Home page view:
    - Loads the contact form (repopulated if session data is stored)
    - Displays modals based on session flags
    """
    contact_data = request.session.pop('contact_form_data', None)
    contact_form = ContactForm(contact_data, prefix='contact')
    if contact_data:
        contact_form = ContactForm(contact_data, prefix='contact')
    else:
        contact_form = ContactForm(prefix='contact')

    show_account_deleted_modal = request.session.pop(
        "show_account_deleted_modal", False)
    show_logged_out_modal = request.session.pop(
        "show_logged_out_modal", False)
    show_success_modal = request.session.pop(
        "show_success_modal", False)

    return render(request, 'home/index.html', {
        "contact_form": contact_form,
        "show_account_deleted_modal": show_account_deleted_modal,
        "show_logged_out_modal": show_logged_out_modal,
        "show_success_modal": show_success_modal,
    })


def plan_view(request):
    """
    Display the pricing plans page.
    - Optionally focuses a specific plan based on GET param `focus`.
    """
    focus = request.GET.get('focus', 'starter')  # Default to 'starter' plan
    plans = Plan.objects.all()
    return render(request, 'home/plan.html', {
        'plans': plans,
        'focus': focus,
    })


def contact(request):
    """
    Handle contact form submissions:
    - Validate form
    - Send email to internal recipient
    - Set success or error messages
    """
    if request.method == "POST":
        form = ContactForm(request.POST, prefix='contact')
        referer = request.META.get('HTTP_REFERER', '/')  # Fallback to homepage

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            try:
                send_mail(
                    subject=f"New Contact Form Submission from {name}",
                    message=(
                        f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
                    ),
                    from_email="noreply@sizemeapp.se",
                    recipient_list=["sara@sizemeapp.se"],
                    fail_silently=False,
                )
                request.session['show_success_modal'] = True
            except BadHeaderError:
                messages.error(request, "Invalid header found.")
            except Exception:
                messages.error(
                    request,
                    "Something went wrong. Please try again later."
                )
        else:
            # Persist form data in session to repopulate after redirect
            request.session['contact_form_data'] = request.POST
            messages.error(request, "Please correct the errors in the form.")

        return redirect(referer)

    return redirect('/')


def clear_success_flag(request):
    """
    Clears the 'show_success_modal' session flag without refreshing the page.
    """
    request.session.pop('show_success_modal', None)
    return HttpResponse(status=204)


def custom_logout(request):
    """
    Logs the user out and redirects to ?next= if available,
    otherwise home.
    Also sets flag to show logout modal.
    """
    logout(request)
    request.session["show_logged_out_modal"] = True
    next_url = request.GET.get('next') or 'home'
    return redirect(next_url)


def custom_404(request, exception):
    """
    Custom 404 error handler view.
    """
    return render(request, "404.html", status=404)
