from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.views import generic
from django.template.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth import login as clogin
from django.contrib.auth import authenticate
from django.utils.safestring import mark_safe
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test
from ajax_search.forms import SearchForm
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import json
import re
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import FormView
from django.db.models import Q
from django.contrib.auth import (
authenticate,
get_user_model,
login,
logout,
	)

user = get_user_model()
#imported forms
from .forms import subscribe_form
from .forms import list_form
from .forms import customer_form
from .forms import booking_form
from .forms import searchform,listrequestform

#imported models
from .models import subscriber
from .models import listings_waiting_list
from .models import contact_on_property
from .models import booked_viewings
from .models import propety,User,listrequest, paypal_payments



@csrf_protect
@ensure_csrf_cookie
def home( request, **kwargs):
	propertys = propety.objects.all().filter(rentbuy='Rent')[:4]
	props = propety.objects.all().filter(rentbuy='Sale')[:4]
	propetys = propety.objects.all()
	return render(request, 'index.html', {'propertys':propertys,'props':props, 'propetys':propetys})


@csrf_protect
@ensure_csrf_cookie
def subscribe(request, **kwargs):
	if request.method == 'POST':
		form = None
		form = subscribe_form(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Thank you for subscribing, We won't spam!")
			return render(request, 'index.html', {'form':form})

		else:
			return render(request, 'index.html', {'form':form})
				

	else:
		return render(request, 'index.html', {'form':form})


class AboutPageView(TemplateView):
	def get(self, request, **kwargs): 
		return render(request, 'about.html', context=None)
		
class ContactPageView(TemplateView):
	def get(self, request, **kwargs): 
		return render(request, 'contact.html', context=None)

	def post(self,request, **kwargs):
		if request.method == 'POST':
			form = customer_form(request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/success/')

		else:
			return render(request, 'success.html', {'form':form})	

def search(request):
	if request.method == 'POST':
		tyype = request.POST['propertytype']
		re = request.POST['rentbuy']
		loc = request.POST['location']
		beds = request.POST['bedrooms']
		baths = request.POST['bathrooms']
		minprice = request.POST['minprice']
		maxprice = request.POST['maxprice']
		
		print(minprice,maxprice,loc)
		# stuff2 = propety.objects.filter(price__gte=minprice,price__lte=maxprice)
		stuff = propety.objects.filter(Q(price__gte=minprice,price__lte=maxprice) & (Q(propertytype__icontains=tyype) & Q(rentbuy__icontains=re)  & Q(location__icontains=loc) & Q(bedrooms__icontains=beds) & Q(bathrooms__icontains=baths))) 
		return render(request, 'ajax_search.html',{'stuff':stuff})	
	else:
		return render(request, 'index.html')



@csrf_protect
@ensure_csrf_cookie		
def propertypage(request, propertytitle,pk, **kwargs): 
	propertys = propety.objects.all().filter(propertytitle= propertytitle)
	if request.method == 'POST':
		form = customer_form(request.POST)
		if form.is_valid():
			# form.save()
			p = form.cleaned_data.get('location')
			print (p)
			try:
				s = User.objects.filter(location__iexact=p).first()
				
				print(s.email)
			except ObjectDoesNotExist:
				pass
				#s = User.objects.filter(location__exact='').only('email').first()
			
			current_site = get_current_site(request)
			properrty = form.cleaned_data.get('propertytitle')
			message = render_to_string('propertymail.html',{
			'user':user,
			'domain':current_site.domain,
			'properrty':properrty,
			})
			mail_subject = 'Property Details Request'
			to_email = s.email
			email = EmailMessage(mail_subject,message,to=[to_email])
			email.send()
			print("haifanyi")
			messages.success(request, "Your message has been sent")
			return render(request, 'property.html', {'form':form,'propertys':propertys})

		else:
			
			propertys = propety.objects.all().filter(propertytitle= propertytitle)
			return render(request, 'property.html',{'propertys':propertys})

	else:
		
		propertys = propety.objects.all().filter(propertytitle= propertytitle)
		return render(request, 'property.html',{'propertys':propertys})
	

@csrf_protect
@ensure_csrf_cookie	
def booking(request,propertytitle, **kwargs):
	propertys = propety.objects.all().filter(propertytitle= propertytitle)
	f = booking_form(request.POST)
	if request.method == 'POST':
		
		if f.is_valid():
			booking = f.save()
			booking.save()
			current_site = get_current_site(request)
			properrty = f.cleaned_data.get('propertytitle')
			message = render_to_string('bookingmail.html',{
			'user':user,
			'domain':current_site.domain,
			'properrty':properrty,
			})
			mail_subject = 'Property viewing booking'
			to_email = f.cleaned_data.get('email')
			email = EmailMessage(mail_subject,message,to=[to_email])
			email.send()
			messages.success(request, "Your booking has been made. Please check your email.")
			return render(request, 'property.html', {'f':f,'propertys':propertys})
			
		else:
			propertys = propety.objects.all().filter(propertytitle= propertytitle)
			return render(request, 'property.html', {'f':f,'propertys':propertys})

	else:
		propertys = propety.objects.all().filter(propertytitle= propertytitle)
		return render(request, 'property.html', {'f':f,'propertys':propertys})


class PropertiesPageView(TemplateView):
	def get(self, request, **kwargs):
		propertyss = propety.objects.all()
		paginator = Paginator(propertyss,4)
		

		page =request.GET.get('page')
		try:
			propertyss = paginator.page(page)
		except PageNotAnInteger:
			propertyss = paginator.page(1)
		except EmptyPage:
			propertyss = paginator.page(paginator.num_pages)

		return render(request, 'properties.html', {'propertyss':propertyss})

@csrf_protect
@ensure_csrf_cookie
@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Agents').exists())
def dashboard(request):
	propt = propety.objects.filter(agent = request.user)
	paginator = Paginator(propt,4)
	
	page = request.GET.get('page')
	try:
		propt = paginator.page(page)
	except PageNotAnInteger:
		propt = paginator.page(1)
	except EmptyPage:
		propt = paginator.page(paginator.num_pages)
	
	return render(request, 'agent.html',{'propt':propt})
	# else:
	# 	return redirect('/accounts/login/')

def agentlistrequests(request):
	lisstt = listrequest.objects.all()
	return render(request,'listrequests.html',{'lisstt':lisstt})

class BookingsPageView(TemplateView):
	def get(self,request, **kwargs):
		books = booked_viewings.objects.all()	
		return render(request,'bookedviewings.html',{'books':books})


def chatindex(request):
    return render(request, 'chatindex.html', {})

def message(request, room_name):
    return render(request, 'message.html', {
       'room_name_json': mark_safe(json.dumps(room_name))
   })


def clientprofile(request):
    return render(request,'clientprofile.html')


def agentprofile(request):
    return render(request,'profile.html')

def agentsearch(request):
	if request.method=="GET":
		search_text = request.POST['search_text']
	else:
		search_text = ''


	bookings =  booked_viewings.objects.all().filter(Title__icontains=search_text)[:5]
	listings =  listings_waiting_list.objects.all().filter(Title__icontains=search_text)[:5]

	return render(request,'agentsearch.html',{'bookings':bookings,'listings':listings})



@csrf_protect
@ensure_csrf_cookie
def listpropetrty(request):
	form = list_form(request.POST)
	if request.method == 'POST':	
		if form.is_valid():
			title = form.cleaned_data.get('propertytitle')
			tyype = form.cleaned_data.get('propertytype')
			loc = form.cleaned_data.get('location')
			pri = form.cleaned_data.get('price')
			purpose = form.cleaned_data.get('rentbuy')
			beds = form.cleaned_data.get('bedrooms')
			baths = form.cleaned_data.get('bathrooms')
			ar = form.cleaned_data.get('area')
			pat = form.cleaned_data.get('patio')
			gar = form.cleaned_data.get('garage')
			desc = form.cleaned_data.get('description')
			
			p = propety.objects.create(propertytitle=title,propertytype=tyype,location=loc,price=pri,rentbuy=purpose,bedrooms=beds,bathrooms=baths,area=ar,patio=pat,garage=gar,description=desc)

			print(p)
			# propety.save()	
			messages.success(request, "Property added successfully")			
			return render(request, 'listToproperty.html',{'form':form})

		else:
			print("form not valid")		
			return render(request, 'listToproperty.html',{'form':form})

	else:
		print("method not worked")
		form = list_form()
		args = {'form':form}
		args.update(csrf(request))
		args['form'] = list_form()
		return render(request,  'listToproperty.html',args)

# def follow_user(request, user):
#     user = User.objects.get(username=user)
#     ...
#     dofollow
#     ...

#     notify.send(request.user, recipient=user, actor=request.user
#                 verb='followed you.', nf_type='followed_by_one_user')

#     return YourResponse

def propertycontact(request):
	requests = contact_on_property.objects.all()
	
	paginator = Paginator(requests,7)
	
	page = request.GET.get('page')
	try:
		requests = paginator.page(page)
	except PageNotAnInteger:
		requests = paginator.page(1)
	except EmptyPage:
		requests = paginator.page(paginator.num_pages)
	return render(request,'propertymessages.html',{'requests':requests})

@csrf_protect
@ensure_csrf_cookie
@login_required(login_url='/accounts/login/')
# @user_passes_test(lambda u: u.groups.filter(name='Client').exists())
def listpropertyy(request,**kwargs):
	form = list_form(request.POST,)
	if request.method == 'POST':	
		if form.is_valid():
			form.save()	
			messages.success(request, "Property added successfully")	
			return render(request, 'payments/process_payment.html')
					
			
		else:
			print(form)		
			return render(request, 'ListProperty.html',{'form':form})

	else:
		print("sio method")
		form = list_form()
		args = {'form':form}
		args.update(csrf(request))
		args['form'] = list_form()
		return render(request,  'ListProperty.html',args)

def clientproperties(request):
	props = propety.objects.filter(lister= request.user)
	trans = paypal_payments.objects.filter(client = request.user)
	return render(request,'myproperties.html',{'props':props})

def paypage(request):
	return render(request,'payment.html')

def messagestatus(request):

    message = contact_on_property.objects.all()
    return redirect(request, 'propertymessages.html',{'message':message})

def clientbookings(request):
	props = booked_viewings.objects.filter(name= request.user)
	return render(request,'clientbookings.html',{'props':props})

@ensure_csrf_cookie
@csrf_protect
def agenteditproperty(request,propertytitle):
	propt = propety.objects.all().filter(propertytitle=propertytitle)
	form = list_form(request.POST)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			messages.success("Property updated successfully")
			return render(request,'agent.html',{'form':form})

		else:
			print("Form si valid")
			return render(request,'agenteditproperty.html',{'form':form,'propt':propt})

	else:
		return render(request,'agenteditproperty.html',{'propt':propt,'form':form})



	


@ensure_csrf_cookie
@csrf_protect
def listingrequest(request):
	form = listrequestform(request.POST)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			messages.success(request, "Your message has been sent. Our agent will contact you shortly")
			return render(request,'ListProperty.html',{'form':form})
		
		else:
			return render(request,'ListProperty.html',{'form':form})
	
	else:
		return render(request,'ListProperty.html',{'form':form})


