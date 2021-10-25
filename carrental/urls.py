from django.urls import path, include

from . import views

app_name = 'carrental'

urlpatterns = [
    path('', views.index, name='index'),
    path('viewcar/<str:mdl>', views.viewcar, name='viewcar'),
    path('searchcar', views.search_car, name='searchcar'),
    path('checkout/<str:mdl>', views.checkout, name='checkout'),
    path('thankyou', views.thankyou, name='thankyou'),
    path('about', views.about_us, name='about'),
    path('gallery', views.gallery, name='gallery'),
    path('testimonials', views.testimonials, name='testimonials'),
    path('faq', views.faq, name='faq'),
    path('terms-conditions', views.tc, name='terms-conditions'),
    path('privacy-policy', views.pp, name='privacy-policy'),
    path('contactus', views.contact, name='contactus'),
]