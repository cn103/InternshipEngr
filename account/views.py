import re
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from account.models import Account
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
# Create your views here.


def index(request):
    return render(request, "account/index.html")


def register_page(request):
    return render(request, "account/register.html")


def login_page(request):
    return render(request, "account/login.html")


def logout(request):
    auth_logout(request)
    messages.warning(request, "Logged out")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def login(request):
    # Check user is already login
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("account:index"))
    # Check this view use when submit login or not if not return to index
    if request.method == "POST":
        # login process
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.warning(request, "Invalid credential")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, "account/index.html")


def register(request):
    # Check this view use when call register page or use when submit register form
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        re_password = request.POST["re_password"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        tel = request.POST["tel"]
        type = request.POST["type"]
        address = request.POST["address"]
        year = request.POST["year"]
        major = request.POST["major"]
        # Check username is already taken
        if User.objects.filter(username=username).first():
            return render(request, "account/register.html", {"fail_username": "This username is already taken"})
        # Check the validity of a Password
        if (len(password) < 8):
            return render(request, "account/register.html", {"fail_password": "Password must have at least 8"})
        elif not re.search("[a-z]", password):
            return render(request, "account/register.html", {"fail_password": "Password must have at least 1 of a-z"})
        elif not re.search("[A-Z]", password):
            return render(request, "account/register.html", {"fail_password": "Password must have at least 1 of A-Z"})
        elif not re.search("[0-9]", password):
            return render(request, "account/register.html", {"fail_password": "Password must have at least 1 of 0-9"})
        # Check re-password is same as password
        if password != re_password:
            return render(request, "account/register.html", {"fail_re_password": "Invalid password confirm"})
        # Check email is already taken
        if User.objects.filter(email=email).first():
            return render(request, "account/register.html", {"fail_email": "This email is already taken"})
        # Add Object User
        add_user = User(username=username, email=email,
                        first_name=first_name, last_name=last_name)
        add_user.set_password(password)
        add_user.save()

        Account.objects.create(user=add_user, tel=tel, type=type,
                               address=address, year=year, major=major)
        return render(request, "account/index.html")
    return render(request, "account/register.html")
