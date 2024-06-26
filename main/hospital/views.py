from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.forms.models import model_to_dict
from django.db import IntegrityError
from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination

from .models import (
    Department,
    Patient,
    Doctor,
    DoctorAvailability,
    MedicalHistory,
    Appointment,
)
from .serializers import DepartmentSerializer, PatientSerializer, DoctorSerializer
from .enum import DayOfWeek


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    pagination_class = LimitOffsetPagination
    lookup_field = "slug"

    def get_queryset(self):
        """Filter using slug"""
        queryset = Department.objects.all()
        slug = self.request.query_params.get("slug", None)
        search = self.request.query_params.get("search", None)
        if slug is not None:
            queryset = queryset.filter(slug=slug)
        elif search is not None:
            queryset = queryset.filter(Q(name__icontains=search))
        return queryset


class DoctorAPIView(APIView, LimitOffsetPagination):
    def post(self, request, *args, **kwargs):
        try:
            payload = request.data
            availability_data = payload.pop("availability", {})

            # Create Doctor Entry
            try:
                doctor = Doctor.objects.create(
                    name=payload["name"],
                    specialization=payload["specialization"],
                    contact_information=payload["contact_information"],
                    department_id=payload["department"],
                )
            except IntegrityError:
                return Response(
                    {"error": "Doctor Already Exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Prepare Availability Data
            availability_instances = []
            for day, timing in availability_data.items():
                try:
                    day_value = DayOfWeek.from_string(day).value
                    availability_instance = DoctorAvailability(
                        doctor=doctor,
                        day=day_value,
                        start_time=timing["start_time"],
                        end_time=timing["end_time"],
                    )
                    availability_instances.append(availability_instance)
                except KeyError:
                    return Response(
                        {"error": "Invalid availability data"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Bulk Create Availability
            DoctorAvailability.objects.bulk_create(availability_instances)

            return Response(model_to_dict(doctor), status=status.HTTP_201_CREATED)
        except Exception as _:
            return Response(
                {"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    def patch(self, request, *args, **kwargs):
        try:
            payload = request.data
            slug = kwargs.get("slug")
            availability_data = payload.pop("availability", {})

            # Update Doctor Entry
            doctor = Doctor.objects.filter(slug=slug)
            if len(doctor) == 0:
                return Response(
                    {"error": "No Doctor matches the given slug."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            doctor.update(**payload)

            # Delete all Doctor Availability
            DoctorAvailability.objects.filter(doctor_id=doctor[0].id).delete()
            # Prepare Availability Data
            availability_instances = []
            for day, timing in availability_data.items():
                try:
                    day_value = DayOfWeek.from_string(day).value
                    availability_instance = DoctorAvailability(
                        doctor_id=doctor[0].id,
                        day=day_value,
                        start_time=timing["start_time"],
                        end_time=timing["end_time"],
                    )
                    availability_instances.append(availability_instance)
                except KeyError:
                    return Response(
                        {"error": "Invalid availability data"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Bulk Create Availability
            DoctorAvailability.objects.bulk_create(availability_instances)

            return Response(
                {"message": "Doctor Details Updated Successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as _:
            return Response(
                {"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, *args, **kwargs):
        try:
            slug = kwargs.get("slug")
            # Get Doctor Details
            try:
                doctor = Doctor.objects.get(slug=slug)
            except Doctor.DoesNotExist:
                return Response(
                    {"error": "No Doctor matches the given slug."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Delete Doctor Entry
            doctor.delete()

            return Response(
                {"message": "Doctor Deleted Successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as _:
            return Response(
                {"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, *args, **kwargs):
        # Initialize the base queryset
        queryset = Doctor.objects.all()

        # Get query params
        slug = kwargs.get("slug")
        search = request.GET.get("search")
        specialization = request.GET.get("specialization")

        # Apply filters based on query params
        if slug:
            queryset = queryset.filter(slug=slug)
        if search:
            queryset = queryset.filter(name__icontains=search)
        if specialization:
            queryset = queryset.filter(specialization=specialization)

        # Paginate the queryset before serialization
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(queryset, request, view=self)

        # Serialize the paginated data
        serializer = DoctorSerializer(result_page, many=True)

        # Return the paginated response
        return paginator.get_paginated_response(serializer.data)


class PatientAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            payload = request.data
            medical_history = payload.pop("medical_history", None)
            # Create Patient Entry
            try:
                patient = Patient.objects.create(
                    name=payload["name"],
                    age=payload["age"],
                    gender=payload["gender"],
                    contact_information=payload["contact_information"],
                    doctor_id=payload["assigned_doctor"],
                )
            except IntegrityError:
                return Response(
                    {"error": "Patient Already Exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Create Medical History Entry
            if medical_history:
                MedicalHistory.objects.create(
                    patient=patient,
                    previous_diagnoses=medical_history["previous_diagnoses"],
                    allergies=medical_history["allergies"],
                    medications=medical_history["medications"],
                )
            return Response(
                {"message": "Patient Created Successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as _:
            return Response(
                {"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    def patch(self, request, *args, **kwargs):
        try:
            slug = kwargs.get("slug")
            payload = request.data
            medical_history = payload.pop("medical_history", None)
            assigned_doctor = payload.pop("assigned_doctor", None)
            if assigned_doctor:
                payload["doctor_id"] = assigned_doctor

            # Update Patient
            patient = Patient.objects.filter(slug=slug)
            if len(patient) == 0:
                return Response(
                    {"error": "No Patient matches the given slug."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            patient.update(**payload)
            # Update Medical History Entry
            if medical_history:
                MedicalHistory.objects.filter(patient_id=patient[0].id).update(
                    **medical_history
                )
            return Response(
                {"message": "Patient Updated Successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return Response(
                {"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, *args, **kwargs):
        try:
            slug = kwargs.get("slug")
            # Create Patient
            try:
                patient = Patient.objects.get(slug=slug)
            except Patient.DoesNotExist:
                return Response(
                    {"error": "No Patient matches the given slug."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            patient.delete()
            return Response(
                {"message": "Patient Deleted Successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return Response(
                {"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, *args, **kwargs):
        queryset = Patient.objects.all()
        # Fetch data from the database
        slug = kwargs.get("slug", None)
        search = request.GET.get("search", None)
        if slug:
            queryset = queryset.filter(slug=slug)
        if search:
            queryset = queryset.filter(name__icontains=search)

        # Paginate the queryset before serialization
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(queryset, request, view=self)

        # Serialize the paginated data
        serializer = PatientSerializer(result_page, many=True)

        # Return the paginated response
        return paginator.get_paginated_response(serializer.data)


class DoctorAppointmentAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            slug = kwargs.get("patient_slug", None)
            payload = request.data
            # Current time
            appointment_date = datetime.strptime(
                payload["date"], "%Y-%m-%d %H:%M:%S.%f"
            )
            day_of_week = appointment_date.weekday()

            # Fetch Patient
            patient = Patient.objects.get(slug=slug)
            doctor_availability = DoctorAvailability.objects.filter(
                doctor_id=patient.doctor, day=day_of_week
            )

            if len(doctor_availability) > 0:
                Appointment.objects.create(
                    patient=patient, date=payload["date"], details=payload["details"]
                )
            return Response(
                {"message": "Appointment Created Successfullly"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as error:
            return Response(
                {"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )
