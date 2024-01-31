from django.urls import path, include
from main.api.views import CategoryViewSet, TagViewSet, ContactCreateAPIview
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'tag', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
    path('contact/', ContactCreateAPIview.as_view())
]
