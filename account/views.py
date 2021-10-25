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
#Database Models from all App
from .models import regUsers, credentials, Verification

# Create your views here.

def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            userType = user.regUser.userType
            if userType == "Agent":
                login(request, user)
                return redirect(request.GET.get("next", "agentDashboard:agBkgDet"))
            elif userType == "Customer":
                login(request, user)
                return redirect(request.GET.get("next", "clientDashboard:myprofile"))
        else:
            messages.add_message(request, messages.ERROR, f'You have entered incorrect username or password, please re-check OR your account is not verified.')
            return redirect('login')


    iploc = ' {}'.format(request.ipinfo.city)

    return render(request, 'login.html', { 'iploc':iploc })


def register(request):

    if request.user.is_authenticated:
        return redirect('carrental:index')

    if request.method == "POST":

        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        contactno = request.POST['contactno']
        username = request.POST['username']
        password = request.POST['password']

        acc_det = regUsers(first_name=fname, last_name=lname, email=email, contactno=contactno)
        acc_det_two = credentials(username=username)
        acc_det_two.set_password(password)
        acc_det.is_active = False
        acc_det.save()
        acc_det_two.regUser = acc_det
        acc_det_two.is_active = False
        acc_det_two.save()

        Verification(user_id=regUsers.objects.get(email=email).id).save()
        code = Verification.objects.get(user_id=regUsers.objects.get(email=email).id).id

        contno = str(contactno)

        html_message = render_to_string('verifyAccountTemplate.html', { 'fname' : fname, 'lname' : lname, 'code' : code })
        subject = 'Action Required : Verify your account - Car-Rental'
        message = ' '

        send_mail(subject, message=message, from_email='shahbhaivaniya@gmail.com', recipient_list=[email], html_message=html_message, fail_silently=False)
        print("Email Sent Successfully")
        messages.add_message(request, messages.SUCCESS, f'Please verify your email address.')
        return HttpResponseRedirect(reverse("register"))

    iploc = ' {}'.format(request.ipinfo.city)

    return render(request, 'register.html', { 'iploc':iploc })


def verify(request, code):

    try:
        Verification.objects.get(id=code)
    except Exception as e:
        print(e)
        messages.add_message(request, messages.ERROR, f'Verification Code Not Found!!')
        return HttpResponseRedirect(reverse('login'))

    user_id = Verification.objects.get(id=code).user_id
    Verification.objects.get(id=code).delete()
    user = regUsers.objects.get(id=user_id)
    user_two = credentials.objects.get(regUser=user_id)

    #Fetch First & Last Name
    ufname = user.first_name
    ulname = user.last_name

    #Fetch Email ID
    uemail = user.email
    user.is_active=True
    user.save()

    user_two.is_active=True
    user_two.save()

    html_message = render_to_string('accountVerified.html', { 'fname' : ufname, 'lname' : ulname })
    subject = 'Welcome to Car-Rental'
    message = ' '

    send_mail(subject, message=message, from_email='shahbhaivaniya@gmail.com', recipient_list=[uemail], html_message=html_message, fail_silently=False)
    messages.add_message(request, messages.SUCCESS, f'Account Verified Successfully, you can now login.')
    return HttpResponseRedirect(reverse('login'))



def change_password(request):


    if request.method == "POST":

        email = request.POST['email']

        Verification(user_id=regUsers.objects.get(email=email).id).save()
        code = Verification.objects.get(user_id=regUsers.objects.get(email=email).id).id
        fname = regUsers.objects.get(email=email).first_name

        html_message = render_to_string('passwordReset.html', { 'code' : code, 'fname' : fname })
        subject = 'Password Reset for your Account - Car Rental'
        message = ' '

        send_mail(subject, message=message, from_email='shahbhaivaniya@gmail.com', recipient_list=[email], html_message=html_message, fail_silently=False)
        messages.add_message(request, messages.SUCCESS, f'Password Reset link has been sent to your registered email id.')
        return HttpResponseRedirect(reverse('change_password'))


    iploc = ' {}'.format(request.ipinfo.city)

    return render(request, 'change_password.html', { 'iploc':iploc })


def update_password(request, code):

    try:
        Verification.objects.get(id=code)
    except Exception as e:
        print(e)
        messages.add_message(request, messages.ERROR, f'Invalid Code!')
        return HttpResponseRedirect(reverse('change_password'))

    if request.method == "POST":

        password = request.POST['password']

        user_id = Verification.objects.get(id=code).user_id
        Verification.objects.get(id=code).delete()
        acc_det = regUsers.objects.get(id=user_id)
        fname = acc_det.first_name
        uemail = acc_det.email
        acc_det.regUsers.set_password(password)
        acc_det.regUsers.save()

        html_message = render_to_string('passwordResetted.html', { 'fname' : fname })
        subject = 'Password Reset Successfully - Car Rental'
        message = ' '

        send_mail(subject, message=message, from_email='shahbhaivaniya@gmail.com', recipient_list=[uemail], html_message=html_message, fail_silently=False)
        messages.add_message(request, messages.SUCCESS, f'Password Changed Successfully, you can login.')
        return HttpResponseRedirect(reverse('login'))


    iploc = ' {}'.format(request.ipinfo.city)

    return render(request, 'update_password.html', { 'iploc':iploc })


def logout_view(request):

    logout(request)
    messages.add_message(request, messages.SUCCESS, f'You have been logout successfully.')
    return HttpResponseRedirect(reverse('login'))


def delete_account(request):

    uid = credentials.objects.get(username=request.user.username).id
    request.user.is_active=False
    request.user.save()
    uidTwo = regUsers.objects.get(id=uid)
    uidTwo.is_active=False
    uidTwo.save()

    ufname = uidTwo.first_name
    ulname = uidTwo.last_name
    uemail = uidTwo.email

    today = datetime.date.today()
    
    html_message = render_to_string('accountDelete.html', { 'fname' : ufname, 'lname' : ulname, 'date' : today })
    subject = 'Account has been deleted - Car Rental'
    message = ' '

    send_mail(subject, message=message, from_email='shahbhaivaniya@gmail.com', recipient_list=[uemail], html_message=html_message, fail_silently=False)

    logout(request)

    messages.add_message(request, messages.ERROR, f'Your account has been deleted successfully.')
    return HttpResponseRedirect(reverse('login'))


#Check Username for Registration Form
@csrf_exempt
def checkUsername(request):

    username = request.GET.get('username', None)

    data = {
        'is_present' : credentials.objects.filter(username__iexact=username).exists()
    }

    return JsonResponse(data)


#Check Email ID for Registration Form
@csrf_exempt
def checkEmailID(request):

    emailid = request.GET.get('email', None)

    data = {
        'is_present' : regUsers.objects.filter(email__iexact=emailid).exists()
    }

    return JsonResponse(data)


#Check Email ID for Change Password
@csrf_exempt
def cpCheckEmail(request):

    emailid = request.GET.get('email', None)

    data = {
        'is_present' : regUsers.objects.filter(email__iexact=emailid).exists()
    }

    return JsonResponse(data)