from django import forms
from accounts.models import User
from django.forms.widgets import CheckboxInput
from django.utils import timezone

from assets.models import *


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username','profile_pic', 'Address', 'groups', 
                 'Telephone', 'is_admin', 'is_active',
                 'is_staff', 'is_superuser',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['profile_pic'].widget.attrs.update({'class': 'form-control'})
        self.fields['Address'].widget.attrs.update({'class': 'form-control'})
        self.fields['groups'].widget.attrs.update({'class': 'form-control'})
        self.fields['Telephone'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_admin'].widget = CheckboxInput(attrs={'class': 'form-check-input'})
        self.fields['is_admin'].label = 'Is admin?'
        self.fields['is_active'].widget = CheckboxInput(attrs={'class': 'form-check-input'})
        self.fields['is_admin'].label = 'Is active?'
        self.fields['is_staff'].widget = CheckboxInput(attrs={'class': 'form-check-input'})
        self.fields['is_admin'].label = 'Is staff?'
        self.fields['is_superuser'].widget = CheckboxInput(attrs={'class': 'form-check-input'})
        self.fields['is_admin'].label = 'Is superuser?'

        
class ClientMessageForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Message
        fields = ('receiver', 'subject', 'body')

class BroadcastMessageForm(forms.ModelForm):
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'rows': 5}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    class Meta:
        model = BroadcastMessage
        fields = ('subject','message')

class AssetForm(forms.ModelForm):
    

    Date_Assigned = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Assets
        fields = ('Name','Type','Quantity','Model','Serian_Num','Asset_State','Departments','LifeSpan'
        ,'Date_Assigned','Employee','Location','Vendor','Description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Name'].widget.attrs.update({'class': 'form-control'})
        self.fields['Type'].widget.attrs.update({'class': 'form-control'})
        self.fields['Quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['Model'].widget.attrs.update({'class': 'form-control'})
        self.fields['Serian_Num'].widget.attrs.update({'class': 'form-control'})
        self.fields['Asset_State'].widget.attrs.update({'class': 'form-control'})
        self.fields['Departments'].widget.attrs.update({'class': 'form-control'})
        self.fields['LifeSpan'].widget.attrs.update({'class': 'form-control'})
        self.fields['Date_Assigned'].widget.attrs.update({'class': 'form-control'})
        self.fields['Employee'].widget.attrs.update({'class': 'form-control'})
        self.fields['Location'].widget.attrs.update({'class': 'form-control'})
        self.fields['Vendor'].widget.attrs.update({'class': 'form-control'})
        self.fields['Description'].widget.attrs.update({'class': 'form-control'})
