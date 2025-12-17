from django.urls import path 
from .views import home
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', home, name='home'), 
    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]