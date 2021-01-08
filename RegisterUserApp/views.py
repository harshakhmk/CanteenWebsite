from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import auth
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
from .forms import *
from .decorators import *
from django.views.generic import CreateView, ListView, UpdateView

def CustomerSignupView(request):
    if request.method=='GET':
        form=CustomerSignupForm()
        return render(request,"customersignup.html",{'form':form})
    else  :
        form=CustomerSignupForm(request.POST)
        if form.is_valid() :
            form.save()
            messages.success(request,"Your account successfully created")
            return redirect('login')   # Mention url name here  
        else :
            messages.error(request,"Invalid data")
            return redirect("CustomerSignup")

def VendorSignupView(request):
    if request.method=='POST':
        form=VendorSignupForm(request.POST)
        if form.is_valid() :
            form.save()
            messages.success(request,"Your account successfully created")
            return redirect('login')    
        else :
                 return redirect('/Signup/vendor') 
    else :
        f=VendorSignupForm()
        return render(request,"vendor_signup.html",{'form':f})



def Logout(request):

    auth.logout(request)
    return redirect("/")

def GenSignup(request):
    return render(request,"genSignup.html") 
"""
def profile_view(request,user_id,*args,**kwargs):
    
    if request.method=="POST":
        profile=get_object_or_404(request.user.id)
        
    
    elif request.METHOD=='GET':
      
     
      profile=get_object_or_404(User,id=user_id)
      context={
                 "profile":profile
            }
    return render(request,"profile-view.html",context)  
"""   
def Login(request):
    
    if request.method=='GET' :
            f=UserLoginForm()
            return render(request,"login.html",{'form':f})
    elif request.method=='POST':
            f=UserLoginForm(request.POST)
            if f.is_valid() :
               
                user=auth.authenticate(username=request.POST.get('username'),
                                      password=request.POST.get('password')        )
                if user is not None: # valid user
                   auth.login(request,user)
                   messages.success(request,"You have been Loged in")
                   return redirect("/")
                else:
                    messages.info(request,"invalid username or password")
                    return redirect("login")    
            else :
                return redirect("login")
 