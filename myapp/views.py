from django.shortcuts import render
from .models import Restaurant
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserRegistrationForm

def home(request):
    # Fetch all restaurant objects from the database
    restaurants = Restaurant.objects.all()
    
    # Render the 'home.html' template with the list of restaurants
    return render(request, 'home.html', {'restaurants': restaurants})

##registre
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro bem-sucedido. Bem-vindo!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'auth/register.html', {'form': form})