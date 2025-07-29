from django.db import models
from django.contrib.auth.models import User

# class HotelUser(User):
#     profile_picture = models.ImageField(upload_to="profile")
#     phone_number =  models.CharField(unique = True , max_length= 10)
#     email_token = models.CharField(max_length = 100 ,null = True , blank=True)
#     otp = models.CharField(max_length = 10 , null = True , blank = True)
#     is_verified = models.BooleanField(default = False)

# class HotelVendor(User):
#     phone_number =  models.CharField(unique = True, max_length= 90)
#     profile_picture = models.ImageField(upload_to="profile")
#     email_token = models.CharField(max_length = 100 ,null = True , blank=True)
#     otp = models.CharField(max_length = 10 , null = True , blank = True)
#     is_verified = models.BooleanField(default = False)

class HotelUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    profile_picture = models.ImageField(upload_to='profile/', blank=True)

    def __str__(self):
        return self.user.username

class HotelVendor(models.Model):
    business_name = models.CharField(max_length = 100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    profile_picture = models.ImageField(upload_to='profile/', blank=True)

    def __str__(self):
        return self.user.username

class Ameneties(models.Model):
    name = models.CharField(max_length = 100)
    icon = models.ImageField(upload_to="hotels")

class Hotel(models.Model):
    hotel_name  = models.CharField(max_length = 100)
    hotel_description = models.TextField()
    hotel_slug = models.SlugField(max_length = 90 , unique  = True)
    hotel_owner = models.ForeignKey(HotelVendor, on_delete = models.CASCADE , related_name = "hotels")
    ameneties = models.ManyToManyField(Ameneties)
    hotel_price = models.FloatField()
    hotel_offer_price = models.FloatField()
    hotel_location = models.TextField()
    is_active = models.BooleanField(default = True)


class HotelImages(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete = models.CASCADE , related_name = "hotel_images")
    image = models.ImageField(upload_to="hotels")

class HotelManager(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete = models.CASCADE , related_name = "hotel_managers")
    manager_name = models.CharField(max_length = 100)
    manager_contact = models.CharField(max_length = 100)


class HotelBooking(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete = models.CASCADE , related_name="bookings" )
    booking_user = models.ForeignKey(HotelUser, on_delete = models.CASCADE , )
    booking_start_date = models.DateField()
    booking_end_date = models.DateField()
    price = models.FloatField()
