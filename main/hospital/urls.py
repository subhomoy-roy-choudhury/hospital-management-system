from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, DoctorAPIView, PatientAPIView

app_name = "Hospital Management"

router = DefaultRouter()
router.register(r"department", DepartmentViewSet, basename="department")

urlpatterns = [
    path("", include(router.urls)),
    re_path(r'^doctor/(?P<slug>[a-zA-Z0-9_-]+)?/?$', DoctorAPIView.as_view(), name='doctor-view'),
    re_path(r'^patient/(?P<slug>[a-zA-Z0-9_-]+)?/?$', PatientAPIView.as_view(), name='patient-view')
]
