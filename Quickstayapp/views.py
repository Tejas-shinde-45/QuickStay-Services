from django.shortcuts import render,HttpResponseRedirect,redirect
from accounts.models import *
from django.contrib import messages
from Quickstayapp.models import *
from datetime import datetime
from django.shortcuts import get_object_or_404

def index(request):
    hotels = Hotel.objects.all()

    if request.GET.get('search'):
        hotels = hotels.filter(hotel_name__icontains=request.GET.get('search'))

    if request.GET.get('sort_by'):
        sort_by = request.GET.get('sort_by')
        if sort_by == "sort_low":
            hotels = hotels.order_by('hotel_offer_price')
        elif sort_by == "sort_high":
            hotels = hotels.order_by('-hotel_offer_price')

    # Get list of booked hotel IDs for the logged-in user
    booked_hotel_ids = []
    if request.user.is_authenticated:
        try:
            hotel_user = HotelUser.objects.get(user=request.user)
            booked_hotel_ids = HotelBooking.objects.filter(
                booking_user=hotel_user
            ).values_list('hotel_id', flat=True)
        except HotelUser.DoesNotExist:
            pass

    return render(request, 'index.html', {
        'hotels': hotels[:50],
        'booked_hotel_ids': booked_hotel_ids
    })

def login_page(request):
    return render(request, 'login.html')


def register_page(request):
    return render(request, 'register.html')


#home/views.py
# other views
# def hotel_details(request, slug):
#     hotel = Hotel.objects.get(hotel_slug = slug)

#     if request.method == "POST":
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')
#         start_date = datetime.strptime(start_date , '%Y-%m-%d')
#         end_date = datetime.strptime(end_date , '%Y-%m-%d')
#         days_count = (end_date - start_date).days

#         if days_count <= 0:
#             messages.warning(request, "Invalid Booking Date.")

#             return HttpResponseRedirect(request.path_info)

#         HotelBooking.objects.create(
#             hotel = hotel,
#             booking_user = HotelUser.objects.get(user= request.user),
#             booking_start_date = start_date,
#             booking_end_date =end_date,
#             price = hotel.hotel_offer_price * days_count
#         )
#         messages.warning(request, "Booking Captured.")

#         return HttpResponseRedirect(request.path_info)


#     return render(request, 'hotel_details.html', context = {'hotel' : hotel})




def hotel_details(request, slug):
    hotel = get_object_or_404(Hotel, hotel_slug=slug)
    ameneties = Ameneties.objects.all()

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.warning(request, "You need to be logged in to book a hotel.")
            return redirect('login')  # Ensure 'login' URL name exists

        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            messages.error(request, "Invalid date format.")
            return HttpResponseRedirect(request.path_info)

        days_count = (end_date - start_date).days
        if days_count <= 0:
            messages.warning(request, "Invalid booking dates.")
            return HttpResponseRedirect(request.path_info)

        # Safely get or create HotelUser
        booking_user, created = HotelUser.objects.get_or_create(user=request.user)

        # Create the booking
        HotelBooking.objects.create(
            hotel=hotel,
            booking_user=booking_user,
            booking_start_date=start_date,
            booking_end_date=end_date,
            price=hotel.hotel_offer_price * days_count
        )
        messages.success(request, "Booking captured successfully.")
        return HttpResponseRedirect(request.path_info)

    return render(request, 'hotel_details.html', context={'hotel': hotel,'ameneties':ameneties})