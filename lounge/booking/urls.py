from django.urls import path 
from . import views
from .views import checkout


urlpatterns = [
    path('', views.index, name='index'),
    path('terms', views.terms, name='terms'),
    path('thanks', views.thanks, name='thanks'),
    path('pay/', views.pay, name='pay'),
    path('checkout', views.checkout, name='checkout'),
    path('cancel/', views.cancel, name='cancel'),
    path('success/', views.success, name='success'),
    path('Accept', views.Accept, name='Accept'),
    path('story', views.story, name='story'),
    path('contact', views.contact, name='contact'),
    path('booking', views.booking, name='booking'),
    path('booking-submit', views.bookingSubmit, name='bookingSubmit'),
    path('user-panel', views.userPanel, name='userPanel'),
    path('user-update/<int:id>', views.userUpdate, name='userUpdate'),
    path('user-update-submit/<int:id>', views.userUpdateSubmit, name='userUpdateSubmit'),
    path('staff-panel', views.staffPanel, name='staffPanel'),
]
