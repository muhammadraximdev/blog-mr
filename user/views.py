from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View

from .forms import RegisterForm, LoginForm


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'user/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        return render(request, 'user/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, "Username yoki parol noto'g'ri!")
        return render(request, 'user/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
