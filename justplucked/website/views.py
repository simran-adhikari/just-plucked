from django.shortcuts import render
from website.models import *
def home_view(request):
    homepage_data = HomepageData.objects.first()

    if not homepage_data:
        # If no HomepageData exists, create a new one
        homepage_data = HomepageData.objects.create()

    # Fetch trending and popular products
    trending_products = homepage_data.trending.all()
    popular_products = homepage_data.popular.all()

    # Pass the data to the template
    return render(request, 'website/home.html', {
        'trending_products': trending_products,
        'popular_products': popular_products,
    })
    

def about_view(request):
    return render(request, 'website/about.html')

def contact_view(request):
    return render(request, 'website/contact.html')

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import FarmerRegistrationForm
from django.contrib import messages
from django.conf import settings

def farmer_registration(request):
    if request.method == 'POST':
        form = FarmerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            farmer = form.save()  # Save the farmer data with is_active = False
            messages.success(request, "Your registration is successful! Your account is awaiting approval.")
            return redirect('sell-with-us')
    else:
        form = FarmerRegistrationForm()

    return render(request, 'website/registration/farmer_registration.html', {'form': form})

