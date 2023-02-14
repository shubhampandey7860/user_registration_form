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
            return HttpResponse('registartion is succesfully done')
            
        
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
            
      