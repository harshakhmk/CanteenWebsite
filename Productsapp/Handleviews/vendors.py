from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from   RegisterUserApp.decorators import *
from ..models import *
from ..forms import *
from RegisterUserApp.models import *
from django.forms.utils import ValidationError

def is_owner(request,id):
   restaurent=Restaurent.objects.get(id=id)
   
   return  request.user==restaurent.owner_of

@login_required(login_url="/accounts/login")
@vendor_required
def create_product(request,restaurent_id):
    if request.method=="GET" :
       form=ProductAddForm()  
       return render(request,"create_product.html",{'form':form})
    else:  # For now nly post request
       if  is_owner(request,restaurent_id):
         form_data=ProductAddForm(request.POST or None,request=request)
         if form_data.is_valid():
            form_data.save()
            messages.info(request,"Succesfully created")
            # Going to rest products list
            return redirect("restaurent_products",kwargs={'id':restaurent_id})
         else :  # Not valid form
             messages.info(request," Something error occured while creating pls try again")
             return redirect("create_product",kwargs={'restaurent_id':restaurent_id})
       else :
           messages.info(request,"You are not allowed to create product in this restaurent")
           return redirect('/')


        
   
@login_required(login_url="/accounts/login")  
@vendor_required
def delete_product(request,restaurent_id,product_id):
    prod=Product.objects.get(id=product_id)
    if prod.restaurent_id.owner_of==request.user :
       prod.is_present=False
       messages.success("The product is successfully deleted")
       prod.delete()
       return redirect("restaurent_products",kwargs={'id':restaurent_id})
    else :
       messages.info(request,"You are not allowed to modify here")    
       return redirect('/')   

@login_required(login_url="/accounts/login")  
@vendor_required
def update_product(request,restaurent_id,product_id):
    
   if request.method=="POST":
      prod=Product.objects.get(id=product_id)
      if prod.restaurent_id.owner_of==request.user :

       form_data=ProductUpdateForm(request.POST or None ,instance=prod)
       if form_data.is_valid() :
          form_data.save()
          messages.info(request,"The product is successfully Updated")
          return redirect("restaurent_products",kwargs={'id':restaurent_id})
       else : #Not valid form, so redirecting to same page
          return redirect("update_product",
          kwargs={
           'restaurent_id':restaurent_id,
            'product_id':product_id 
          }
          )       
      else :
          messages.warning("You aren't allowed to modify here")
          return redirect("/")
   else:
      form=ProductUpdateForm()
      return render(request,"Product.html",{'form':form})


@login_required(login_url="/accounts/login")  
@vendor_required
def Create_Restaurent(request,**kwargs):
   if request.method=="POST":
      form=RestaurentAddForm(request.POST , request=request )
      if form.is_valid():
        form.save()
        messages.info(request,"The Restaurent is successfully Created")
      else : # Not valid form
        messages.info(request,"Fill the deatils properly")   
      return redirect('/')   

   elif request.method=="GET" :
    form= RestaurentAddForm()
    return render(request,"Restaurent.html",{'form':form})


@login_required(login_url="/accounts/login")  
@vendor_required
def Update_Restaurent(request,id):
 restaurent=get_object_or_404(Restaurent,id=id)
 if request.method=="POST":
   if request.user==restaurent.owner_of :
        form=RestaurentUpdateForm(request.POST ,instance=restaurent)
        if form.is_valid():
           form.save()
           messages.info(request,"Successfully updated")

        else :
           messages.info(request,"Not updatable right now try again later")   
   else :
      messages.info(request,"Not updatable right You don't have access rights")
   return redirect('/')
 elif request.method=="GET" :
    form= RestaurentUpdateForm()
    return render(request,"Restaurent.html",{'form':form})    

@login_required(login_url="/accounts/login")  
@vendor_required
def Delete_Restaurent(request,id):
   if is_owner(request,id) :
      restaurent=Restaurent.objects.get(id=id)
      messages.info(request," allowed ")

      restaurent.delete()
   else :
      messages.info(request,"You don't have access rights, not allowed ")
   return redirect('/')      
