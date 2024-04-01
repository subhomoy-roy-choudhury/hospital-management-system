# Create your views here.
from rest_framework import viewsets
from .models import Department
from .serializers import DepartmentSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        """Filter using slug"""
        queryset = Department.objects.all()
        slug = self.request.query_params.get("slug", None)
        if slug is not None:
            queryset = queryset.filter(slug=slug)
        return queryset
