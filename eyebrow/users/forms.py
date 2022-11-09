
from django import forms
from .models import UserProfile
from my_admin.models import Account


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')
        widgets = {
                    'first_name' : forms.TextInput(attrs={'class':'form-control col-12'}),
                    'last_name' : forms.TextInput(attrs={'class':'form-control col-12'}),
                    'phone_number':forms.TextInput(attrs={'class':'form-control col-12'}),    
        }
                    
        


class UserProfileForm(forms.ModelForm):
    profile_picture=forms.ImageField(required=False, error_messages= {'invalid':{"Image files only"}},widget=forms.FileInput)
    class Meta:

        model = UserProfile
        fields = ('address_line_1','address_line_2','city','state','country','profile_picture')
        widgets = {
                    'address_line_1' : forms.TextInput(attrs={'class':'form-control col-12'}),
                    'address_line_2' : forms.TextInput(attrs={'class':'form-control col-12'}),
                    'city':forms.TextInput(attrs={'class':'form-control col-12'}), 
                    'state':forms.TextInput(attrs={'class':'form-control col-12'}),
                    'country':forms.TextInput(attrs={'class':'form-control col-12'}),
                    
                    

        }
                    
        
