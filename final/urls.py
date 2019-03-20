"""final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path
from django.conf.urls import url,include
from django.contrib.auth import views
from django.contrib.auth import views as auth_views
from accounts.views import (login,register,reset_view,refer_view,success)
from home.views import dashboard,home,subscribe,agentprofile, search, propertycontact,listpropertyy, paypage, listpropetrty, messagestatus, clientbookings,agenteditproperty
# from payment.views import process_payment, payment_done, payment_canceled
from django.urls import path
from django.views.generic import TemplateView
from home.views import listingrequest
from home.views import dashboard,home,subscribe,message,listpropertyy,propertypage, booking
from home.views import agentprofile,clientprofile,clientproperties
from home import views
from payments.views import process_payment, payment_done, payment_canceled

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('home.urls')),
    url(r'^', include('django.contrib.auth.urls')), 
    # path('paypal/', include('paypal.standard.ipn.urls')),
    # url(r'^notifications/', include('notify.urls', 'notifications')),
    url(r'^search/',search,name='search'),
    # url(r'^process-payment/',process_payment,name='payment'),
    # url(r'^payment-done/', payment_done, name='payment_done'),
    # url(r'^payment-canceled/', payment_canceled, name='payment_canceled'),
    url(r'^accounts/login/$',login,name='login'),
    url(r'^agent/',dashboard ,name='dashboard'),
    url(r'^about/$', views.AboutPageView.as_view(),name='about'),
	url(r'^contact/$', views.ContactPageView.as_view(),name='contact'),
	url(r'^properties/$', views.PropertiesPageView.as_view(),name='properties'),
	url(r'^requestedlistings/$', views.ListingsPageView.as_view()),
	url(r'^bookedviewings/$', views.BookingsPageView.as_view()),
	# url(r'^(?P<room_name>[^/]+)/$', views.message, name='room'),
	# url(r'^message/$', message,name='chat'),
	url(r'^property/(?P<propertytitle>[-\w]+)/(?P<pk>\d+)/$', propertypage, name='property'),
	url(r'^propertys/(?P<propertytitle>[-\w]+)/(?P<pk>\d+)/$', booking , name='booking'),
	url(r'^agent/profile/$', agentprofile),
	url(r'^client/profile/$', clientprofile),
	url(r'^myproperties/$', clientproperties),
	# url(r'^/message/', TemplateView.as_view(template_name='message.html'))
	url(r'^register/',register,name='register'),
	url(r'^subscribe/$',subscribe,name='subscribe'),
    url(r'^ListProperty/$', listpropertyy ,name='list_property'),
    url(r'^list/$', listpropetrty ,name='listproperty'),
    url(r'^listrequest/$', listingrequest ,name='listrequest'),
    url(r'^agent/profile/$', agentprofile),
    url(r'^register/',register,name='register'),
    url(r'^subscribe/',subscribe,name='subscribe'),
    url(r'^client-bookings/',clientbookings ,name='clientbookings'),
    url(r'^success/',success,name='success'),
    url(r'^updatemessage/',messagestatus,name='messagestatus'),
    url(r'^agent-edit-property/(?P<propertytitle>[-\w]+)/$',agenteditproperty,name='agentedit'),
    url(r'^reset/',reset_view,name='reset'),
    url(r'^refer/',refer_view,name='refer'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',include('accounts.urls')),
    url(r'^password_reset/$', auth_views.PasswordResetView, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.PasswordResetConfirmView, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView, name='password_reset_complete'),    
    url(r'^property_contacts/',propertycontact,name='propertycontact'),
    url(r'^process-payment/',process_payment,name='payment'),
    url(r'^payment-done/', payment_done, name='payment_done'),
    url(r'^payment-canceled/', payment_canceled, name='payment_canceled'),
    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
