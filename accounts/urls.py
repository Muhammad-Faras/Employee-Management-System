from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    AccountsSignUpView,
)
from .forms import AccountsCustomLoginForm  # Import your custom login form

app_name = "accounts"
urlpatterns = [
    path('signup/', AccountsSignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', authentication_form=AccountsCustomLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
