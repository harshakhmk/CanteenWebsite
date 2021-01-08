from django.contrib import admin
from django.urls import path,include
from .views import *
from .Handleviews.vendors import *

urlpatterns = [
    path('', home, name="home"),
	path('search',search_items,name="search"),
    path('Restaurent/<int:id>/products',restaurent_product_list,name="restaurent_products"),#get list of products under this Restaaurent Id
    path('product-detail/<int:id>/',product_detail,name="product-detail"),
   
    path('add-to-cart/<int:id>',add_to_cart,name="add_to_cart"),
    path('remove-from-cart/<int:id>',remove_from_cart,name="remove_from_cart"),
    path('remove-single-item-from-cart/<int:id>/',remove_singleitem_from_cart,name="remove_singleitem_from_cart"),
    path('order-history',Order_History_List,name="order-history"),
    path('order-summary/', OrderSummaryView, name='order-summary'),
    path('complete-order/',CompleteOrder,name="complete-order"),
    path('Create_Restaurent/',Create_Restaurent,name="Create_Restaurent"),
    path('Update_Restaurent/<int:id>',Update_Restaurent,name="Update_Restaurent"),
    path('Delete_Restaurent/<int:id>',Delete_Restaurent,name="Delete_Restaurent"),
    path('Restaurent/<int:restaurent_id>/create_product',create_product,name="create_product"),
    path('Restaurent/<int:restaurent_id>/update_product/<int:product_id>/',update_product,name="update_product"),
    path('Restaurent/<int:restaurent_id>/delete_product/<int:product_id>/',delete_product,name="delete_product"),


]