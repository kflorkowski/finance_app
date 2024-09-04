from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout


def welcome(request):
    '''
    GET - Przekierowuje na strone powitalną z możliwością
    zalogowania/zarejestrowania
    '''
    return render(request, 'welcome.html')


def register(request):
    '''
    GET - wyświetla formularz rejestracji użytkownika.

    POST - jeżeli formularz jest wypełniony poprawnie,
    zapisuje nowego użytkownika w bazie danych, 
    informuje o pomyślnym utworzeniu konta oraz
    przekierowuje do widoku logowania.
    '''
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    '''
    GET - wyświelta formularz logowania użytkownika

    POST - jeżeli dane logowania są poprawne to 
    loguje użytkownika i przekierowuje na stronę główną
    aplikacji. Jeżeli dane są nie poprawne, wyświetla
    komunikat informującyo niepoprawności loginu lub hasła. 
    '''
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
