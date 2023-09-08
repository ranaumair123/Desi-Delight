from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import MakeTable, Reservations, VisitedUsers
from .forms import ReservationForm, VisitedUserForm
from .utils import Util
from django.contrib import messages
# Create your views here.


def index(request):
    table = MakeTable.objects.filter(table_status=True).values('table_name')
    reservation_form = ReservationForm()
    visited_user_form =VisitedUserForm()
    return render(request, 'coreapp/index.html',context={'form':reservation_form,'form2':visited_user_form,'table':table})


def make_reservation(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ReservationForm(request.POST)
            if form.is_valid():
                table_name = form.cleaned_data['table']
                table = MakeTable.objects.get(table_name=table_name)
                reservation = Reservations(
                    user=request.user,  
                    table=table,  
                    reservation_name=form.cleaned_data['reservation_name'],
                    reservation_email=form.cleaned_data['reservation_email'],
                    reservation_phone=form.cleaned_data['reservation_phone'],
                    reservation_date=form.cleaned_data['reservation_date'],
                    reservation_time=form.cleaned_data['reservation_time'],
                    reservation_message = form.cleaned_data['reservation_text_message'],
                    persons=form.cleaned_data['reservation_no_of_people'],
                )
                reservation.save()
                messages.success(request,'Your booking request was sent. We will call back or send an Email to confirm your reservation. Thank you!')
                return HttpResponseRedirect(reverse('coreapp:index'))  
        else:
            form = ReservationForm()  
        table = MakeTable.objects.filter(table_status=True).values('table_name')
        messages.error(request,'Please fill the Reservation Form with Appropriate data',extra_tags='danger')
        return render(request, 'coreapp/index.html', context={'form': form,'table':table})
    else:
        messages.error(request,'You are not authorized to book a table. Please Register Yourself First or Login. Thank you!',extra_tags='danger')
    return HttpResponseRedirect(reverse('authusers:sign-up'))

def reservation_listing(request):
    if request.user.is_authenticated:
        user_reservations = Reservations.objects.filter(user = request.user)
        print('User Reservations',user_reservations )
        return render(request,'coreapp/reservations.html',context={'reservations':user_reservations})
    return redirect('coreapp:index')

def update_reservation_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            record_id = request.POST.get('reservation_id')
            reservation = Reservations.objects.get(id=record_id)
            reservation.reservation_status = 'is_cancelled'
            reservation.save() 
            messages.success(request,'Reservation has been cancelled successfully!')
            
    else:
        messages.error(request,'You are not authorized to change the status',extra_tags='danger')
    return HttpResponseRedirect(reverse('coreapp:reservation-listing'))

def contact_us(request):
    if request.method == 'POST':
        form = VisitedUserForm(request.POST)
        if form.is_valid():
            visited_user = VisitedUsers(
                visited_user_name = form.cleaned_data['visited_user_name'],
                visited_user_email = form.cleaned_data['visited_user_email'],
                visited_phone_number = form.cleaned_data['visited_user_phone']
            )
            visited_user.save()

            e_subject = form.cleaned_data['visited_user_email_subject']
            msg = form.cleaned_data['visited_user_message']
            mail = form.cleaned_data['visited_user_email']
            try:
                subject = e_subject
                body = msg
                email = mail

                data = {
                    'subject': subject,
                    'body': body,
                    'to_email': email,
                }
                Util.send_email(data)
                messages.success(request,'Email sent successfully')

            except Exception:
                messages.error(request,'Error in Sending the Email',extra_tags='danger')
            return HttpResponseRedirect(reverse('coreapp:index'))
    else:
        form = VisitedUserForm() 
    messages.error(request,'Please fill the Contact Us form with Appropriate data',extra_tags='danger')
    return render(request, 'coreapp/index.html', context={'form2': form})
