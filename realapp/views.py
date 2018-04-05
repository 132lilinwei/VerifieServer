# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os.path
from django.core.files import File
from newsite import settings
from realapp.models import MyUser
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import base64
from django.core.mail import send_mail
import json
import paho.mqtt.client as mqtt
import random
import time
import threading
import sys
from threading import Thread
from django.utils import timezone
import datetime

# Face verification import
from realapp.photo import face_recognition
from django.contrib.gis.geoip2 import GeoIP2

NOSMS = True

SESSIONSTATUS = {
    "REG_BASICINFO" : 1 ,
    "REG_EMAIL" : 2,
    "REG_PHONE" : 3,
    "REG_PHOTO1" : 4,
    "REG_PHOTO2" : 5,
    #REG_PHOTO3 = '6',
    "LOGIN_BASICINFO" : 11,
    "LOGIN_EMAIL" : 12,
    "LOGIN_PHONE" : 13,
    "LOGIN_PHOTO" : 14,
    "LOGIN_PHOTO_VERI": 15,
    "LOGIN_DIGI" : 17,
    "LOGIN_DIGI_VERI":18,
    "LOGGEDIN" : 21
}
appres_fatal_error = "FATAL ERROR"
appres_success = "SUCCESS"
appres_too_frequent = "REQUEST TOO FREQUENT"
appres_veri_fail = "VERIFICATION FAILS"
appres_timeout = "TIME OUT"

BASE = os.path.dirname(os.path.abspath(__file__))




@csrf_exempt
def reg_basic(request):
    autoLogout(request)
    username = request.POST["username"]
    password = request.POST["password"]
    email = request.POST["email"]
    nric = request.POST["nric"]
    phone_number = request.POST["phone_number"]
    if request.session.get("status") != None:
        return HttpResponse(appres_fatal_error)

    if checkAndDel(username):
        return HttpResponse("USERNAME EXISTS")

    #else
    ip = get_client_ip(request)
    g = GeoIP2()
    info = g.city(ip)
    geolocation = str(info.get("city")) + ", " + str(info.get("country_name"))

    newUser = MyUser(username = username, password = password, email = email, nric = nric, phone_number = phone_number, geolocation=geolocation)
    newUser.save()
    request.session['status'] = SESSIONSTATUS['REG_BASICINFO']
    request.session['username'] =  username
    request.session['last_sent'] = int(timezone.now().timestamp())
    request.session['time'] = int(timezone.now().timestamp())



    #SEND EMAIL
    sendEmailSaveCode(username)
    return HttpResponse(appres_success)


@csrf_exempt
def reg_email(request):
    if autoLogout(request):
        return HttpResponse(appres_timeout)
    status = request.session.get('status')
    if status != SESSIONSTATUS['REG_BASICINFO']:
        return HttpResponse(appres_fatal_error)
    #else
    if attackDefense(request):
        return HttpResponse(appres_too_frequent)
    sendEmailSaveCode(request.session.get('username'))
    return HttpResponse(appres_success)

@csrf_exempt
def reg_emailverify(request):
    if autoLogout(request):
        return HttpResponse(appres_timeout)
    status = request.session.get('status')
    if status != SESSIONSTATUS['REG_BASICINFO']:
        return HttpResponse(appres_fatal_error)

    #else
    user = MyUser.objects.get(username=request.session.get('username'))
    if user.randomcode == request.POST["randomcode"]:
        request.session["status"] = SESSIONSTATUS["REG_EMAIL"]
        request.session["last_sent"] = int(timezone.now().timestamp())

        #auto send sms
        sendSmsSaveCode(request.session.get('username'))
        return HttpResponse(appres_success)
    else:
        return HttpResponse(appres_veri_fail)


@csrf_exempt
def reg_phone(request):
    if autoLogout(request):
        return HttpResponse(appres_timeout)
    status = request.session.get('status')
    if status != SESSIONSTATUS['REG_EMAIL']:
        return HttpResponse(appres_fatal_error)
    if (attackDefense(request)):
        return HttpResponse(appres_too_frequent)
    sendSmsSaveCode(request.session.get('username'))
    return HttpResponse(appres_success)

@csrf_exempt
def reg_phoneverify(request):
    if autoLogout(request):
        return HttpResponse(appres_timeout)
    status = request.session.get('status')
    if status != SESSIONSTATUS['REG_EMAIL']:
        return HttpResponse(appres_fatal_error)
    if NOSMS==True:
        request.session["status"] = SESSIONSTATUS["REG_PHONE"]
        return HttpResponse(appres_success)
    #else
    user = MyUser.objects.get(username=request.session.get('username'))
    if user.randomcode == request.POST["randomcode"]:
        request.session["status"] = SESSIONSTATUS["REG_PHONE"]
        return HttpResponse(appres_success)
    else:
        return HttpResponse(appres_veri_fail)


@csrf_exempt
def reg_photo(request):
    if autoLogout(request):
        return HttpResponse(appres_timeout)
    image = request.POST["image"]
    username = request.session.get("username")
    status = request.session.get("status")
    nowphoto = 0
    if status == SESSIONSTATUS["REG_PHONE"] or status == SESSIONSTATUS["REG_PHOTO1"] or status == SESSIONSTATUS["REG_PHOTO2"]:

        if status == SESSIONSTATUS["REG_PHONE"]:
            nowphoto = 1
        if status == SESSIONSTATUS["REG_PHOTO1"]:
            nowphoto = 2
        if status == SESSIONSTATUS["REG_PHOTO2"]:
            nowphoto = 3
        try:
            user = MyUser.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponse(appres_fatal_error)

        data = os.path.join(BASE, "temp/image")
        with open(data, "wb") as f:
            f.write(base64.b64decode(image))

        django_file = File(open(data, "rb"))
        if (nowphoto == 1):
            user.photo1.save(username + str(nowphoto)+".jpeg" , django_file, save=True)
            request.session["status"] = SESSIONSTATUS["REG_PHOTO1"]
            print(user.photo1)
            return HttpResponse(appres_success)
        if (nowphoto == 2):
            user.photo2.save(username + str(nowphoto)+".jpeg" , django_file, save=True)
            request.session["status"] = SESSIONSTATUS["REG_PHOTO2"]
            return HttpResponse(appres_success)
        if (nowphoto == 3):
            user.photo3.save(username + str(nowphoto)+".jpeg" , django_file, save=True)
            user = MyUser.objects.get(username=username)
            user.digicard = generateDigi()
            user.complete = True
            user.save()
            request.session.flush()
            return HttpResponse(appres_success)
    else:
        return HttpResponse(appres_fatal_error)






@csrf_exempt
def login_basic(request):
    autoLogout(request)
    username = request.POST["username"]
    password = request.POST["password"]
    if request.session.get('status') !=None:
        return HttpResponse(appres_fatal_error)

    if checkAndDel(username) == False:
        return HttpResponse("NO SUCH USER")

    user = MyUser.objects.get(username=username)
    ip = get_client_ip(request)
    g = GeoIP2()
    info = g.city(ip)
    geolocation = str(info.get("city")) + ", " + str(info.get("country_name"))
    if (geolocation != user.geolocation):
        sendEmailLocation(username=username)

    if (user.password == password):
        request.session["status"] = SESSIONSTATUS["LOGIN_BASICINFO"]
        request.session["username"] = request.POST["username"]
        request.session["last_sent"] = int(timezone.now().timestamp())
        request.session["time"] = int(timezone.now().timestamp())
        #auto send email
        sendEmailSaveCode(username)
        return HttpResponse(appres_success)
    else:
        return HttpResponse("WRONG PASSWORD")


@csrf_exempt
def login_email(request):
    if autoLogout(request):
        return HttpResponse(appres_timeout)
    if request.session.get('status') != SESSIONSTATUS['LOGIN_BASICINFO']:
        return HttpResponse(appres_fatal_error)
    if (attackDefense(request)):
        return HttpResponse(appres_too_frequent)
    sendEmailSaveCode(request.session.get('username'))
    return HttpResponse(appres_success)


@csrf_exempt
def login_emailverify(request):
    if autoLogout(request):
        return HttpResponse(appres_timeout)
    status = request.session.get('status')
    if status != SESSIONSTATUS['LOGIN_BASICINFO']:
        return HttpResponse(appres_fatal_error)

    # else
    user = MyUser.objects.get(username=request.session.get('username'))
    if user.randomcode == request.POST["randomcode"]:
        request.session["status"] = SESSIONSTATUS["LOGIN_EMAIL"]
        request.session["last_sent"] = int(timezone.now().timestamp())
        # auto send sms
        sendSmsSaveCode(request.session.get('username'))
        return HttpResponse(appres_success)
    else:
        return HttpResponse(appres_veri_fail)


@csrf_exempt
def login_phone(request):
    if autoLogout(request):
        return HttpResponse(appres_timeout)
    status = request.session.get('status')
    if status != SESSIONSTATUS['LOGIN_EMAIL']:
        return HttpResponse(appres_fatal_error)
    if (attackDefense(request)):
        return HttpResponse(appres_too_frequent)
    sendSmsSaveCode(request.session.get('username'))
    return HttpResponse(appres_success)

@csrf_exempt
def login_phoneverify(request):
    autoLogout(request)
    status = request.session.get('status')
    if status != SESSIONSTATUS['LOGIN_EMAIL']:
        return HttpResponse(appres_fatal_error)

    #else
    if NOSMS==True:
        request.session["status"] = SESSIONSTATUS["LOGIN_PHONE"]
        return HttpResponse(appres_success)

    user = MyUser.objects.get(username=request.session.get('username'))
    if user.randomcode == request.POST["randomcode"]:
        request.session["status"] = SESSIONSTATUS["LOGIN_PHONE"]
        return HttpResponse(appres_success)
    else:
        return HttpResponse(appres_veri_fail)



@csrf_exempt
def login_photo(request):
    if autoLogout(request):
        return HttpResponse(appres_timeout)
    status = request.session.get('status')
    if status != SESSIONSTATUS['LOGIN_PHONE']:
         return HttpResponse(appres_fatal_error)
    request.session["photo"] = "FAIL"
    username = request.session.get("username")
    image = request.POST["image"]
    photothread(username = username,image = image)
    user = MyUser.objects.get(username=username)
    if user.photoverify == True:
        request.session['status'] = SESSIONSTATUS["LOGIN_PHOTO"]
        user.photoverify = False
        user.save()
        digi_entry = generateDigiEntry()
        request.session["digi_entry"] = digi_entry
        return HttpResponse(appres_success+" "+digi_entry)
    else:
        request.session['status'] = SESSIONSTATUS["LOGIN_PHONE"]
        return HttpResponse(appres_veri_fail)


# @csrf_exempt
# def login_photoveri(request):
#     if autoLogout(request):
#         return HttpResponse(appres_timeout)
#     status = request.session.get('status')
#     if status != SESSIONSTATUS["LOGIN_PHOTO"]:
#          return HttpResponse(appres_fatal_error)
#     username = request.session.get("username")
#     user = MyUser.objects.get(username=username)
#     if user.photoverify == True:
#         request.session['status'] = SESSIONSTATUS["LOGIN_PHOTO_VERI"]
#         user.photoverify = False
#         user.save()
#         return HttpResponse(appres_success)
#     else:
#         request.session['status'] = SESSIONSTATUS["LOGIN_PHONE"]
#         return HttpResponse(appres_veri_fail)



# @csrf_exempt
# def digicard(request):
#     if autoLogout(request):
#         return HttpResponse(appres_timeout)
#     status = request.session.get('status')
#     if status != SESSIONSTATUS['LOGIN_PHOTO_VERI']:
#         return HttpResponse(appres_fatal_error)
#     request.session["status"] = SESSIONSTATUS["LOGIN_DIGI"]
#     digi_entry = generateDigiEntry()
#     request.session["digi_entry"] = digi_entry
#     return HttpResponse(digi_entry)

@csrf_exempt
def digicard_veri(request):
    if autoLogout(request):
        return HttpResponse(appres_timeout)
    status = request.session.get('status')
    if status != SESSIONSTATUS["LOGIN_PHOTO"]:
        return HttpResponse(appres_fatal_error)
    answer = request.POST["answer"]
    digi_entry = request.session.get('digi_entry')
    username = request.session.get("username")
    if checkDigi(digi_entry, answer, username):
        request.session["status"] = SESSIONSTATUS["LOGGEDIN"]
        return HttpResponse(appres_success)
    else:
        return HttpResponse(appres_veri_fail)






@csrf_exempt
def logout(request):
    request.session.flush()
    return HttpResponse("SUCCESSFUL LOGOUT")

@csrf_exempt
def something(request):
    if request.session.get("username") != None:
        return HttpResponse("session shows log in")
    return HttpResponse("NO SESSION")


def checkAndDel(username):
    try:
        user = MyUser.objects.get(username=username)
        if user.complete == False:
            user.delete()
            return False
        else:
            return True
    except ObjectDoesNotExist:
        return False



def generateRdm():
    randomcode = str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))
    return randomcode
def sendEmailSaveCode(username):
    thread = Thread(target=sendEmailSaveCodeHelper, args=(username,))
    thread.start()


def sendEmailSaveCodeHelper(username):
    randomcode = generateRdm()
    user = MyUser.objects.get(username=username)
    user.randomcode = randomcode
    user.save()
    send_mail(
        'New registration to Verifie',
        "The code is " + randomcode,
        'llw19970903@gmail.com',
        [user.email],
        fail_silently=False,
    )

def sendSmsSaveCode(username):
    thread = Thread(target=sendSmsSaveCodeHelper, args=(username,))
    thread.start()

def sendSmsSaveCodeHelper(username):
    if NOSMS ==True:
        return
    randomcode = generateRdm()
    user = MyUser.objects.get(username=username)
    user.randomcode = randomcode
    number = user.phone_number
    user.save()
    mqttc = mqtt.Client("client1", clean_session=False)
    mqttc.username_pw_set("jxjanbvd", "uuUlFpgEVUte")
    mqttc.connect("m23.cloudmqtt.com", 10035, 60)
    mqttc.publish("sms/henry", number+":Your KYC code is " + randomcode)

def autoLogout(request):
    last_time = request.session.get("time")
    if (last_time == None or (int(timezone.now().timestamp() - last_time) > 120) ):
        request.session.flush()
        return True
    else:
        request.session["time"] = int(timezone.now().timestamp())
        return False

def attackDefense(request):
    last_time = request.session.get("last_sent")
    print(last_time)
    print(timezone.now().timestamp())
    request.session['last_sent'] = int(timezone.now().timestamp())
    if (int(timezone.now().timestamp() - last_time) < 5):
        return True
    else:
        return False



def photothread(username, image):
    data = os.path.join(BASE, "temp/image")
    with open(data, "wb") as f:
        f.write(base64.b64decode(image))
    user = MyUser.objects.get(username=username)
    img_path = data
    # Verify the newly uploaded photo with the user model
    photo_verified = face_recognition.verify_img(img_path, user)

    if photo_verified:
        user.photoverify = True
    else:
        user.photoverify = False
    
    user.save()


def generateDigi():
    return "L41R3T6KS71QHPTPU5V82923JB7WMDZ6NUE"
def generateDigiEntry():
    result = ""
    for i in range(4):
        letter = chr(random.randint(0,6) + 65)
        num = str(random.randint(0,4))
        result = result + letter+ num + " "
    return result.strip(" ")

def checkDigi(digi_entry, answer, username):
    user = MyUser.objects.get(username=username)
    entries = str(digi_entry).split(" ")
    for i in range(len(entries)):
        position = ord(entries[i][0])-65 + (int(entries[i][1])) * 7
        print("hahahaoewifjwioefj" + str(position))
        print(digi_entry)
        print(answer)
        if (user.digicard[position] != answer[i]):
            return False
    return True

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def sendEmailLocation(username):
    thread = Thread(target=sendEmailLocationHelper, args=(username,))
    thread.start()
def sendEmailLocationHelper(username):
    user = MyUser.objects.get(username=username)
    send_mail(
        'Verifie New Log In',
        "Someone had tried to login to your account in "+ user.geolocation + ". Please confirm if this is you.",
        'llw19970903@gmail.com',
        [user.email],
        fail_silently=False,
    )



