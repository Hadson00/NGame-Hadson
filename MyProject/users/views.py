from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm, UserRegistrationForm
from django.contrib import messages
from .models import User
from users.decorators import user_is_admin, user_is_client
from django.contrib.auth.decorators import login_required, user_passes_test

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user_temp = User.objects.get(email= email)
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=user_temp, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard_admin' if user.user_type == 'admin' else 'dashboard_client')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request, 'Cadastrado com sucesso!')
            return redirect('login')
        else:
            messages.error(request, 'Erro ao cadastrar!')
    else:
        form = UserRegistrationForm()
    return render(request, 'site/signup.html', {'form':form})

@login_required
@user_passes_test(user_is_admin)
def admin_page(request):
    return render(request, 'site/dashboard_admin.html')

@login_required
@user_passes_test(user_is_client)
def client_page(request):
    return render(request, 'site/dashboard_client.html')