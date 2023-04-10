from datetime import timedelta
import stripe
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *


def index(request):
    return render(request, "index.html", {})


def story(request):
    return render(request, 'story.html')


def contact(request):
    return render(request, 'contact.html')


def thanks(request):
    return render(request, 'thanks.html', 'index')



def terms(request):
    return render(request, 'terms.html')


def booking(request):
    # Calling 'validWeekday' Function to Loop days you want in the next 21 days:
    weekdays = validWeekday(22)

    # Only show the days that are not full:
    validateWeekdays = isWeekdayValid(weekdays)

    if request.method == 'POST':
        service = request.POST.get('service')
        day = request.POST.get('day')
        guests = request.POST.get('guests')

        if service == None:
            messages.success(request, "Please Select A Service!")
            return redirect('booking')

        # Store day and service in django session:
        request.session['day'] = day
        request.session['service'] = service
        request.session['guests'] = guests

        return redirect('bookingSubmit')

    return render(request, 'booking.html', {
        'weekdays': weekdays,
        'validateWeekdays': validateWeekdays,
    })


def bookingSubmit(request):
    user = request.user
    times = [
        "1 PM", "1:30 PM", "2 PM", "2:30 PM", "3 PM", "3:30 PM", "4 PM", "4:30 PM", "5 PM", "5:30 PM", "6 PM",
        "6:30 PM", "7 PM", "7:30 PM"
    ]
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    # Get stored data from django session:
    day = request.session.get('day')
    service = request.session.get('service')
    guests = request.session.get('guests')

    # Only show the time of the day that has not been selected before:
    hour = checkTime(times, day)
    if request.method == 'POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)


        if service != None:
            if day <= maxDate and day >= minDate:
                if date == 'Monday' or date == 'Saturday' or date == 'Wednesday':
                    if Reservation.objects.filter(day=day).count() < 11:
                        if Reservation.objects.filter(day=day, time=time).count() < 1:
                            reservationForm = Reservation.objects.get_or_create(
                                user=user,
                                service=service,
                                day=day,
                                time=time,
                                guests=guests,

                            )
                            messages.success(request, "Reservation Saved!")
                            return redirect('pay')
                        else:
                            messages.success(request, "The Selected Time Has Been Reserved Before!")
                    else:
                        messages.success(request, "The Selected Day Is Full!")
                else:
                    messages.success(request, "The Selected Date Is Incorrect")
            else:
                messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
        else:
            messages.success(request, "Please Select A Reservation Option!")

    return render(request, 'bookingSubmit.html', {
        'times': hour,
    })


def userPanel(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user).order_by('day', 'time')
    return render(request, 'userPanel.html', {
        'user': user,
        'reservations': reservations,
    })


def userUpdate(request, id):
    reservation = Reservation.objects.get(pk=id)
    userdatepicked = reservation.day
    # Copy  booking:
    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')

    # 24h if statement in template:
    delta24 = (userdatepicked).strftime('%Y-%m-%d') >= (today + timedelta(days=1)).strftime('%Y-%m-%d')
    # Calling 'validWeekday' Function to Loop days you want in the next 21 days:
    weekdays = validWeekday(22)

    # Only show the days that are not full:
    validateWeekdays = isWeekdayValid(weekdays)

    if request.method == 'POST':
        service = request.POST.get('service')
        day = request.POST.get('day')
        guests = request.POST.get('guests')

        # Store day and service in django session:
        request.session['day'] = day
        request.session['service'] = service
        request.session['guests'] = guests

        return redirect('userUpdateSubmit', id=id)

    return render(request, 'userUpdate.html', {
        'weekdays': weekdays,
        'validateWeekdays': validateWeekdays,
        'delta24': delta24,
        'id': id,
    })


def userUpdateSubmit(request, id, ):
    user = request.user
    times = [
        "1 PM", "1:30 PM", "2 PM", "2:30 PM", "3 PM", "3:30 PM", "4 PM", "4:30 PM", "5 PM", "5:30 PM", "6 PM",
        "6:30 PM", "7 PM", "7:30 PM"
    ]
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    day = request.session.get('day')
    service = request.session.get('service')
    guests = request.session.get('guests')

    # Only show the time of the day that has not been selected before and the time he is editing:
    hour = checkEditTime(times, day, id)
    reservation = Reservation.objects.get(pk=id)
    userSelectedTime = reservation.time
    if request.method == 'POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if service != None:
            if day <= maxDate and day >= minDate:
                if date == 'Monday' or date == 'Saturday' or date == 'Wednesday':
                    if Reservation.objects.filter(day=day).count() < 11:
                        if Reservation.objects.filter(day=day, time=time).count() < 1 or userSelectedTime == time:
                            reservationForm = Reservation.objects.filter(pk=id).update(
                                user=user,
                                service=service,
                                day=day,
                                time=time,
                                guests=guests,

                            )
                            messages.success(request, "Reservation Edited!")
                            return redirect('index')
                        else:
                            messages.success(request, "The Selected Time Has Been Reserved Before!")
                    else:
                        messages.success(request, "The Selected Day Is Full!")
                else:
                    messages.success(request, "The Selected Date Is Incorrect")
            else:
                messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
        else:
            messages.success(request, "Please Select A Reservation Option!")
        return redirect('userPanel')

    return render(request, 'userUpdateSubmit.html', {
        'times': hour,
        'id': id,
    })


def staffPanel(request):
    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime
    # Only show the reservations 21 days from today
    items = Reservation.objects.filter(day__range=[minDate, maxDate]).order_by('day', 'time')

    return render(request, 'staffPanel.html', {
        'items': items,
    })


def dayToWeekday(x):
    z = datetime.strptime(x, "%Y-%m-%d")
    y = z.strftime('%A')
    return y


def validWeekday(days):
    # Loop days you want in the next 21 days:
    today = datetime.now()
    weekdays = []
    for i in range(0, days):
        x = today + timedelta(days=i)
        y = x.strftime('%A')
        if y == 'Monday' or y == 'Saturday' or y == 'Wednesday':
            weekdays.append(x.strftime('%Y-%m-%d'))
    return weekdays


def isWeekdayValid(x):
    validateWeekdays = []
    for j in x:
        if Reservation.objects.filter(day=j).count() < 10:
            validateWeekdays.append(j)
    return validateWeekdays


def checkTime(times, day):
    # Only show the time of the day that has not been selected before:
    x = []
    for k in times:
        if Reservation.objects.filter(day=day, time=k).count() < 1:
            x.append(k)
    return x


def checkEditTime(times, day, id):
    # Only show the time of the day that has not been selected before:
    x = []
    reservation = Reservation.objects.get(pk=id)
    time = reservation.time
    for k in times:
        if Reservation.objects.filter(day=day, time=k).count() < 1 or time == k:
            x.append(k)
    return x


def Accept(request):

    return render(request, 'Accept.html')


def cancel(request):
    return render(request, 'cancel.html')


def success(request):
    return render(request, 'success.html')


# Save and validate Payment
# views.py
def pay(request):
    return render(request, 'pay.html')


def checkout(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=[
            'card'
        ],
        line_items=[
            {
                # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                'price': 'price_1MqMTWInB8jXLmYzxTekayWc',
                'quantity': 1,
            },
        ],
        mode='payment',

        success_url='https://kgslounge.herokuapp.com/success',


        cancel_url='https://kgslounge.herokuapp.com/cancel',
    )

    return redirect(checkout_session.url, code=303)
