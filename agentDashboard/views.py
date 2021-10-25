from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import datetime
#Database Models from other Apps
from account.models import regUsers, credentials, Verification
from clientDashboard.models import bookingDetails, bookingAccount, vehicles, driverDetails
#Importing request and json
import requests, json
#Cloudinary Import Libraries
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Create your views here.

@login_required(login_url='/account/login')
def agBkgDet(request):

    fname = None
    
    uid = credentials.objects.get(username=request.user.username).id
    uidTwo = regUsers.objects.get(id=uid)
    fname = uidTwo.first_name

    bkgDet = bookingDetails.objects.all().order_by('-start_date')


    #Pagination-Code
    paginator = Paginator(bkgDet, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    iploc = ' {}'.format(request.ipinfo.city)

    return render(request, 'agBkgDet.html', { 
        'iploc' : iploc, 'bkgDet' : bkgDet, 'page_obj' : page_obj , 'fname' : fname
        })


@login_required(login_url='/account/login')
def addcar(request):

    fname = None

    uid = credentials.objects.get(username=request.user.username).id
    uidTwo = regUsers.objects.get(id=uid)
    fname = uidTwo.first_name

    if request.method == "POST":
        carname = request.POST.get("brandName")
        modelname = request.POST.get("modelName")    
        rcno = request.POST.get("rcNumber")
        pkc = request.POST.get("perKmsCost")
        feat = request.POST.get("feat")
        trans = request.POST.get('transmission')
        fuel = request.POST.get('fuelType')
        mink = request.POST.get("minKM")
        feeAftrFreKM = request.POST.get("priceAftrFreeKM")
        seat = request.POST.get("seatcap")

        r = cloudinary.uploader.upload(request.FILES.get("carImg"), folder = "Car_Rental/cars/")
        img_url = r["secure_url"]
    

        cardet = vehicles(
            brandName=carname, modelName=modelname, rcNumber=rcno, perKmsCost=pkc, features=feat, transmission=trans, fuelType=fuel, minKMS=mink, aftrKmPrice=feeAftrFreKM, seatingCapacity=seat, carImg=img_url
        )
        cardet.save()

        print(modelname + " Car Added Successfully!!")



    iploc = ' {}'.format(request.ipinfo.city)

    return render(request, 'addcar.html', {
        'iploc' : iploc, 'fname' : fname
    })


@login_required(login_url='/account/login')
def adddriver(request):

    fname = None

    uid = credentials.objects.get(username=request.user.username).id
    uidTwo = regUsers.objects.get(id=uid)
    fname = uidTwo.first_name

    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        cno = request.POST.get("cno")
        lcNumber = request.POST.get("lcNumber")
        lcExp = request.POST.get("lcExp")

        driverDetails(first_name=fname, last_name=lname, email=email, contactno=cno, licenseNumber=lcNumber, licenseExpiry=lcExp).save()


        print(fname + " " + lname + " Driver Details Added Successfully")

    iploc = ' {}'.format(request.ipinfo.city)


    return render(request, 'adddriver.html', {
        'iploc' : iploc, 'fname' : fname
    })