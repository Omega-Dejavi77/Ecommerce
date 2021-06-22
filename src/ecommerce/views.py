from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .forms import ContactForm, LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, get_user_model

import requests

def home_page(request):
    context = {
        "title": "Hello World",
        "content": "This is content",
    }
    if request.user.is_authenticated:
        context['premium_content'] = "YEAHHHH"
    return render(request, "home_page.html", context)


def about_page(request):
    context = {
        "title": "About",
        "content": "This is content"
    }
    return render(request, "home_page.html", context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title": "Contact",
        "content": "This is content",
        "form": contact_form
    }
    if contact_form.is_valid():
        print(request.POST.get("fullname"))
    
    return render(request, "contact/view.html", context)


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request=request, username=username, password= password)
        if user is not None:
            login(request, user)
            return redirect("/login")
        else:
            print("Error")

    return render(request, "auth/login.html", context)


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = get_user_model().objects.create_user(username, email, password)
        print(new_user)

    return render(request, "auth/register.html", context)


def request_api(request):
    token = 'Token 9d543932-eedc-42f8-82f4-8515c9248db1'
    # url = 'https://community.blueliv.com/api/v1/sparks/timeline?'
    url = 'https://community.blueliv.com/api/v1/users/Blueliv/sparks'
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    return HttpResponse(response)
