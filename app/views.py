from django.shortcuts import render
from app.forms import *
from app.models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.
def home(request):
    if request.session.get('username'):
        username = request.session['username']
        d={'username' :username}
        return render(request,'home.html',d)
    return render(request,'home.html')

def registration(request):
    uf = UserForm()
    Pf = ProfileForm()
    d={'user':uf,'profile':Pf}
    if request.method=='POST' and request.FILES:
        UFD = UserForm(request.POST)
        PFD = ProfileForm(request.POST,request.FILES)
        if UFD.is_valid() and PFD.is_valid():
            UFO=UFD.save(commit=False)
            pwd = UFD.cleaned_data['password']
            UFO.set_password(pwd)
            UFO.save()
            
            PFO = PFD.save(commit=False)
            PFO.profile_user = UFO
            PFO.save()
            print(UFO.email)
            send_mail('registartion','Thank you for registration','shubhampan7860@gmail.com',[UFO.email],fail_silently=False)
            return HttpResponse('registration is succesfully done')
            
        
    return render(request,'registration.html',d)    

def Login(request):
    if request.method=="POST":
        username = request.POST['un']
        password = request.POST['pwd']
        # authentication and authorization
        user = authenticate(username = username,password=password)
        if user and user.is_active:
            login(request,user)
            request.session['username'] = username
            return HttpResponseRedirect(reverse('home')) 
        else:
            return HttpResponse('You are authenticated user')
    return render(request,'login.html')    
        
@login_required         
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def profile_display(request): 
    un=request.session.get('username')
    UO=User.objects.get(username=un)
    PO=Profile.objects.get(profile_user=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'profile_display.html',d)

@login_required
def change_password(request):
    if request.method=='POST':
        pw = request.POST['password']
        user = request.session.get('username')
        uo = User.objects.get(username=user)
        uo.set_password(pw)
        uo.save()
        return HttpResponse('password changed successfully')
    return render(request,'change_password.html')    
def reset_password(request):
    if request.method=='POST':
        un=request.POST['un']
        pw=request.POST['pw']

        LUO=User.objects.filter(username=un)

        if LUO:
            UO=LUO[0]
            UO.set_password(pw)
            UO.save()
            return HttpResponse('password reset is done')
        else:
            return HttpResponse('user is not present in my DB')
    return render(request,'reset.html')    
        
                