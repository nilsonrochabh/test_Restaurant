from django.urls import path
from .views import home,register,produto,produto_list   
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', home, name='home'), 
    
    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('produto/', produto, name='produto'),
    path('produto_list/', produto_list, name='produto_list'),
]