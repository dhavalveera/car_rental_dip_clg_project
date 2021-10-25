from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'clientDashboard'

urlpatterns = [
    path('myprofile', views.myprofile, name="myprofile"),
    path('mybookings', views.mybookings, name="mybookings"),
    path('detmybookings/<int:pk>', views.detmybookings, name="detmybookings"),
    path('delAcc', views.delAcc, name="delAcc"),
]