from django.shortcuts import render, redirect
from .models import Registration

def register_user(request):
    if request.method == 'POST':
        Registration.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=request.POST['password'],
            confirm_password=request.POST['confirm_password'],
            date_of_birth=request.POST['date_of_birth'],
            gender=request.POST.get('gender', '')
        )
        return redirect('register_user')
    return render(request, 'registration/register.html')
