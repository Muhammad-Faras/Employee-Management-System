from django.contrib.auth.views import LoginView,LogoutView
from .forms import AccountsCustomLoginForm, AccountsCustomSignupForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

class AccountsLoginView(LoginView):
    form_class = AccountsCustomLoginForm
    template_name = 'accounts/login.html'  # Use your custom template
    success_url = reverse_lazy('home:home')


class AccountsSignUpView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = AccountsCustomSignupForm
    success_url = reverse_lazy('accounts:login')  # Redirect to login page on successful sign up
