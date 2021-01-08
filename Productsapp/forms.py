from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from .models import *

class ProductAddForm(ModelForm):
    class Meta:
        model=Product
        fields=['name','price','description','img'] 
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MyForm, self).__init__(*args, **kwargs)
    def save(self, commit=True):
        product = super().save(commit=False)
        if self.request.user.owner_of is None :
            raise ValidationError("Product doesn't have independent existence,create Restaurent First ")
        product.restaurent_id = self.request.user.owner_of

        if commit:
            product.save()
        return product       

class RestaurentAddForm(ModelForm):
    class Meta:
        model=Restaurent
        fields=['name','location','description','img']    
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RestaurentAddForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        restaurent = super().save(commit=False)
        #By doing this we get model object
        restaurent.owner_of = self.request.user
        if commit:
            restaurent.save()
        return restaurent

    


class ProductUpdateForm(ModelForm):

    class Meta:
        model=Product
        fields=['name','price','description','img','is_present']

class RestaurentUpdateForm(ModelForm):
     class Meta:
        model=Restaurent
        fields=['name','location','description','img']    