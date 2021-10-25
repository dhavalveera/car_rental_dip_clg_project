from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
#Database Models from all Apps
from account.models import regUsers, credentials
from .models import bookingDetails, bookingAccount, vehicles, driverDetails

# Create your views here.


#My Profile
@login_required(login_url='/account/login')
def myprofile(request):

    uid = credentials.objects.get(username=request.user.username).id
    uidTwo = regUsers.objects.get(id=uid)
    fname = uidTwo.first_name
    email = uidTwo.email

    #credentials Table Row
    LogUserOne = credentials.objects.get(username=request.user.username).username
    #regUsers Table Row
    LogUserTwo = regUsers.objects.get(id=uid)


    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        contactno = request.POST['contactno']

        userOne = credentials.objects.get(username=request.user.username)
        userOne.username = username
        userOne.save()

        userTwo = regUsers.objects.get(id=uid)
        userTwo.first_name = fname
        userTwo.last_name = lname
        userTwo.email = email
        userTwo.contactno = contactno
        userTwo.save()

        html_message = render_to_string('accountUpdate.html', { 'fname' : fname })
        subject = 'Account Information Updated Successfully - Car Rental'
        message = ' '

        send_mail(subject, message=message, from_email='shahbhaivaniya@gmail.com', recipient_list=[email], html_message=html_message, fail_silently=False)
        messages.add_message(request, messages.SUCCESS, f'Your Account Information has been updated successfully.')
        return redirect("clientDashboard:myprofile")


    iploc = ' {}'.format(request.ipinfo.city)

    return render(request, 'myprofile.html', { 'iploc' : iploc, 'fname' : fname, 'iploc' : iploc, 'LogUserOne' : LogUserOne, 'LogUserTwo' : LogUserTwo })


#My Bookings
@login_required(login_url='/account/login')
def mybookings(request):

    uid = credentials.objects.get(username=request.user.username).id
    uidTwo = regUsers.objects.get(id=uid)
    fname = uidTwo.first_name

    bdDet = bookingDetails.objects.filter(regUser_id=uidTwo.id).order_by('-start_date')

    bdID = bookingDetails.objects.get(regUser_id=uidTwo.id).id
    baAmt = bookingAccount.objects.get(id=bdID).amount


    #Pagination-Code
    paginator = Paginator(bdDet, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)



    iploc = ' {}'.format(request.ipinfo.city)

    return render(request, 'mybookings.html', { 
        'iploc' : iploc, 'fname' : fname, 'page_obj' : page_obj, 'bdDet' : bdDet, 'baAmt' : baAmt 
        })



#Display Specific Booking Details
@login_required(login_url='/account/login')
def detmybookings(request, pk):


    uid = credentials.objects.get(username=request.user.username).id
    uidTwo = regUsers.objects.get(id=uid)
    fname = uidTwo.first_name

    bdDet = bookingDetails.objects.filter(id=pk)
    bdID = bookingDetails.objects.get(id=pk).id

    baAmt = bookingAccount.objects.get(id=bdID).amount
    batDT = bookingAccount.objects.get(id=bdID).transactionDate



    iploc = ' {}'.format(request.ipinfo.city)

    return render(request, 'detmybookings.html', { 
        'iploc' : iploc, 'fname' : fname, 'bdDet' : bdDet, 'baAmt' : baAmt, 'batDT' : batDT
        })



#Delete Profile under My Profile
@login_required(login_url='/account/login')
def delAcc(request):

    uid = credentials.objects.get(username=request.user.username).id
    uidTwo = regUsers.objects.get(id=uid)
    fname = uidTwo.first_name




    iploc = ' {}'.format(request.ipinfo.city)


    return render(request, 'delProfile.html', { 'iploc' : iploc, 'fname' : fname })