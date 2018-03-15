from django.shortcuts import render
from django.contrib.auth import authenticate
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect


def login(request):
    return render(request, 'login/login.html',{})

def on_login(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(username = username, password = password)
    if user is not None:
        return HttpResponseRedirect(reverse("polls:index"))
    else:
        return HttpResponseRedirect(reverse("login:login"))



