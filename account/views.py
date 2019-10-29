from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from BikeShare.forms import RegistrationForm, AccountAuthenticationForm


def login_view(request):

    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('/')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                role = request.user.role
                if role == 'Customer':
                    return redirect('/customer/')
                elif role == 'Operator':
                    return redirect('/operator/')
                elif role == 'Manager':
                    return redirect('/manager/')
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, 'login.html', context)


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            role = 'Customer'
            account = authenticate(username=username, password=raw_password, role=role)
            login(request, account)
            if role=='Customer':
                return redirect('/customer/')
            elif role=='Operator':
                return redirect('/operator/')
            elif role=='Manager':
                return redirect('/manager/')
        else:
            context['registation_form'] = form
    else:
        form = RegistrationForm()
        context['registation_form'] = form

    return render(request, 'signup.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')