from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Patient, Doctor


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    email = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "user_role",
        )


class PatientRegistrationForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = (
            "user",
            "gender",
            "age",
            "contact_no",
            "address",
            "medical_history",
        )


class DoctorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = (
            "user",
            "gender",
            "age",
            "contact_no",
            "specialization",
            "experience",
        )
