from __future__ import unicode_literals
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
from django.contrib.auth import authenticate
from django.utils.safestring import mark_safe
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test
from .tokens import account_activation_token
import json
from django import forms
# Create your views here.
from .forms import loginform,RegistrationForm
from home.models import User
from django.contrib.auth.models import Group
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
# from MySite.models import Profile
# from django.contrib.auth import get_user_model
# user = get_user_model()


@csrf_protect
@ensure_csrf_cookie
def login(request):
	if request.method == 'POST':
		form = loginform(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			user = authenticate(username=username,password=password)
			# next = request.POST.get('next', '/')
			# 	return HttpResponseRedirect(next)
			url = request.path
			next = request.POST.get('next', '/')

			auth_login(request,user)
			if user.groups.filter(name='Agents').exists():
				return HttpResponseRedirect('/agent/')
			if user.groups.filter(name='Clients').exists():
				return HttpResponseRedirect(next)
				
				
		else:
			return render(request, 'registration/login.html',{"form":form})
			
	else:
		form =loginform()
		args = {'form':form}
		args.update(csrf(request))
		args['form'] = loginform
		return render(request,'registration/login.html',args)

@csrf_protect
@ensure_csrf_cookie
def register(request):
	if request.method == 'POST':
		f = RegistrationForm(request.POST)
		if f.is_valid():
			user = f.save()
			user.is_active = False
			user.save()
			group = f.cleaned_data.get('group')
			user.groups.add(group)
			current_site = get_current_site(request)
			message = render_to_string('accounts/activate-email.html',{
			'user':user,
			'domain':current_site.domain,
			'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
			'token':account_activation_token.make_token(user),
			})
			mail_subject = 'Activate your account'
			to_email = f.cleaned_data.get('email')
			email = EmailMessage(mail_subject,message,to=[to_email])
			email.send()
			return redirect('/success/')
			return HttpResponse("Please confirm your email address")
			
			
	else:
		f = RegistrationForm()
		
	return render(request, 'registration/signup.html', {'form': f})

def success(request):
	return render_to_response('accounts/success.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return render(request,'accounts/valid.html')
    else:
    	return render(request,'accounts/invalid.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return render(request,'accounts/valid.html')
    else:
    	return render(request,'accounts/invalid.html')
@csrf_protect
def logout_page(request):
	user = User.objects.get(username='username')
	[s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == user.id]
	logout(request,user)
	return HttpResponseRedirect('/accounts/login/')

@csrf_protect
def forgot_view(request):
	return render(request,'freelance/forgot-password.html')

@csrf_protect
def reset_view(request):
	form = PasswordResetForm(request.POST or None)
	if form.is_valid():
		return render(request,"accounts/referal.html")
	else:
		return render(request,'freelance/forgot-password.html',{"form":form})
def refer_view(request):
	return render(request, 'accounts/referal.html')
