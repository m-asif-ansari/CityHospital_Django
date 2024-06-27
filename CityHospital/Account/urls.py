from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login_view"),
    path("register/", views.register, name="register"),
    path("patient/", views.patient_register, name="patient_register"),
    path("doctor/", views.doctor_register, name="doctor_register"),
    path("logout/", views.logout_page, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("showdoctor/", views.show_doctor, name="showdoctor"),
    path("appointment/<int:id>", views.book_appointment, name="book_appointment"),
    path("appointment/<int:id>/book", views.book_date, name="book_date"),
    path("slotbooking/<int:id>", views.book_slot, name="book_slot"),
    path(
        "active/", views.patient_active_appointment, name="patient_active_appointment"
    ),
    path("all/", views.patient_all_appointment, name="patient_all_appointment"),
    path("delete/<int:id>", views.delete_appointment, name="delete_appointment"),
    path("print/<int:id>", views.print_appointment, name="print_appointment"),
    path(
        "doctor/active/",
        views.doctor_active_appointment,
        name="doctor_active_appointment",
    ),
    path("doctor/all/", views.doctor_all_appointment, name="doctor_all_appointment"),
]
