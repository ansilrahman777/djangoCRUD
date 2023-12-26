from django.urls import path
from app import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('login',views.handlelogin,name='handlelogin'),
    path('logout',views.handlelogout,name='handlelogout'),
    path('signup',views.handlesignup,name='handlesignup'),
    path('adminlogin',views.handleadminlogin,name='handleadminlogin'),
    path('adminlogout',views.handleadminlogout,name='handleadminlogout'),
    path('adminview',views.handleadminview,name='handleadminview'),
    path('insert',views.insertdata,name='insertdata'),
    path('update/<id>/',views.updatedata,name='updatedata'),
    path('deleteconfirm/<id>/', views.deleteconfirm, name='deleteconfirm'),
    path('deletedata/<id>/',views.deletedata,name='deletedata'),

]
