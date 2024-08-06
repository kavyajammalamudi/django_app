from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Student, Admin, Teacher, CustomUser
from .models import *
from django.contrib.auth import authenticate

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
# Custom User Registration Form
class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'mobile_no', 'is_student', 'is_admin', 'is_teacher']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email

    def clean_mobile_no(self):
        mobile_no = self.cleaned_data.get('mobile_no')
        if mobile_no:
            if CustomUser.objects.filter(mobile_no=mobile_no).exists():
                raise forms.ValidationError('Mobile number is already associated with another user.')
        return mobile_no

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match')

        return cleaned_data

# Login Form
class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        
        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid email or password. Please try again.")
            self.user = user
        return cleaned_data
    
    def get_user(self):
        return self.user
    
######################################################################################

class RequestOTPForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not CustomUser.objects.filter(email=email, is_student=True).exists():
            raise ValidationError("Please Check Email.")
        return email
    
class VerifyOTPForm(forms.Form):
    otp = forms.CharField(max_length=6, min_length=6)

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("The two password fields must match.")
        return cleaned_data

###########################################################################################################

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'image', 'description']

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['course', 'video_url', 'video_name', 'video_des', 'video_number']