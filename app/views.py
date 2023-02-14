from django.shortcuts import render
from app.forms import *
from app.models import *
from django.http import HttpResponse
from django.core.mail import send_mail
# Create your views here.
def home(request):
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
            send_mail('registartion','Thank you for registration','',[UFO.email],fail_silently=False)
            return HttpResponse('registartion is succesfully done')
            
        
    return render(request,'registration.html',d)    
        
    