from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission
from django.db.models.signals import pre_save,post_delete,post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from django.shortcuts import reverse
# Create your models here.


#This model is for Vendors
class User(AbstractUser):
  
  bio=models.TextField(default='',null=True,blank=True,max_length=200)
  
  is_customer=models.BooleanField(default=False,null=False,blank=False)
  is_vendor=models.BooleanField(default=False,blank=False,null=False)
  
  def __str__(self):
    return self.username
  def login(self):
    return reverse('login')
  def logout(self):
    return reverse('logout')  
  def vendor_absolute_url(self):
      return reverse("profile-view",
      kwargs={
        "id":self.id
      }
      )     

class Customer(models.Model):
  user=models.OneToOneField(User,on_delete=models.CASCADE)
  bio=models.TextField(default='',null=True,blank=True)
  
  def validate_email(self):
    return self.user.email.startswith("@student.nitw.ac.in")

  def customer_absolute_url(self):
      return reverse("profile-view",
      kwargs={
        "id":self.id
      }
      )      

  def __str__(self):
    return self.user.username
