from django.urls import path, include

from . import views

urlpatterns = [
    path('login', views.login_view, name="login"),
    path('register', views.register, name="register"),
    path("verify/<str:code>/", views.verify, name="verif"),
    path("change_password", views.change_password, name="change_password"),
    path("update_password/<str:code>/", views.update_password, name="update_password"),
    path("logout", views.logout_view, name="logout"),
    path("delete", views.delete_account, name="delete"),
    path('checkUsername', views.checkUsername, name="checkUsername"),
    path('checkEmailID', views.checkEmailID, name="checkEmailID"),
    path('cpCheckEmail', views.cpCheckEmail, name="cpCheckEmail"),
]