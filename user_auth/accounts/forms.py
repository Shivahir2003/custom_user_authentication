from django import forms
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.models import UserProfile

class UserSignUpForm(UserCreationForm):
    """ User Register form 

        extends:
            UserCreationForm
    """
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

    def clean_password1(self):
        password = self.cleaned_data['password1']
        if len(password)<8:
            self.add_error("password1","password must be 8 characters long")
        return password

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            self.add_error("password2","Password does not match")
        return password2


class UserProfileForm(forms.Form):
    mobile_number = forms.CharField(max_length=10,required=True)
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES,required=True)
    user_image = forms.FileField(required=False)

    def clean_mobile_number(self):
        mobile_number= self.cleaned_data['mobile_number']

        if len(mobile_number) < 10:
            self.error("mobile number must be 10 digit")
        elif not mobile_number.isnumeric():
            self.error("mobile number must be numeric")
        return mobile_number

class UserLoginForm(forms.Form):
    """ User Login form """
    username = forms.CharField(max_length=65,required=True)
    password = forms.CharField(max_length=65,
                               required=True,
                               widget=forms.PasswordInput())


class ChangePasswordForm(forms.Form):
    """Change password form"""
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())


    def clean_new_password(self):
        new_password=self.cleaned_data['new_password']

        if new_password and len(new_password)<8:
            self.add_error("new_password","password must be 8 characters long")
        return new_password
    def clean_confirm_password(self):
        new_password=self.cleaned_data['new_password']
        confirm_password=self.cleaned_data['confirm_password']

        if new_password!=confirm_password:
            self.add_error("confirm_password","does not match with new password")
        return confirm_password

