from django import forms

class signinForm(forms.Form):
	username = forms.CharField(max_length=30, 
	            widget=forms.TextInput(attrs={'class' : 'myfieldclass'}))
	password = forms.CharField(max_length=30, 
	            widget=forms.PasswordInput(attrs={'class' : 'myfieldclass'}))

class signupForm(forms.Form):
	username = forms.CharField(max_length=30, 
	            widget=forms.TextInput(attrs={'class' : 'myfieldclass'}))
	password = forms.CharField(max_length=30, 
	            widget=forms.PasswordInput(attrs={'class' : 'myfieldclass'}))
	passwordagain = forms.CharField(max_length=30, 
	            widget=forms.PasswordInput(attrs={'class' : 'myfieldclass'}))

