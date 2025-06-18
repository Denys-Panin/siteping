from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required


def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('site-select')
    return redirect('login')


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('site-select')
    else:
        form = CustomUserCreationForm()
    return render(request, "account/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('site-select')
    else:
        form = AuthenticationForm()
    return render(request, "account/login.html", {"form": form})
