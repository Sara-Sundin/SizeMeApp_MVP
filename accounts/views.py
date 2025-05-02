from django.contrib.auth import update_session_auth_hash, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import CustomSignupForm, CustomLoginForm, CustomUserUpdateForm
from .models import CustomUser


@login_required
def dashboard_view(request):
    """
    Display the user dashboard, including flags for showing modals related to
    profile updates, measurements, and redirect feedback.
    """
    user = request.user
    show_modal = not all([user.chest, user.waist, user.hips, user.shoulders])
    show_profile_updated_modal = request.session.pop("show_profile_updated_modal", False)
    show_measurements_updated_modal = request.session.pop("show_measurements_updated_modal", False)
    show_measurements_deleted_modal = request.session.pop("show_measurements_deleted_modal", False)
    show_redirect_modal = request.session.pop("show_redirect_modal", False)

    return render(request, 'accounts/dashboard.html', {
        "show_modal": show_modal,
        "show_profile_updated_modal": show_profile_updated_modal,
        "show_measurements_updated_modal": show_measurements_updated_modal,
        "show_measurements_deleted_modal": show_measurements_deleted_modal,
        "redirect_modal": show_redirect_modal,
    })


@login_required
def login_update_measurements(request):
    """
    Update user measurements upon login and set a session flag to trigger
    a redirect modal in the dashboard.
    """
    if request.method == "POST":
        user = request.user
        user.chest = request.POST.get("chest")
        user.waist = request.POST.get("waist")
        user.hips = request.POST.get("hips")
        user.shoulders = request.POST.get("shoulders")
        user.save()

        request.session["show_redirect_modal"] = True
        return redirect("dashboard")


@login_required
def update_measurements(request):
    """
    Save new measurement values from the dashboard and set a success modal flag.
    """
    if request.method == "POST":
        user = request.user
        user.chest = request.POST.get("chest")
        user.waist = request.POST.get("waist")
        user.hips = request.POST.get("hips")
        user.shoulders = request.POST.get("shoulders")
        user.save()

        request.session["show_measurements_updated_modal"] = True
    return redirect("dashboard")


@login_required
def delete_measurements(request):
    """
    Remove all measurement values for the current user and set a deleted modal flag.
    """
    if request.method == "POST":
        user = request.user
        user.chest = None
        user.waist = None
        user.hips = None
        user.shoulders = None
        user.save()

        request.session["show_measurements_deleted_modal"] = True
    return redirect("dashboard")


@login_required
def delete_account(request):
    """
    Permanently delete the user account and set a session flag to show a farewell modal.
    """
    if request.method == "POST":
        request.user.delete()
        logout(request)
        request.session["show_account_deleted_modal"] = True
        return redirect('home')


def custom_logout(request):
    """
    Log the user out and set a flag to trigger a logged-out modal on the homepage.
    """
    logout(request)
    request.session["show_logged_out_modal"] = True
    return redirect("home")


class SignupView(CreateView):
    """
    View for handling new user sign-up using the CustomSignupForm.
    Automatically logs in the user upon successful sign-up.
    """
    model = CustomUser
    form_class = CustomSignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class CustomLoginView(LoginView):
    """
    View for handling user login using the custom login form.
    """
    template_name = 'accounts/login.html'
    authentication_form = CustomLoginForm


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating the user's profile (e.g. full name and email).
    Supports password update with session re-authentication.
    """
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        user = form.save(commit=False)
        password = self.request.POST.get("password1")

        if password:
            user.set_password(password)
            update_session_auth_hash(self.request, user)

        user.save()
        self.request.session["show_profile_updated_modal"] = True
        return redirect(self.success_url)
