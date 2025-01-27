from .views import RegistrationView, UsernameValidationView,EmailValidationView, LoginView, Logoutview
from django.urls import path

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('validate-username/', (UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email/', (EmailValidationView.as_view()), name='validate-email'),
    path('login/', (LoginView.as_view()), name='login'),
    path('logout/', (Logoutview.as_view()), name='logout'),
    
    

]