from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

Reservation_Options = (
    ("Table Reservations", "Table Reservations"),
    ("Booth Reservations", "Booth Reservations"),
    ("Couch Reservations", "Couch Reservations"),
    ("Private Occasion", "Private Occasion"),
)

TIME_CHOICES = (
    ("1 PM", "1 PM"),
    ("1:30 PM", "1:30 PM"),
    ("2 PM", "2 PM"),
    ("2 PM", "2:30 PM"),
    ("3 PM", "3 PM"),
    ("3:30 PM", "3:30 PM"),
    ("4 PM", "4 PM"),
    ("4:30 PM", "4:30 PM"),
    ("5 PM", "5 PM"),
    ("5:30 PM", "5:30 PM"),
    ("6 PM", "6 PM"),
    ("6:30 PM", "6:30 PM"),
    ("7 PM", "7 PM"),
    ("7:30 PM", "7:30 PM"),
)

Guest_Number = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("6", "7"),
)


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    service = models.CharField(max_length=50, choices=Reservation_Options, default="Table Reservations")
    day = models.DateField(default=datetime.now)
    guests = models.CharField(max_length=1, choices=Guest_Number, default="")
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="1 PM")
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f"{self.user} | day: {self.day} | time: {self.time} | guests: {self.guests}"


# model to collect payment


# forms.py


class PaymentForm(forms.Form):
    name = forms.CharField(label='Name on Card', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    card_number = forms.CharField(label='Card Number', max_length=16)
    expiration_date = forms.DateField(label='Expiration Date', input_formats=['%m/%Y'])
    cvv = forms.CharField(label='CVV', max_length=3)
    amount = forms.DecimalField(label='Amount', max_digits=6, decimal_places=2, validators=[MinValueValidator(10), MaxValueValidator(1000)])
