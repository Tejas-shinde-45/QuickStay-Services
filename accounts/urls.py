# from django.urls import path
# from accounts import views
# urlpatterns=[
#     path('login/',views.login_page,name='login'),
#     path('register/',views.register_page,name='register'),

#     path('verify-account/<token>/', views.verify_email_token, name="verify_email_token"),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout_view'),

    path('loginvender/', views.login_venders, name='loginvender'),
    path('registervender/',views.register_venders,name='registervender'),
    path('vdashboard/',views.dashboard,name='dashboard'),

    path('add_hotel/',views.add_hotel,name='add_hotel'),
    path('upload/<slug>/',views.upload_images,name='upload_images'),
    path('delete_image/<id>/' , views.delete_image, name="delete_image"),

    path('edit_hotel/<slug>/', views.edit_hotel , name="edit_hotel"),
    path('delete_hotel/<id>/',views.delete_hotel,name="delete_hotel")


]
