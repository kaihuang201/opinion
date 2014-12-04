from django import forms

class signinForm(forms.Form):
	username = forms.CharField(
                max_length=30, 
	            widget=forms.TextInput(attrs={
                                'class' : 'form-control',
                                'placeholder' : 'Username',
                            }),
                )

	password = forms.CharField(max_length=30, 
	            widget=forms.PasswordInput(attrs={
                                'class' : 'form-control',
                                'placeholder' : 'Password',
                            }))

class signupForm(signinForm):
	password_again = forms.CharField(max_length=30, 
	            widget=forms.PasswordInput(attrs={'class' : 'form-control',
                                'placeholder' : 'Password Again',
                            }))

class profileEditForm(forms.Form):
     motto = forms.CharField(max_length=200,
                widget=forms.TextInput(attrs={'class':'form-control',
                                'placeholder' : 'Enter Your Motto',
                            }))
class searchForm(forms.Form):
    datepickerAttr = {
                        'class':'datepicker',
                        'data-provide':'datepicker-inline',
                        'data-date-format':'yyyy/mm/dd'
                     }

    after = forms.CharField(label='After', max_length=100, 
                            widget=forms.TextInput(attrs=datepickerAttr))
    before = forms.CharField(label='Before', max_length=100, 
                            widget=forms.TextInput(attrs=datepickerAttr))
    
    title_include = forms.CharField(label='Title Includes', max_length=200,
                widget=forms.TextInput(attrs={'class':'form-control',
                                'placeholder' : 'Please Enter Text',
                            }))
    min_like = forms.IntegerField(label='Number of Likes Greater Than ')


