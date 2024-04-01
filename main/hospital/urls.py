from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet

app_name = "Hospital Management"

router = DefaultRouter()
router.register(r"departments", DepartmentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
