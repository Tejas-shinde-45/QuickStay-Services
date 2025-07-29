# from django.shortcuts import render,redirect
# from django.contrib import messages
# from django.http import HttpResponse
# from .models import *
# from django.db.models import Q
# from django.contrib.auth import authenticate,login
# from .utils import generateRandomToken,sendEmailToken


# # Create your views here.
# def login_page(request):    
#     if request.method == "POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         hotel_user = HotelUser.objects.filter(
#             email = email)


#         if not hotel_user.exists():
#             messages.warning(request, "No Account Found.")
#             return redirect('/account/login/')

#         if not hotel_user[0].is_verified:
#             messages.warning(request, "Account not verified")
#             return redirect('/account/login/')

#         hotel_user = authenticate(username = hotel_user[0].username , password=password)

#         if hotel_user:
#             messages.success(request, "Login Success")
#             login(request , hotel_user)
#             return redirect('/account/login/')

#         messages.warning(request, "Invalid credentials")
#         return redirect('/account/login/')
#     return render(request, 'login.html')

# def register_page(request):
#     if request.method == "POST":

#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         phone_number = request.POST.get('phone_number')

#         hotel_user = HotelUser.objects.filter(
#             Q(email = email) | Q(phone_number  = phone_number)
#         )

#         if hotel_user.exists():
#             messages.warning(request, "Account exists with Email or Phone Number.")
#             return redirect('/accounts/register/')

#         hotel_user = HotelUser.objects.create(
#             username = phone_number,
#             first_name = first_name,
#             last_name = last_name,
#             email = email,
#             phone_number = phone_number,
#             email_token = generateRandomToken()
#         )
#         hotel_user.set_password(password)
#         hotel_user.save()

#         sendEmailToken(email , hotel_user.email_token)

#         messages.success(request, "An email Sent to your Email")
#         return redirect('/accounts/register/')


#     return render(request, 'register1.html')
# *****************************************************************************************
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import generateSlug
from django.shortcuts import get_object_or_404





def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        user_type = request.POST["user_type"]
        phone = request.POST["phone_number"]

        user = User.objects.create_user(username=username, email=email, password=password)

        if user_type == "user":
            HotelUser.objects.create(user=user, phone_number=phone)
        else:
            HotelVendor.objects.create(user=user, phone_number=phone)

        messages.success(request, "Registration successful. Please login.")
        return redirect("login")

    return render(request, "register1.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("index")  # change to dashboard/home
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "login1.html")

def logout_view(request):
    logout(request)
    return redirect("login")


# for venders...
# accounts/views.py

def register_venders(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        business_name = request.POST.get('business_name')
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone_number")

        username = email.split('@')[0]

        # Check if phone already used
        if HotelVendor.objects.filter(phone_number=phone).exists():
            messages.error(request, "Phone number already in use.")
            return redirect("registervender")

        # Optional: check if user with username or email exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("registervender")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("registervender")

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Create vendor profile
        HotelVendor.objects.create(
            user=user,
            business_name=business_name,
            phone_number=phone
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect("loginvender")

    return render(request, "vendor/register_vender.html")

def login_venders(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "vendor/login_vender.html")
# --------------------------------------------------------------------------------
@login_required(login_url='loginvender')
def dashboard(request):
    try:
        vendor = HotelVendor.objects.get(user=request.user)  # get the vendor linked to the logged-in user
        hotels = Hotel.objects.filter(hotel_owner=vendor)     # now this will work
    except HotelVendor.DoesNotExist:
        messages.error(request, "Vendor profile not found.")
        return redirect('loginvender')  # or show an error page

    context = {'hotels': hotels}
    return render(request, 'vendor/vedor_dashboard.html', context)
# -----------------------------------------------------------------------------------
# views.py
@login_required(login_url='login_vendor')
def add_hotel(request):
    if request.method == "POST":
        hotel_name = request.POST.get('hotel_name')
        hotel_description = request.POST.get('hotel_description')
        ameneties= request.POST.getlist('ameneties')
        hotel_price= request.POST.get('hotel_price')
        hotel_offer_price= request.POST.get('hotel_offer_price')
        hotel_location= request.POST.get('hotel_location')
        hotel_slug = generateSlug(hotel_name)

        hotel_vendor = get_object_or_404(HotelVendor, user=request.user)

        hotel_obj = Hotel.objects.create(
            hotel_name = hotel_name,
            hotel_description = hotel_description,
            hotel_price = hotel_price,
            hotel_offer_price = hotel_offer_price,
            hotel_location = hotel_location,
            hotel_slug = hotel_slug,
            hotel_owner = hotel_vendor
        )

        for ameneti in ameneties:
            ameneti = Ameneties.objects.get(id = ameneti)
            hotel_obj.ameneties.add(ameneti)
            hotel_obj.save()


        messages.success(request, "Hotel Created")
        return redirect('dashboard')


    ameneties = Ameneties.objects.all()

    return render(request, 'vendor/add_hotel.html', context = {'ameneties' : ameneties})


# accounts/views.py
#other views 

@login_required(login_url='login_vendor')
def upload_images(request, slug):
    hotel_obj = Hotel.objects.get(hotel_slug = slug)
    if request.method == "POST":
        image = request.FILES['image']
        print(image)
        HotelImages.objects.create(
        hotel = hotel_obj,
        image = image
        )
        return HttpResponseRedirect(request.path_info)

    return render(request, 'vendor/upload_image.html', context = {'images' : hotel_obj.hotel_images.all()})

@login_required(login_url='login_vendor')
def delete_image(request, id):
    print(id)
    print("#######")
    hotel_image = HotelImages.objects.get(id = id)
    hotel_image.delete()
    messages.success(request, "Hotel Image deleted")
    return redirect('dashboard')

# views.py
@login_required(login_url='login_vendor')
def edit_hotel(request, slug):
    hotel_obj = Hotel.objects.get(hotel_slug=slug)
    
    # Check if the current user is the owner of the hotel
    print(request.user.id)
    print(hotel_obj.hotel_owner.id)
    # if request.user.id != hotel_obj.hotel_owner.id:
    #     return HttpResponse("You are not authorized")

    if request.method == "POST":
        # Retrieve updated hotel details from the form
        hotel_name = request.POST.get('hotel_name')
        hotel_description = request.POST.get('hotel_description')
        hotel_price = request.POST.get('hotel_price')
        hotel_offer_price = request.POST.get('hotel_offer_price')
        hotel_location = request.POST.get('hotel_location')
        
        # Update hotel object with new details
        hotel_obj.hotel_name = hotel_name
        hotel_obj.hotel_description = hotel_description
        hotel_obj.hotel_price = hotel_price
        hotel_obj.hotel_offer_price = hotel_offer_price
        hotel_obj.hotel_location = hotel_location
        hotel_obj.save()
        
        messages.success(request, "Hotel Details Updated")

        return HttpResponseRedirect(request.path_info)

    # Retrieve amenities for rendering in the template
    ameneties = Ameneties.objects.all()
    
    # Render the edit_hotel.html template with hotel and amenities as context
    return render(request, 'vendor/edit_hotel.html', context={'hotel': hotel_obj, 'ameneties': ameneties})



@login_required(login_url='login_vendor')
def delete_hotel(request, id):
    print(id)
    print("#######")
    hotel = Hotel.objects.get(id = id)
    hotel.delete()
    messages.success(request, "Hotel deleted")
    return redirect('dashboard')


# def logout_view(request):
#     logout(request)
#     return redirect('login')