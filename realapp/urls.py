from django.urls import path
from realapp import views
app_name = 'realapp'
urlpatterns = [
    path('registration/basic/', views.reg_basic, name='registration_basic'),
    path('registration/email/', views.reg_email, name='registration_email'),
    path('registration/emailveri/', views.reg_emailverify, name='registration_emailverify'),
    path('registration/phone/', views.reg_phone, name='registration_phone'),
    path('registration/phoneveri/', views.reg_phoneverify, name='registration_phoneverify'),
    path('registration/photo/', views.reg_photo, name='registration_photo'),
    path('login/basic/', views.login_basic, name='login_basic'),
    path('login/email/', views.login_email, name='login_email'),
    path('login/emailveri/', views.login_emailverify, name='login_emailverify'),
    path('login/phone/', views.login_phone, name='login_phone'),
    path('login/phoneveri/', views.login_phoneverify, name='login_emailverify'),
    path('login/photo/', views.login_photo, name='login_photo'),
    path('logout/', views.logout, name="logout"),
    path('something/', views.something, name="something"),

]