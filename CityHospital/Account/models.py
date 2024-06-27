from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    user_role = [
        ("Patient", "patient"),
        ("Doctor", "doctor"),
    ]

    user_role = models.CharField(max_length=10, choices=user_role)


class Patient(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        to_field="username",
    )
    gender = models.CharField(
        max_length=10,
        choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")),
    )
    age = models.IntegerField()
    contact_no = models.IntegerField()
    address = models.CharField(max_length=100)
    medical_history = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Doctor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        to_field="username",
    )
    gender = models.CharField(
        max_length=10,
        choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")),
    )
    specialization = models.CharField(max_length=100)
    age = models.IntegerField()
    contact_no = models.IntegerField()
    experience = models.IntegerField(default=10)

    def __str__(self):
        return self.user.username


class Appointment(models.Model):
    time_slot = [
        ("09:00", "09:00"),
        ("09:30", "09:30"),
        ("10:00", "10:00"),
        ("10:30", "10:30"),
        ("11:00", "11:00"),
        ("11:30", "11:30"),
        ("12:00", "12:00"),
        ("12:30", "12:30"),
        ("14:00", "14:00"),
        ("14:30", "14:30"),
        ("15:00", "15:00"),
        ("15:30", "15:30"),
        ("16:00", "16:00"),
        ("16:30", "16:30"),
        ("17:00", "17:00"),
        ("17:30", "17:30"),
    ]
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="patient", null=True
    )

    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="doctor", null=True
    )
    date = models.DateField()
    time = models.CharField(max_length=10, choices=time_slot)
    appointment_desc = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.app = str(self.date) + " " + str(self.time)
        try:
            self.appointment_desc = self.app
            super().save(*args, **kwargs)
        except:
            return

    def __str__(self):
        return self.doctor.user.username + " with " + self.patient.user.username
