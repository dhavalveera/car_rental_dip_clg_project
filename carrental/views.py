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
from datetime import datetime
from datetime import date
import time
#Database Models from other Apps
from account.models import regUsers, credentials, Verification
from clientDashboard.models import bookingDetails, bookingAccount, vehicles, driverDetails
#Importing request and json
import requests, json
#Cloudinary Import Libraries
import cloudinary
import cloudinary.uploader
import cloudinary.api
#Importing Django Settings
from django.conf import settings
#Django-Environ
import os
import environ
#Environment Variable Configuration
env = environ.Env()
#reading .env file here
environ.Env.read_env()
#Importing Connection
from django.db import connection
#Importing Stripe
import stripe
#Importing xhtml2pdf to create PDF
from xhtml2pdf import pisa
from io import BytesIO


stripe.api_key = env("STRIPE_PRIVATE_KEY")


# Create your views here.

#Home-Page
def index(request):

    fname = None

    if request.user.is_authenticated:
        uid = credentials.objects.get(username=request.user.username).id
        uidTwo = regUsers.objects.get(id=uid)
        fname = uidTwo.first_name

    carDetails = vehicles.objects.all()

    if request.method == "POST":
        src = request.POST['source']
        dest = request.POST['destination']
        sdoj = request.POST['sdoj']
        edoj = request.POST['edoj']

        print(sdoj)

        #Geocoding API of here.com
        apikey = env("HEREAPI")
        URL = "https://geocode.search.hereapi.com/v1/geocode"
        #Geocoding Query for Source Location
        PARAMS = {'apikey':apikey,'q':src}
        r = requests.get(url = URL, params = PARAMS) 
        data = r.json()
        Loc1latitude = str(data['items'][0]['position']['lat'])
        Loc1longitude = str(data['items'][0]['position']['lng'])
        orig = Loc1longitude+","+Loc1latitude

        #Geocoding Query for Destination Location
        PARAMS = {'apikey':apikey,'q':dest}
        r1 = requests.get(url = URL, params = PARAMS) 
        data = r1.json()
        Loc2latitude = str(data['items'][0]['position']['lat'])
        Loc2longitude = str(data['items'][0]['position']['lng'])
        desti = Loc2longitude+","+Loc2latitude

        #Distance Matrix API of mapbox.com
        URLMain = "https://api.mapbox.com/directions-matrix/v1/mapbox/driving/"
        URL1 = "?access_token="+env("MAPBOXAPI")
        URL2 = "&sources=0&destinations=1&annotations=duration,distance"
        full_url = URLMain+orig+";"+desti+URL1+URL2

        output = requests.get(full_url).json()
        mtr = output['distances'][0][0]
        km = int(mtr / 1000)
        print("KM : ", km)

        seconds = output['durations'][0][0]

        dura = time.strftime("%H:%M", time.gmtime(seconds))
        print(dura, "Hours")

        request.session['srcLocation'] = src
        request.session['destLocation'] = dest
        request.session['stdt'] = sdoj
        request.session['eddt'] = edoj
        request.session['kms'] = km
        request.session['time'] = dura

        return HttpResponseRedirect('searchcar')





    iploc = ' {}'.format(request.ipinfo.city)


    return render(request, 'index.html', {
        'iploc' : iploc, 'fname' : fname, 'carDetails' : carDetails
    })


def viewcar(request, mdl):

    fname = None

    if request.user.is_authenticated:
        uid = credentials.objects.get(username=request.user.username).id
        uidTwo = regUsers.objects.get(id=uid)
        fname = uidTwo.first_name


    cars = vehicles.objects.get(modelName=mdl)


    iploc = ' {}'.format(request.ipinfo.city)


    return render(request, 'viewcar.html', {
        'iploc' : iploc, 'fname' : fname, 'cars' : cars, 'mdl' : mdl
    })



def search_car(request):

    fname = None

    if request.user.is_authenticated:
        uid = credentials.objects.get(username=request.user.username).id
        uidTwo = regUsers.objects.get(id=uid)
        fname = uidTwo.first_name

    src = request.session.get("srcLocation")
    des = request.session.get("destLocation")
    sdt = request.session.get("stdt")
    edt = request.session.get("eddt")
    km = request.session.get("kms")
    dur = request.session.get("time")

    sdtform = datetime.strptime(sdt, '%d-%m-%Y').strftime('%Y-%m-%d')
    edtform = datetime.strptime(edt, '%d-%m-%Y').strftime('%Y-%m-%d')

    sdtformOne = datetime.strptime(sdt, '%d-%m-%Y').strftime('%d-%b-%Y')
    edtformOne = datetime.strptime(edt, '%d-%m-%Y').strftime('%d-%b-%Y')

    # row = bookingDetails.objects.raw('''SELECT * FROM vehicles WHERE ID NOT IN (SELECT vehicles_id from bookingDetails WHERE (sdt BETWEEN start_date AND end_date) OR (edt BETWEEN start_date AND end_date))''')
    # print(row)

    # with connection.cursor() as cursor:
    #     cursor.execute('''SELECT * FROM vehicles WHERE id NOT IN (SELECT vehicles_id from bookingDetails WHERE ({sdt} BETWEEN start_date AND end_date) OR ({edt} BETWEEN start_date AND end_date).format(sdt=sdt, edt=edt))''')
    #     row = cursor.fetchall()

    row = vehicles.objects.exclude(bdvechicles__start_date__lt=sdtform, bdvechicles__end_date__gt=edtform).exclude(bdvechicles__start_date__lt=sdtform, bdvechicles__end_date__gt=edtform)


    iploc = ' {}'.format(request.ipinfo.city)
    

    return render(request, 'search_car.html', {
        'iploc' : iploc, 'fname' : fname, 'src' : src, 'des' : des, 'sdt' : sdtformOne, 'edt' : edtformOne, 'km' : km, 'dur' : dur, 'row' : row
    })


@login_required(login_url='/account/login')
def checkout(request, mdl):

    fname = None

    if request.user.is_authenticated:
        uid = credentials.objects.get(username=request.user.username).id
        uidTwo = regUsers.objects.get(id=uid)
        fname = uidTwo.first_name

    cars = vehicles.objects.get(modelName=mdl)

    src = request.session.get("srcLocation")
    des = request.session.get("destLocation")
    sdt = request.session.get("stdt")
    edt = request.session.get("eddt")
    km = request.session.get("kms")
    dur = request.session.get("time")


    sdtform = datetime.strptime(sdt, '%d-%m-%Y').strftime('%Y-%m-%d')
    edtform = datetime.strptime(edt, '%d-%m-%Y').strftime('%Y-%m-%d')

    sdtformOne = datetime.strptime(sdt, '%d-%m-%Y').strftime('%d-%b-%Y')
    edtformOne = datetime.strptime(edt, '%d-%m-%Y').strftime('%d-%b-%Y')

    date_format = "%d-%m-%Y"
    a = datetime.strptime(sdt, date_format)
    b = datetime.strptime(edt, date_format)

    delta = b - a
    totalDays = delta.days
    
    dpd = 400

    tax_amount = cars.perKmsCost * .18
    total_amount = cars.perKmsCost * totalDays + tax_amount + dpd


    request.session['totalDays'] = totalDays
    request.session['dpd'] = dpd
    request.session['tax_amount'] = tax_amount
    request.session['total'] = total_amount
    request.session['brndName'] = cars.brandName
    request.session['mdlName'] = cars.modelName

    fullName = cars.brandName + " " + mdl + " " + "Car Booking"

    # bd = bookingDetails.objects.get(source=src).id

    # ba = bookingAccount.objects.get(id=bd)
    # dt = ba.transactionDate

    # ttype = ba.transactionType

    sdtform = datetime.strptime(sdt, '%d-%m-%Y').strftime('%Y-%m-%d')
    edtform = datetime.strptime(edt, '%d-%m-%Y').strftime('%Y-%m-%d')


    transacType = "Cash"

    ddDet = driverDetails.objects.get(id=1)

    bd = bookingDetails(regUser=uidTwo, start_date=sdtform, end_date=edtform, approxKMS=km, source=src, destination=des,driver_id=ddDet, vehicles_id=cars)
    bd.save()


    ba = bookingAccount(bookingDetails_id=bd, transactionType=transacType, amount=total_amount)
    ba.save()

    bd = bookingDetails.objects.get(source=src).id


    html_message = render_to_string('bookingConfirmation.html', { 'fname' : fname, 'fullName' : fullName, 'total_amount' : total_amount, 'id' : bd })
    subject = 'Thank You for Booking - Car Rental'
    message = ' '

    email = uidTwo.email

    send_mail(subject, message=message, from_email='shahbhaivaniya@gmail.com', recipient_list=[email], html_message=html_message, fail_silently=False)
    print("Email Sent Successfully")



    iploc = ' {}'.format(request.ipinfo.city)


    return render(request, 'checkout.html', {
        'iploc' : iploc, 'fname' : fname, 'cars' : cars, 'src' : src, 'des' : des, 'sdt' : sdtformOne, 'edt' : edtformOne, 'km' : km, 'dur' : dur, 'days' : totalDays, 'dpd' : dpd, 'tax_amount' : tax_amount, 'total_amount' : total_amount
    })



@login_required(login_url='/account/login')
def thankyou(request):

    fname = None

    if request.user.is_authenticated:
        uid = credentials.objects.get(username=request.user.username).id
        uidTwo = regUsers.objects.get(id=uid)
        fname = uidTwo.first_name

    src = request.session.get("srcLocation")
    des = request.session.get("destLocation")
    sdt = request.session.get("stdt")
    edt = request.session.get("eddt")
    km = request.session.get("kms")
    dur = request.session.get("time")
    totalDays = request.session.get("totalDays")
    dpd = request.session.get("dpd")
    tax_amount = request.session.get("tax_amount")
    total = request.session.get("total")
    mdlName = request.session.get("mdlName")

    cars = vehicles.objects.get(modelName=mdlName)
    brndName = cars.brandName

    fullName = brndName + " " + mdlName + " " + "Car Booking"

    bd = bookingDetails.objects.get(source=src).id

    ba = bookingAccount.objects.get(id=bd)
    dt = ba.transactionDate

    ttype = ba.transactionType


    
    iploc = ' {}'.format(request.ipinfo.city)

    return render(request, 'thankyou.html', {
        'iploc' : iploc, 'fname' : fname, 'src' : src, 'des' : des, 'sdt' : sdt, 'edt' : edt, 'km' : km, 'dur' : dur, 'totalDays' : totalDays, 'dpd' : dpd, 'tax_amount' : tax_amount, 'total' : total, 'brndName' : brndName, 'mdlName' : mdlName, 'bd' : bd, 'dt' : dt, 'ttype' : ttype, 'cars' : cars, 'fullName' : fullName
    })



#About-Us-Page
def about_us(request):

    fname = None

    if request.user.is_authenticated:
        uid = credentials.objects.get(username=request.user.username).id
        uidTwo = regUsers.objects.get(id=uid)
        fname = uidTwo.first_name

    print(fname)
    iploc = ' {}'.format(request.ipinfo.city)

    return render(request, 'about.html', {
        'iploc' : iploc, 'fname' : fname,
    })


#Gallery-Page
def gallery(request):

    fname = None

    if request.user.is_authenticated:
        uid = credentials.objects.get(username=request.user.username).id
        uidTwo = regUsers.objects.get(id=uid)
        fname = uidTwo.first_name

    carDetails = vehicles.objects.all()

    iploc = ' {}'.format(request.ipinfo.city)

    return render(request, 'gallery.html', {
        'iploc' : iploc, 'fname' : fname, 'carDetails' : carDetails,
    })


#Testimonials-Page
def testimonials(request):

    fname = None

    if request.user.is_authenticated:
        uid = credentials.objects.get(username=request.user.username).id
        uidTwo = regUsers.objects.get(id=uid)
        fname = uidTwo.first_name

    iploc = ' {}'.format(request.ipinfo.city)

    return render(request, 'testimonials.html', {
        'iploc' : iploc, 'fname' : fname,
    })


#Frequently-Asked-Question-Page
def faq(request):

    fname = None

    if request.user.is_authenticated:
        uid = credentials.objects.get(username=request.user.username).id
        uidTwo = regUsers.objects.get(id=uid)
        fname = uidTwo.first_name

    iploc = ' {}'.format(request.ipinfo.city)

    return render(request, 'faq.html', {
        'iploc' : iploc, 'fname' : fname,
    })


#Terms-&-Conditions-Page
def tc(request):

    fname = None

    if request.user.is_authenticated:
        uid = credentials.objects.get(username=request.user.username).id
        uidTwo = regUsers.objects.get(id=uid)
        fname = uidTwo.first_name

    iploc = ' {}'.format(request.ipinfo.city)

    return render(request, 'tc.html', {
        'iploc' : iploc, 'fname' : fname,
    })


#Privacy-Policy-Page
def pp(request):

    fname = None

    if request.user.is_authenticated:
        uid = credentials.objects.get(username=request.user.username).id
        uidTwo = regUsers.objects.get(id=uid)
        fname = uidTwo.first_name

    iploc = ' {}'.format(request.ipinfo.city)

    return render(request, 'pp.html', {
        'iploc' : iploc, 'fname' : fname,
    })


#Contact-Us-Page
def contact(request):

    fname = None

    if request.user.is_authenticated:
        uid = credentials.objects.get(username=request.user.username).id
        uidTwo = regUsers.objects.get(id=uid)
        fname = uidTwo.first_name


    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        cno = request.POST.get("cno")
        sub = request.POST.get("sub")
        msg = request.POST.get("msg")

        recipient = ['carrentalclgproject@gmail.com']
        ctno = str(cno)

        send_mail(
            sub + " - Car Rental",
            "Full Name = " + name + "\n\n" + "Email ID = " + email + "\n\n" + "Contact Number" + ctno + "\n\n" + "Message : " + msg,
            email,
            recipient,
            fail_silently = False
        )

        html_message = render_to_string('contact-us-temp.html', { 'name' : name })
        subject = 'Thank You for Contacting Us - Car Rental'
        message = ' '

        send_mail(subject, message=message, from_email='carrentalclgproject@gmail.com', recipient_list=[email], html_message=html_message, fail_silently=False)
        
        print("Mail Sent!!")

    iploc = ' {}'.format(request.ipinfo.city)

    return render(request, 'contact.html', {
        'iploc' : iploc, 'fname' : fname,
    })
