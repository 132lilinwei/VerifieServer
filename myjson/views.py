from django.shortcuts import render
from django.http import HttpResponse
from myjson.models import Securities
# Create your views here.
from django.core import serializers
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def myjson(request):
    if (request.session["log"] == True):
        print("yes!")
    print(request.POST["username"])
    response = HttpResponse("success")
    response.set_cookie("cookie",'Cook')
    return response
    # username = request.POST["username"]
    # password = request.POST["password"]
    # user = authenticate(username = username, password = password)
    # if user is not None:
    #     return HttpResponse("success")
    # else:
    #     return HttpResponse("failure")