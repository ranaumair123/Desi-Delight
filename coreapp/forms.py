from django.core.validators import RegexValidator, EmailValidator
from django import forms
from .models import MakeTable, Reservations


class ReservationForm(forms.Form):
    table = forms.CharField(required=True, widget=forms.Select())
    reservation_name = forms.CharField(required=True, max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Name'}))
    reservation_email = forms.EmailField(required=True, max_length=50, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'type': 'email', 'placeholder': 'Email'}))
    reservation_phone = forms.CharField(required=True, max_length=20, 
                                        validators=[RegexValidator(regex=r'^(\+92|0)?(3\d{9})$',
                                        message='Enter a valid Pakistan phone number.')], widget=forms.NumberInput(
        attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Phone #'}))
    reservation_date = forms.DateField(required=True, widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Date'}))
    reservation_time = forms.TimeField(required=True, widget=forms.TimeInput(
        attrs={'class': 'form-control', 'type': 'time', 'placeholder': 'Time'}))
    reservation_no_of_people = forms.IntegerField(required=True, min_value=1, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'type': 'number', 'placeholder': '# of people'}))
    reservation_text_message = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Message'}))


class VisitedUserForm(forms.Form):
    visited_user_name = forms.CharField(
        required=True, max_length=30, help_text='Mohammad Ahmed')
    visited_user_email = forms.EmailField(
        required=True, help_text='admin@gmail.com', validators=[EmailValidator(message="Enter a Valid Email")])
    visited_user_email_subject = forms.CharField(
        required=True, max_length=50, widget=forms.TextInput())
    visited_user_message = forms.CharField(
        required=True, max_length=255, widget=forms.Textarea())
    visited_user_phone = forms.CharField(required=True, help_text='Enter Phone number in this formate "03XXXXXXXXX"', validators=[RegexValidator(regex=r'^(\+92|0)?(3\d{9})$',
                                                                                                                                                 message='Enter a valid Pakistan phone number.')])
