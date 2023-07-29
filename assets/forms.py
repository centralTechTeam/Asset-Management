from django.forms import ModelForm

from django import forms 
from .models import *

from accounts.models import User
from django.core.exceptions import ValidationError


class AssetForm(forms.ModelForm):
    
    Date_Acquired = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'date'}))
    Warantee_Start_Date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'date'}))
    Warantee_End_Date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Assets
        fields = ('Name','Type','Quantity','Model','Serian_Num','Asset_State','Departments','LifeSpan'
        ,'Date_Acquired','Date_Assigned','Warantee_Start_Date','Warantee_End_Date','Employee','Location','Vendor','Description')

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
        self.fields['Date_Acquired'].widget.attrs.update({'class': 'form-control', 'placeholder': '1/1/2019'})
        self.fields['Date_Assigned'].widget.attrs.update({'class': 'form-control'})
        self.fields['Warantee_Start_Date'].widget.attrs.update({'class': 'form-control', 'placeholder': '1/1/2019'})
        self.fields['Warantee_End_Date'].widget.attrs.update({'class': 'form-control', 'placeholder': '1/1/2019'})
        self.fields['Employee'].widget.attrs.update({'class': 'form-control'})
        self.fields['Date_Assigned'].widget.attrs.update({'class': 'form-control', 'placeholder': '1/1/2019'})
        self.fields['Location'].widget.attrs.update({'class': 'form-control'})
        self.fields['Vendor'].widget.attrs.update({'class': 'form-control'})
        self.fields['Description'].widget.attrs.update({'class': 'form-control'})

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Company_Name'].widget.attrs.update({'class': 'form-control'})
        self.fields['Name'].widget.attrs.update({'class': 'form-control'})
        self.fields['Business'].widget.attrs.update({'class': 'form-control'})
        self.fields['Address'].widget.attrs.update({'class': 'form-control'})
        self.fields['City'].widget.attrs.update({'class': 'form-control'})
        self.fields['Phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['Email'].widget.attrs.update({'class': 'form-control'})
        self.fields['Website'].widget.attrs.update({'class': 'form-control'})
        self.fields['Country'].widget.attrs.update({'class': 'form-control'})
        
class UserForm(forms.ModelForm):
    Date_of_Birth = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'date'}))
    Departments = forms.ModelChoiceField(queryset=Assign.objects.all(), widget=forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ['user']

        widgets = {

            'Full_Name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'Title': forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}),
            'Phone': forms.TextInput(attrs={'class': 'form-control'}),
            'Address': forms.TextInput(attrs={'class': 'form-control'}),
            'Date_of_Birth': forms.TextInput(attrs={'class': 'form-control'}),
            'Marital_Status': forms.Select(choices=Employee.Status, attrs={'class': 'form-control'}),

        }

################## User Details Form #########################
class UserDetails(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

        widgets = {
            'Full_Name': forms.TextInput(attrs={'class': 'form-control'}),
            'Title': forms.TextInput(attrs={'class': 'form-control'}),
            'Departments': forms.TextInput(attrs={'class': 'form-control'}),
            'Phone': forms.TextInput(attrs={'class': 'form-control'}),
            'Address': forms.TextInput(attrs={'class': 'form-control'}),
            'Date_of_Birth': forms.TextInput(attrs={'class': 'form-control'}),
            'Marital_Status': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SuperUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['Address','Telephone','Date_of_Birth','profile_pic']
        exclude = ['user']

        
        widgets = {
            'Address': forms.TextInput(attrs={'class': 'form-control'}),
            'Telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'Date_of_Birth': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AssetTypesForm(forms.ModelForm):
    class Meta:
        model = Asset_Type
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].widget.attrs.update({'class': 'form-control'})
        
class AssignGroupsForm(forms.ModelForm):
    class Meta:
        model = Assign
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Name'].widget.attrs.update({'class': 'form-control'})
        
class EmployeeForm(forms.ModelForm):
    Date_of_Birth = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'date'}))
    class Meta:
        model = Employee
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Full_Name'].widget.attrs.update({'class': 'form-control'})
        self.fields['user'].widget.attrs.update({'class': 'form-control'})
        self.fields['Title'].widget.attrs.update({'class': 'form-control'})
        self.fields['Departments'].widget.attrs.update({'class': 'form-control'})
        self.fields['Phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['Address'].widget.attrs.update({'class': 'form-control'})
        self.fields['profile_pic'].widget.attrs.update({'class': 'form-control'})
        self.fields['Date_of_Birth'].widget.attrs.update({'class': 'form-control'})
        self.fields['Marital_Status'].widget.attrs.update({'class': 'form-control'})


class MessageForm(forms.ModelForm):
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Message
        fields = ('subject', 'body')