from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from .forms import CustomSignupForm
from .models import CustomUser
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from .forms import CustomUserUpdateForm
from django.shortcuts import redirect

@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')


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
        # Re-render the page with form errors
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
