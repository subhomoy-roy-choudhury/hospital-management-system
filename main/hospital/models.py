from django.db import models
from django.utils.text import slugify
from django.core.validators import RegexValidator
from .enum import DayOfWeek, Gender

# Phone Number Regex
phone_regex = RegexValidator(
    regex=r"^\+?\d{1,3}?\d{9,15}$",
    message="Phone number must be entered in a valid format. Up to 15 digits allowed.",
)


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    services_offered = models.TextField()
    slug = models.SlugField(null=True, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Doctor(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(null=True, unique=True, db_index=True)
    specialization = models.CharField(max_length=100)
    contact_information = models.CharField(validators=[phone_regex], max_length=255)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class DoctorAvailability(models.Model):
    day = models.IntegerField(choices=DayOfWeek.choices())
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        day_string = dict(self.DAY_CHOICES).get(self.day)
        return f"{self.doctor.name} available on {day_string} from {self.start_time} to {self.end_time}"


class Patient(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(null=True, unique=True, db_index=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=Gender.choices())
    contact_information = models.CharField(validators=[phone_regex], max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    previous_diagnoses = models.TextField()
    allergies = models.TextField()
    medications = models.TextField()

    def __str__(self):
        return f"Medical History of {self.patient.name}"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    details = models.TextField()

    def __str__(self):
        return f"Appointment on {self.date} for {self.patient.name}"
