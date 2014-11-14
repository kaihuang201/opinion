from django import forms

class signinForm(forms.Form):
	username = forms.CharField(max_length=30, 
	            widget=forms.TextInput(attrs={'class' : 'form-control'}))
	password = forms.CharField(max_length=30, 
	            widget=forms.PasswordInput(attrs={'class' : 'form-control'}))

class signupForm(forms.Form):
	username = forms.CharField(max_length=30, 
	            widget=forms.TextInput(attrs={'class' : 'form-control'}))
	password = forms.CharField(max_length=30, 
	            widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
	password_again = forms.CharField(max_length=30, 
	            widget=forms.PasswordInput(attrs={'class' : 'form-control'}))

