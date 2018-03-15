from django.urls import path
from login import views

app_name = 'login'
urlpatterns = [
    path('', views.login, name='login'),
    path('onlogin/', views.on_login, name ='on_login'),

]
