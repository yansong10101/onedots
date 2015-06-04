__author__ = 'zys'
from django import forms
from designweb.models import UserProfile


class UserProfileForm(forms.Form):
    # designer_type = forms.CharField(max_length=50, label='Designer Type', help_text='Please enter the type')
    first_name = forms.CharField(max_length=50, label='First Name')
    last_name = forms.CharField(max_length=50, label='Last Name')
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICE, label='Gender')
    address1 = forms.CharField(max_length=50, label='Address 1')
    address2 = forms.CharField(max_length=50, label='Address 2')
    city = forms.CharField(max_length=20, label='City')
    state = forms.CharField(max_length=2, label='State')
    zip = forms.CharField(max_length=9, label='Zip Code')

    class Meta:
        model = UserProfile
        fields = ('designer_type', 'gender', 'address1', 'address2', 'city', 'state', 'zip', )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={
        'class': 'full-width has-padding has-border', 'placeholder': 'E-Mail', }))
    password = forms.CharField(max_length=25, label='', widget=forms.TextInput(attrs={
        'class': 'full-width has-padding has-border', 'placeholder': 'Password', 'type': 'password'}))


class SignupForm(forms.Form):
    username = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={
        'class': 'full-width has-padding has-border', 'placeholder': 'E-Mail', }))
    password1 = forms.CharField(max_length=25, label='', widget=forms.TextInput(attrs={
        'class': 'full-width has-padding has-border', 'placeholder': 'Password', 'type': 'password'}))
    password2 = forms.CharField(max_length=25, label='', widget=forms.TextInput(attrs={
        'class': 'full-width has-padding has-border', 'placeholder': 'Confirm Password', 'type': 'password'}))


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=25, label='Old Password')
    password = forms.CharField(max_length=25, label='New Password')
    password2 = forms.CharField(max_length=25, label='Confirm Password')
