from django.db import models
from django.forms import ModelForm
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

class subscriber(models.Model):
	email = models.CharField(max_length=150)
	subscriber_id = models.AutoField(primary_key=True)

class listings_waiting_list(models.Model):
	property_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	mobile_no = models.CharField(max_length=10)
	location = models.CharField(max_length=100)
	price = models.IntegerField()
	purpose = models.CharField(max_length=50)
	tyype = models.CharField(max_length=50)

class contact_on_property(models.Model):
	message_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	email = models.EmailField(max_length=150)
	message = models.CharField(max_length=1000)
	property_id = models.IntegerField()

	Complete = 'Complete'
	Pending = 'Pending'

	STATUS_CHOICES = (
        (Complete, 'Complete'),
        (Pending, 'Pending'),
    )
	status = models.CharField(max_length=10, choices=STATUS_CHOICES,default=Pending)


class listrequest(models.Model):
	request_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	email = models.CharField(max_length=200)
	mobile_no = models.CharField(max_length=10)
class booked_viewings(models.Model):
	booking_id = models.AutoField(primary_key=True)
	mobile_no = models.CharField(max_length=10)
	property_id = models.IntegerField()
	name = models.CharField(max_length=100)
	date = models.DateField(blank=False,)
	propertytitle = models.CharField(max_length=500,blank=True)
	time = models.CharField(max_length=10)

class propety(models.Model):
	lister = models.CharField(max_length=100)
	agent = models.CharField(max_length=100) 
	property_id = models.AutoField(primary_key=True)
	propertytitle = models.CharField(max_length=2000)
	location = models.CharField(max_length=1000)
	price = models.IntegerField()
	propertytype = models.CharField(max_length=50)
	extras = models.CharField(max_length=20,blank=True)
	rentbuy = models.CharField(max_length=10)
	property_picture = models.FileField(upload_to='',blank=True)
	entrance_pic = models.FileField(upload_to='',blank=True)
	sitting_pic = models.FileField(upload_to='',blank=True)
	dining_pic = models.FileField(upload_to='',blank=True)
	kitchen_pic = models.FileField(upload_to='',blank=True)
	bedroom_pic = models.FileField(upload_to='',blank=True)
	bathroom_pic = models.FileField(upload_to='',blank=True)
	description = models.CharField(max_length=5000)
	bedrooms = models.IntegerField(blank=True)
	bathrooms = models.IntegerField(blank=True)
	patio = models.IntegerField(blank=True)
	garage = models.IntegerField(blank=True)
	area = models.CharField(max_length=20,blank=True)

	Complete = 'Complete'
	Pending = 'Pending'

	STATUS_CHOICES = (
        (Complete, 'Complete'),
        (Pending , 'Pending'),
    )
	status = models.CharField(max_length=10, choices=STATUS_CHOICES,default=Pending)


from .forms import property_form

class property_admin(admin.ModelAdmin):
	form = property_form
	property_title = models.CharField(max_length=2000)
	locatiom = models.CharField(max_length=1000)
