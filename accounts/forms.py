from django import forms
from django.contrib.auth.forms import UserCreationForm
from home.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from django.contrib.auth import (
authenticate,
get_user_model,
logout,
)



class loginform(forms.Form):
    username = forms.CharField(label="username",max_length=30,widget=forms.TextInput(attrs={'class':'form-control','name':'username'}))
    password = forms.CharField(label="password",max_length=30,widget=forms.PasswordInput(attrs={'class':'form-control','name':'password'}))

    def clean(self,*args,**kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username,password=password)

        user_qs = User.objects.filter(username=username)
        if user_qs.count() == 1:
            user = user_qs.first()
            if not user.is_active:
                raise forms.ValidationError("This user is not active")


        if not user:
            raise forms.ValidationError("This user does not exist")

        if not user.check_password(password):
            raise forms.ValidationError("Incorrect password!")

        if user.groups.filter(name='Client').exists() == False and user.groups.filter(name='Client').exists():
            raise forms.ValidationError("Sorry, you are not permitted to access this page")

        return super(loginform,self).clean(*args,**kwargs)

class RegistrationForm(UserCreationForm):
	group = forms.ModelChoiceField(label ='Account type:',queryset=Group.objects.all(),required=True,widget=forms.Select(attrs={'class':'form-control','name':'group'}))
	first_name = forms.CharField(max_length=30, required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First name','name':'first_name'}))
	last_name = forms.CharField(max_length=30, required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last name','name':'last_name'}))
	username = forms.CharField(label="Username",max_length=30,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your username','name':'username'}))
	mobile_no = forms.IntegerField(required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Mobile No1','name':'mobile1'}))
	location = forms.CharField(max_length=30, required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Location','name':'location'}))
	email = forms.CharField(max_length=75,help_text="Note: Your account activation and password reset links will be sent to this email.", required=True,widget=forms.TextInput(attrs={'class':'form-control','id':'exampleInputEmail1','placeholder':'Enter your email','name':'email'}))
	password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Type in your password','name':'password1'}))
	password2 = forms.CharField(label='Password Confirmation',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Repeat the password above','name':'password2'}))	
	
	class Meta:
		model = User
		fields =('group','first_name','last_name','username','mobile_no','location', 'email','password1','password2')

	def clean_email(self):
		if User.objects.filter(email__iexact=self.cleaned_data['email']):
			raise forms.ValidationError("Sorry ,this email address is already in use.Please supply a different email address or request a password reset.")
		return self.cleaned_data['email']

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Sorry the passwords you entered don't match.Please try again")
		return password2

	def save(self, commit=True):
		user = super(RegistrationForm,self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user