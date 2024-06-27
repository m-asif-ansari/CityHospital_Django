from django.shortcuts import render, redirect
from .forms import (
    SignUpForm,
    LoginForm,
    PatientRegistrationForm,
    DoctorRegistrationForm,
)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Patient, Doctor, Appointment
from datetime import datetime
from django.contrib import messages


date_obj = datetime.now().date()
time_slot = [
    ("09:00"),
    ("09:30"),
    ("10:00"),
    ("10:30"),
    ("11:00"),
    ("11:30"),
    ("12:00"),
    ("12:30"),
    ("14:00"),
    ("14:30"),
    ("15:00"),
    ("15:30"),
    ("16:00"),
    ("16:30"),
    ("17:00"),
    ("17:30"),
]


def home(request):
    return render(request, "homepage/home.html")


def register(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/login")
        else:
            messages.error(request, "form is not valid")
    return render(request, "registration/register.html", {"form": form})


def patient_register(request):
    if request.method == "POST":
        form = PatientRegistrationForm(request.POST)
        form.user = request.user
        if form.is_valid():
            form.save()
            return redirect("/dashboard")
    else:
        form = PatientRegistrationForm()
    return render(request, "registration/patient/details.html", {"form": form})


def doctor_register(request):
    if request.method == "POST":
        form = DoctorRegistrationForm(request.POST)
        form.user = request.user
        if form.is_valid():
            form.save()
            return redirect("/dashboard")
    else:
        form = DoctorRegistrationForm()
    return render(request, "registration/doctor/details.html", {"form": form})


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None and user.user_role == "Doctor":
                login(request, user)
                doctor_details = Doctor.objects.filter(user=user).exists()
                if doctor_details:
                    return redirect("/dashboard")
                else:
                    return redirect("/doctor")

            elif user is not None and user.user_role == "Patient":
                login(request, user)
                patient_details = Patient.objects.filter(user=user).exists()
                if patient_details:
                    return redirect("/dashboard")
                else:
                    return redirect("/patient")
            else:
                messages.error(request, "invalid username or password")

        else:
            messages.error(request, "error validating form")
    return render(
        request,
        "registration/login.html",
        {"form": form},
    )


@login_required(login_url="login")
def dashboard(request):
    user = request.user
    doctor_list = Doctor.objects.all()
    if user.user_role == "Doctor":
        return redirect("/doctor/active")
    elif user.user_role == "Patient":
        return render(
            request,
            "dashboard/patient_view/book_appointment.html",
            {"doctor": doctor_list},
        )
    return render(request, "dashboard/layout.html", {"user": user})


@login_required(login_url="login")
def show_doctor(request):
    doctor_list = Doctor.objects.all()
    return render(
        request, "dashboard/patient_view/doctor_list.html", {"doctor": doctor_list}
    )


@login_required(login_url="login")
def book_appointment(request, id):
    doctor = Doctor.objects.get(id=id)
    patient = Patient.objects.get(user=request.user)

    return render(
        request,
        "dashboard/patient_view/book_date.html",
        {"doc": doctor, "patient": patient},
    )


@login_required(login_url="login")
def book_date(request, id):
    global date_obj
    date_obj = request.POST["date"]
    patient = Patient.objects.get(user=request.user)
    doctor = Doctor.objects.get(id=id)
    appointment = Appointment.objects.filter(doctor=doctor).filter(date=date_obj).all()
    global time_slot
    booked_slots = [applist.time for applist in appointment]

    return render(
        request,
        "dashboard/patient_view/book_slot.html",
        {
            "doc": doctor,
            "appointment": appointment,
            "time_slot": time_slot,
            "booked_slots": booked_slots,
            "date_obj": date_obj,
            "patient": patient,
        },
    )


@login_required(login_url="login")
def book_slot(request, id):
    doctor = Doctor.objects.get(id=id)
    patient = Patient.objects.filter(user=request.user).get()
    Appointment.objects.create(
        patient=patient, doctor=doctor, date=date_obj, time=request.POST["time"]
    )
    doc = Doctor.objects.all()
    messages.success(request, "Appointment booked successfully")

    return redirect("/active", {"doc": doctor, "messages": messages})


@login_required(login_url="login")
def patient_active_appointment(request):
    patient = Patient.objects.filter(user=request.user).get()
    appointment = (
        Appointment.objects.filter(patient=patient)
        .filter(date__gte=datetime.now().date())
        .order_by("date", "time")
        .all()
    )
    doctor = Doctor.objects.all()
    return render(
        request,
        "dashboard/patient_view/manage_app.html",
        {"appointments": appointment, "patient": patient, "type": "Active"},
    )


@login_required(login_url="login")
def patient_all_appointment(request):
    patient = Patient.objects.filter(user=request.user).get()
    appointment = (
        Appointment.objects.filter(patient=patient).order_by("-date", "time").all()
    )
    return render(
        request,
        "dashboard/patient_view/manage_app.html",
        {"appointments": appointment, "patient": patient, "type": "All"},
    )


@login_required(login_url="login")
def delete_appointment(request, id):
    appointment = Appointment.objects.get(id=id)
    appointment.delete()
    messages.error(request, "Appointment deleted successfully")
    return redirect("/active", messages=messages)


@login_required(login_url="login")
def print_appointment(request, id):
    apointment = Appointment.objects.get(id=id)
    return render(
        request, "dashboard/patient_view/bill.html", {"appointment": apointment}
    )


@login_required(login_url="login")
def doctor_all_appointment(request):
    doctor = Doctor.objects.filter(user=request.user).get()
    appointment = (
        Appointment.objects.filter(doctor=doctor)
        .order_by("-date")
        .order_by("-time")
        .all()
    )
    return render(
        request,
        "dashboard/doctor_view/app_list.html",
        {"doctor": doctor, "appointments": appointment, "type": "All"},
    )


@login_required(login_url="login")
def doctor_active_appointment(request):
    doctor = Doctor.objects.filter(user=request.user).get()
    appointment = (
        Appointment.objects.filter(doctor=doctor)
        .filter(date__gte=datetime.now().date())
        .order_by("date", "time")
        .all()
    )

    return render(
        request,
        "dashboard/doctor_view/app_list.html",
        {"doctor": doctor, "appointments": appointment, "type": "Active"},
    )


def logout_page(request):
    logout(request)
    return redirect("/")
