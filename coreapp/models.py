from django.db import models
from authusers.models import User
from autoslug import AutoSlugField
from datetime import date


# Create your models here.

TABLE_TYPE_CHOICES = (
    ('two_to_four_table', 'Two to Four Person Table'),
    ('bar_height_table', 'Bar Height Tables'),
    ('family_table', 'Family Dining Tables'),
    ('booth_table', 'Booths'),
    ('outdoor_table', 'Outdoor Tables')
)


RESERVATION_STATUS_CHOICES = (
    ('in_review', 'In Review'),
    ('reserved', 'Reserved'),
    ('is_cancelled', 'Cancelled')
)


class MakeTable(models.Model):

    table_name = models.CharField(max_length=30)
    table_type = models.CharField(choices=TABLE_TYPE_CHOICES, max_length=30,)
    seating_capacity = models.PositiveIntegerField(default=2)
    table_status = models.BooleanField(default=True)
    slug = AutoSlugField(populate_from='table_name', unique=True)

    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Tables'

    def __str__(self):
        return self.table_name


class Reservations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(MakeTable, on_delete=models.CASCADE)

    reservation_name = models.CharField(max_length=50)
    reservation_email= models.EmailField(max_length=50)
    reservation_phone = models.CharField(max_length=20)
    reservation_date = models.DateField(verbose_name='Reservation Date')
    reservation_time = models.TimeField(verbose_name='Reservation Time')
    reservation_message = models.CharField(max_length=255)
    persons = models.PositiveIntegerField(verbose_name='Persons')
    
    reservation_status = models.CharField(
        choices=RESERVATION_STATUS_CHOICES, max_length=15, default='in_review')
    # created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Reservations'

    def __str__(self):
        return f"{self.user.username} - {self.table.table_name}"

    def save(self, *args, **kwargs):
        # Update the table_status based on reservation_status and reservation_date
        if self.reservation_status == 'reserved':
            self.table.table_status = False
        elif self.reservation_status == 'in_review' or self.reservation_date < date.today() or self.reservation_status == 'is_cancelled':
            self.table.table_status = True
        self.table.save()
        super().save(*args, **kwargs)



class VisitedUsers(models.Model):
    visited_user_name = models.CharField(max_length=30)
    visited_user_email = models.EmailField(max_length=50)
    visited_phone_number = models.CharField(max_length=15)

    class Meta:
        verbose_name_plural = 'Visited Users'