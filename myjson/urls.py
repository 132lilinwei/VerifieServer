from django.urls import path
from myjson import views


app_name = 'myjson'
urlpatterns = [
    path('', views.myjson, name='myjson'),

]