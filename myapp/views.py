from django.shortcuts import render
from .models import Restaurant

def home(request):
    # Fetch all restaurant objects from the database
    restaurants = Restaurant.objects.all()
    
    # Render the 'home.html' template with the list of restaurants
    return render(request, 'home.html', {'restaurants': restaurants})