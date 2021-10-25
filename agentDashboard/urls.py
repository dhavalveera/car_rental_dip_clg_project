from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'agentDashboard'

urlpatterns = [
    path('agBkgDet', views.agBkgDet, name="agBkgDet"),
    path('addcar', views.addcar, name="addcar"),
    path('adddriver', views.adddriver, name="adddriver"),
]