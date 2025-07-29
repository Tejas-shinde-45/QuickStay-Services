from django.urls import path
from Quickstayapp import views
urlpatterns=[
    path('',views.index,name='index'),
    path('login/',views.login_page,name='login'),
    path('register/',views.register_page,name='register'),
    path('hotel_details/<slug>/', views.hotel_details, name="hotel_details"),
]