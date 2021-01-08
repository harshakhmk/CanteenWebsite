from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('Signup',views.GenSignup,name="Signup"),
    path('logout/',views.Logout,name="logout"),
    path('Signup/customer/',views.CustomerSignupView,name="CustomerSignup"),
    path('Signup/vendor/',views.VendorSignupView,name="VendorSignup"),
    path('login/',views.Login,name="login"),
    
    #path('profile-view/<int:user_id>',views.profile_view,name='profile-view'),
   
]
