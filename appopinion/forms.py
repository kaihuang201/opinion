from django import forms

class signinForm(forms.Form):
	username = forms.CharField(
                max_length=30, 
	            widget=forms.TextInput(attrs={
                                'class' : 'form-control'}),
                validators=[validators.validate_slug])

	password = forms.CharField(max_length=30, 
	            widget=forms.PasswordInput(attrs={
                                'class' : 'form-control'}))

class signupForm(signinForm):
	password_again = forms.CharField(max_length=30, 
	            widget=forms.PasswordInput(attrs={'class' : 'form-control'}))

class profileEditForm(forms.Form):
     motto = forms.CharField(max_length=200,
                widget=forms.TextInput(attrs={'class':'form-control'}))
