from rest_framework import viewsets, permissions, generics
from main.models import Category, Tag, Contact, Report
from main.api.serializers import CategorySerializer, TagSerializer, ContactSerializer, ReportSerializer
from main.api.permissions import IsAdminUserOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    # http://127.0.0.1:8000/main/category/
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    # http://127.0.0.1:8000/main/tag/
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class ContactCreateAPIview(generics.CreateAPIView):
    # http://127.0.0.1:8000/main/contact/
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ReportCreateAPIView(generics.ListCreateAPIView):
    # http://127.0.0.1:8000/main/report/
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
