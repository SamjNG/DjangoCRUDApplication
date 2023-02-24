from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, User, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

# Create your views here.

def home(request):

    return render(request, 'home.html')

def signup(request): 

    if request.method == 'GET':
        print('Registro enviado')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.createuser(username=request.POST['username'],
                                               password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })
        else:
            return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Password do not match'
                })
        
    return render(request, 'signup.html', {
        'form': UserCreationForm
    })

def tasks(request):
    return render(request, 'tasks.html')

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {
            'form': AuthenticationForm,
            'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')