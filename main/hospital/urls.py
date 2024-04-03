from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import (
    DepartmentViewSet,
    DoctorAPIView,
    PatientAPIView,
    DoctorAppointmentAPIView,
)

app_name = "Hospital Management"

router = DefaultRouter()
router.register(r"department", DepartmentViewSet, basename="department")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "patient/<slug:slug>/appointment/",
        DoctorAppointmentAPIView.as_view(),
        name="doctor-appointment",
    ),
    re_path(
        r"^doctor/(?P<slug>[a-zA-Z0-9_-]+)?/?$",
        DoctorAPIView.as_view(),
        name="doctor-view",
    ),
    re_path(
        r"^patient/(?P<slug>[a-zA-Z0-9_-]+)?/?$",
        PatientAPIView.as_view(),
        name="patient-view",
    ),
]
