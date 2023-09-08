from django.urls import path
from coreapp import views


app_name = 'coreapp'

urlpatterns = [
    path('',views.index,name='index'),
    path('make-reservation/',views.make_reservation,name='make_reservation'),
    path('contact-us/',views.contact_us,name='contact-us'),
    path('get-reservations/',views.reservation_listing,name='reservation-listing'),
    path('cancel-reservation/',views.update_reservation_view,name='cancel-reservation'),
]