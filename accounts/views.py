from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import login, logout
from .forms import CustomSignupForm, CustomLoginForm, CustomUserUpdateForm
from .models import CustomUser
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def dashboard_view(request):
    user = request.user
    show_modal = not all([user.chest, user.waist, user.hips, user.shoulders])
    return render(request, 'accounts/dashboard.html', {"show_modal": show_modal})


@login_required
def update_measurements(request):
    if request.method == "POST":
        user = request.user
        user.chest = request.POST.get("chest")
        user.waist = request.POST.get("waist")
        user.hips = request.POST.get("hips")
        user.shoulders = request.POST.get("shoulders")
        user.save()
    return redirect("dashboard")


def custom_logout(request):
    logout(request)
    return redirect('home')  # Change to 'login' or any page you prefer


class SignupView(CreateView):
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
    template_name = 'accounts/login.html'
    authentication_form = CustomLoginForm


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        return self.request.user
