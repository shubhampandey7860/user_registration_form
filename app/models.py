from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Profile(models.Model):
    profile_user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='image')
    address = models.TextField()
    
    
    