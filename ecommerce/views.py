from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserEmail

def home(request):
    if request.method == "POST":
        user_email = request.POST.get('email')

        if user_email:
            # Save email to MongoDB
            if not UserEmail.objects.filter(email=user_email).exists():
                UserEmail.objects.create(email=user_email)

            # Send email
            send_mail(
                subject="Welcome to Our Platform!",
                message=f"Hello, {user_email}. Thank you for registering.",
                from_email="genzclothing95@gmail.com",
                recipient_list=[user_email],
            )

            messages.success(request, "Email sent and saved successfully!")
            return redirect('home')
        else:
            messages.error(request, "Email is required!")

    return render(request, 'home.html')