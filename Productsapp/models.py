from django.db import models
from  RegisterUserApp.models import User,Customer
import datetime
from django.shortcuts import reverse
# Create your models here.
class Restaurent(models.Model):
    name=models.TextField(blank=False,null=False,default="",max_length=40)
    description=models.TextField(default="",null=True,blank=True,max_length=200)
    img=models.ImageField(null=True,blank=True)
    is_present=models.BooleanField(default=False,null=True,blank=False)
    location=models.TextField(blank=False,null=False,default="",max_length=40,db_index=True)
    owner_of=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
       return  reverse("restaurent_products", kwargs={
           "id":self.id
       })   

class ProductCategory(models.Model):
    title=models.TextField(max_length=255,null=True,blank=True)
    def __str__(self):
        return self.title

class Product(models.Model):
    name=models.TextField(blank=True,null=True,max_length=20)
    price=models.FloatField()
    restaurent_id=models.ForeignKey(Restaurent,on_delete=models.CASCADE)
    description=models.TextField(default="",null=True,blank=True,max_length=200)
    is_present=models.BooleanField(default=False,null=True,blank=False)
    img=models.ImageField(null=True,blank=True)
    category=models.ForeignKey(ProductCategory, null=True,blank=True, on_delete=models.SET_NULL)
    def __str__(self):
        return f"{self.name} in {self.restaurent_id.name} "
    def get_absolute_url(self):
       return  reverse("product-detail", kwargs={
           "id":self.id
       })       

    def get_add_to_cart_url(self):
        return  reverse("add_to_cart", kwargs={
           "id":self.id
       })  
    def get_remove_from_cart_url(self):
        return  reverse("remove_from_cart", kwargs={
           "id":self.id
       }) 
    def get_remove_singleitem_from_cart_url(self):
        return reverse("remove_singleitem_from_cart",kwargs={'id':self.id})    
    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url           

class OrderProduct(models.Model):
    quantity=models.PositiveIntegerField(blank=True,null=True,default=1)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(Customer,on_delete=models.CASCADE)
    date_added=models.DateTimeField(auto_now_add=True)
    ordered=models.BooleanField(default=False,null=True,blank=True)
    def __str__(self):
        return f"{self.quantity} by {self.user.user.username}"
    def get_total_item_price(self):
        return self.quantity * self.product.price    
    
class Order(models.Model):
     user=models.ForeignKey(Customer,on_delete=models.CASCADE)
     transaction_date=models.DateTimeField(auto_now_add=True)
     is_complete=models.BooleanField(default=False,null=True,blank=False)
     transaction_id=models.CharField(default=" ",max_length=60,null=False,blank=True,unique_for_year=True)
     products=models.ManyToManyField(OrderProduct)
     start_date=models.DateTimeField(auto_now_add=True)
     final_price=models.IntegerField(default=0,blank=True)
     class Meta:
         ordering=['-start_date']


     
     @property
     def get_order_history(self):
         return reverse("order-history",kwargs={
             "id":self.id
         }) 
     def total_items_count(self):
         count=0
         for item in self.products.all() :
             count+=1
         return count        
     def total_price(self):
        total=0
        for item in self.products.all() :
           total+=item.get_total_item_price()
        return total 
    

class ShippingAddress(models.Model):
    user=models.ForeignKey(Customer,on_delete=models.CASCADE)
    order_id=models.ForeignKey(Order,on_delete=models.CASCADE)
    address=models.TextField(default="",null=True,blank=True,max_length=200)
    phone_no=models.CharField(max_length=13,null=True,blank=True)
    date_shipped=models.DateTimeField(auto_now_add=True)


"""
class OrderRecommendations(models.Model):
    user=models.ForeignKey(Customer,on_delete=models.CASCADE)
    order_id=models.ForeignKey(Order,on_delete=models.CASCADE)
    ordered_products=models.ForeignKey(OrderProduct,on_delete=models.CASCADE)
"""    