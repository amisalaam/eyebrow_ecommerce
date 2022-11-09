from django import forms

from my_admin.models import Account
from .models import  RegForm


class UserSignin(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'password']
        widgets = {
                    'email' : forms.TextInput(attrs={'class':'form-control col-12'}),
                    'password' : forms.PasswordInput(render_value=True,attrs={'class':'form-control col-12' } )
                }


class UserSignup(forms.ModelForm):
    Confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control col-12' ,'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control col-12' ,'class':'form-control'}))
    class Meta:
        model = Account
        fields = [ 'first_name', 'last_name','email','username','phone_number', 'password']
        widgets = {
                    'username' : forms.TextInput(attrs={'class':'form-control col-12'}),
                    'email' : forms.TextInput(attrs={'class':'form-control col-12'}),
                    'first_name' : forms.TextInput(attrs={'class':'form-control col-12'}),
                    'last_name' : forms.TextInput(attrs={'class':'form-control col-12'}),
                    'phone_number':forms.TextInput(attrs={'class':'form-control col-12'}),    
                    
                    
                    
                }
def clean(self):
    cleaned_data = super(UserSignup,self).clean()    
    password=cleaned_data.get('password')
    confirm_password=cleaned_data.get('confirm_password') 

    if password != confirm_password:
        raise forms.ValidationError( 'password does not match')                            
