from rest_framework import serializers
from django.forms.models import model_to_dict
from .models import (
    Department,
    Patient,
    Doctor,
    DoctorAvailability,
    MedicalHistory,
    Appointment,
)
from .enum import DayOfWeek


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = ["day", "start_time", "end_time"]


class DoctorSerializer(serializers.ModelSerializer):
    department_details = DepartmentSerializer(source="department", read_only=True)
    availability = serializers.SerializerMethodField()
    assigned_patients = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = [
            "name",
            "specialization",
            "contact_information",
            "department_details",
            "availability",
            "assigned_patients",
        ]

    def get_availability(self, obj):
        availabilities = DoctorAvailability.objects.filter(doctor=obj)
        availabilities_data = DoctorAvailabilitySerializer(
            availabilities, many=True
        ).data
        return {
            DayOfWeek.get_day_by_number(availability["day"]).lower(): {
                "start_time": availability["start_time"],
                "end_time": availability["end_time"],
            }
            for availability in availabilities_data
        }

    def get_assigned_patients(self, obj):
        assigned_patients = Patient.objects.filter(doctor=obj)
        return [
            model_to_dict(assigned_patient) for assigned_patient in assigned_patients
        ]


class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = ["previous_diagnoses", "allergies", "medications"]


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = ["date", "details"]


class PatientSerializer(serializers.ModelSerializer):
    medical_history = serializers.SerializerMethodField()
    appointments = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            "name",
            "age",
            "gender",
            "contact_information",
            "medical_history",
            "appointments",
            "doctor",
        ]

    def get_medical_history(self, obj):
        medical_histories = MedicalHistory.objects.get(patient=obj)
        medical_histories_serializer = MedicalHistorySerializer(medical_histories)
        return medical_histories_serializer.data

    def get_appointments(self, obj):
        appointments = Appointment.objects.filter(patient=obj)
        appointments_serializer = AppointmentSerializer(appointments, many=True)
        return appointments_serializer.data

    def get_doctor(self, obj):
        return model_to_dict(obj.doctor)
