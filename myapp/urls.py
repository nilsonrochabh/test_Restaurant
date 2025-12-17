from django.urls import path 
from .views import home,register
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', home, name='home'), 
    
    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('register/', register, name='register'),
]