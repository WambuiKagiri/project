from django.contrib import admin
from django.contrib import messages
from django.shortcuts import render
from django import forms
from django.contrib.auth.admin import UserAdmin

from .models import User
from .models import subscriber
from .models import listings_waiting_list
from .models import contact_on_property
from .models import propety
from .models import booked_viewings,listrequest
# Register your models here.
admin.site.register(User)


admin.site.register(listrequest)

class property_admin(admin.ModelAdmin):
	def formfield_for_dbfield(self, db_field, **kwargs):
		formfield = super(property_admin, self).formfield_for_dbfield(db_field, **kwargs)
		if db_field.name == 'description':
			formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
			return formfield
		if db_field.name == 'location':
			formfield.widget = forms.TextInput(attrs=formfield.widget.attrs)
			return formfield
		if db_field.name == 'propertytitle':
			formfield.widget = forms.TextInput(attrs=formfield.widget.attrs)
			return formfield
		if db_field.name == 'price':
			formfield.widget = forms.TextInput(attrs=formfield.widget.attrs)
			return formfield
		if db_field.name == 'propertytype':
			formfield.widget = forms.TextInput(attrs=formfield.widget.attrs)
			return formfield
		if db_field.name == 'rentbuy':
			formfield.widget = forms.TextInput(attrs=formfield.widget.attrs)
			return formfield
		if db_field.name == 'extras':
			formfield.widget = forms.TextInput(attrs=formfield.widget.attrs)
			return formfield
		if db_field.name == 'bedrooms':
			formfield.widget = forms.TextInput(attrs=formfield.widget.attrs)
			return formfield
		if db_field.name == 'bathrooms':
			formfield.widget = forms.TextInput(attrs=formfield.widget.attrs)
			return formfield
		if db_field.name == 'patio':
			formfield.widget = forms.TextInput(attrs=formfield.widget.attrs)
			return formfield
		if db_field.name == 'area':
			formfield.widget = forms.TextInput(attrs=formfield.widget.attrs)
			return formfield
		if db_field.name == 'garage':
			formfield.widget = forms.TextInput(attrs=formfield.widget.attrs)
			return formfield
		if db_field.name == 'lister':
			formfield.widget = forms.TextInput(attrs=formfield.widget.attrs)
			return formfield
		if db_field.name == 'status':
			formfield.widget = forms.TextInput(attrs=formfield.widget.attrs)
			return formfield
		if db_field.name == 'agent':
			formfield.widget = forms.TextInput(attrs=formfield.widget.attrs)
			return formfield
		if db_field.name == 'property_picture':
			formfield.widget = forms.FileInput(attrs=formfield.widget.attrs)
			return formfield
		if db_field.name == 'entrance_pic':
			formfield.widget = forms.FileInput(attrs=formfield.widget.attrs)
			return formfield
		if db_field.name == 'sitting_pic':
			formfield.widget = forms.FileInput(attrs=formfield.widget.attrs)
			return formfield
		if db_field.name == 'dining_pic':
			formfield.widget = forms.FileInput(attrs=formfield.widget.attrs)
			return formfield
		if db_field.name == 'kitchen_pic':
			formfield.widget = forms.FileInput(attrs=formfield.widget.attrs)
			return formfield
		if db_field.name == 'bedroom_pic':
			formfield.widget = forms.FileInput(attrs=formfield.widget.attrs)
			return formfield

	list_display = ['property_id','lister','agent','status','propertytitle','location','price','propertytype','rentbuy','bedrooms','bathrooms','patio','garage','area']
	list_filter = ['price','location','rentbuy','propertytype']
	class Meta:
		model = propety

class subAdmin(admin.ModelAdmin):
	list_display = ['subscriber_id','email']

	class Meta:
		model = subscriber


admin.site.register(subscriber,subAdmin)
admin.site.register(propety,property_admin)


class listings_waiting_listAdmin(admin.ModelAdmin):
	actions = ['add_to_properties']


	# def add_to_properties(self, request, queryset):
	# 	if 'do_action' in request.POST:
	# 		form = ListToProperty_Form(request.POST)
	# 		if form.is_valid():
		# admin.site.add_action(add_to_properties)

admin.site.register(listings_waiting_list,listings_waiting_listAdmin)



class booked_viewingsAdmin(admin.ModelAdmin):
	list_display = ['booking_id','name','mobile_no','property_id','date','time','propertytitle']
	list_filter = ['name','date','propertytitle','time']
	
	class Meta:
		model = booked_viewings
admin.site.register(booked_viewings,booked_viewingsAdmin)

class contact_on_propertyAdmin(admin.ModelAdmin):
	list_display = ['message_id','name','email','property_id','message','status']
	
	class Meta:
		model = contact_on_property
admin.site.register(contact_on_property,contact_on_propertyAdmin)