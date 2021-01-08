from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required
import random
import string
from django.db import transaction
from RegisterUserApp.models import *
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.views.generic import ListView, DetailView, View

def generate_id(n=15):
   return ''.join(random.SystemRandom().choice(string.ascii_uppercase+ string.ascii_lowercase + string.digits) for _ in range(n))

def home(request):
    context={
        "list":Restaurent.objects.all()
    }
    return render(request,"restuarent_list.html",context)


#All the products under this restaurent     
def restaurent_product_list(request,id):# Working 
    R=get_object_or_404(Restaurent,id=id)
    prod=R.product_set.all()
    context={"products":prod}
    return render(request,"products_list.html",context)
    

 


def product_detail(request,id):
    objects=get_object_or_404(Product,id=id)
    context={"obj":objects}
    return render(request,"product_detail.html",context)


@login_required(login_url='/accounts/login/')
def add_to_cart(request,id):
    #get the item with this id
    # convert this to order_product object  Intermediate Model
    # Now we aren't getting items that has already been added
    product=get_object_or_404(Product,id=id)   
    order_product,created=OrderProduct.objects.get_or_create(product=product,
    user=request.user.customer,
    ordered=False
    )


   #Generate Order QS which is incomplete 
    order_qs=Order.objects.filter(user=request.user.customer,is_complete=False)
    
    
    # If Unordered order exists then proceed
    if order_qs.exists():
        order=order_qs[0]# picking the first order which is incomplete

        # Now check if user has already added this product in cart
        if order.products.filter(product__id=product.id).exists():
            order_product.quantity+=1
            order_product.save()
        else:  #new item added to cart 
            order.products.add(order_product) 

    #Not ordered before
    else:
         start_date=timezone.now()
         order=Order.objects.create(user=request.user.customer,start_date=start_date)
         order.products.add(order_product) 
    return redirect("order-summary")  

@login_required(login_url='/accounts/login')
def remove_from_cart(request,id):
   # order_product=OrderProduct.objects.create(product=item)
    #Generate user Order QS which is incomplete 
    product=get_object_or_404(Product,id=id)
    user_order_qs=Order.objects.filter(user=request.user.customer,is_complete=False)
    if user_order_qs.exists():
        order=user_order_qs[0]# picking the first order which is incomplete

        # Now check if object is in cart
        if order.products.filter(product__id=product.id).exists():
            order_product=OrderProduct.objects.filter(product=product,
                               user=request.user.customer,
                                ordered=False
                                   )[0]
            order.products.remove(order_product)
            order_product.delete() 
            return redirect("order-summary")
        else:  
           messages.info(request,"product not exists in ur cart to remove")

    #Not ordered before
    else:
        messages.info(request,"U haven't started ur first order yet")
        
    return redirect("order-summary")                               

@login_required(login_url='/accounts/login')
def remove_singleitem_from_cart(request,id):
    # order_product=OrderProduct.objects.create(product=item)
    #Generate user Order QS which is incomplete 
    product=get_object_or_404(Product,id=id) 
    user_order_qs=Order.objects.filter(user=request.user.customer,is_complete=False)
    if user_order_qs.exists():
        order=user_order_qs[0]# picking the first order which is incomplete

        # Now check if object is in cart
        if order.products.filter(product__id=product.id).exists():
            order_product=OrderProduct.objects.filter(product=product,
                               user=request.user.customer,
                                ordered=False
                                   )[0]
            if order_product.quantity>1 :
                 order_product.quantity-=1
                 order_product.save()

            else:
                order.products.remove(order_product)

            
        else:  
           messages.info(request,"product not exists in ur cart to remove")

    #Not ordered before
    else:
        messages.info(request,"U haven't started ur first order yet")
    return redirect("order-summary")     

def search_items(request):
 
  if 'search' in request.GET:
    search_term = request.GET['search']
    query_set=Product.objects.filter(name__icontains=search_term.lower())
    
  return render(request,"search.html",context={"query_set":query_set}) 
    

@login_required(login_url='/accounts/login/')
def Order_History_List(request):
    context={
        "objects":Order.objects.filter(
            user=request.user.customer,
            order_by="-transaction_date",
            is_complete=True
            
            )
            }
    return render(request,"Order_history.html",context=context)        


@login_required(login_url='accounts/login')  
def OrderSummaryView(request,*args,**kwargs):
        try :
            order=Order.objects.get(user=request.user.customer,is_complete=False)
            context = {
                'order': order
            }
            return render(request, 'order_summary.html', context)
        except ObjectDoesNotExist :
            messages.warning(request, "You do not have an active order")
            return redirect("/")

@login_required(login_url='accounts/login')
@transaction.atomic
def CompleteOrder(request):
    order=Order.objects.filter(
        user=request.user.customer,
        is_complete=False
      )[0]
    if order is not None :
       order.is_complete=True
       order.final_price=order.total_price()
       order.transaction_date=timezone.now()
       order.transaction_id=generate_id()
       order.save()
       messages.success(request,"Your Order has been Ordered")
       return redirect('/')
    else :
        messages.error(request,"You don't  have any order complete")
        return redirect("complete-order")           