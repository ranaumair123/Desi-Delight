from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.auth.models import Group
from . models import *
# Register your models here.

admin.site.unregister(Group)




@admin.register(MakeTable)
class MakeTableAdmin(admin.ModelAdmin):
    list_display = ['id','table_name','table_type','seating_capacity','table_status']

@admin.register(VisitedUsers)
class VisitedUsersAdmin(admin.ModelAdmin):
    list_display = ['id','visited_user_email','visited_phone_number']

@admin.register(Reservations)
class ReservationsAdmin(admin.ModelAdmin):
    list_display = ['id','table','user','persons','reservation_date','reservation_status']


    
    
    