from django.urls import path, include
from rest_framework.routers import DefaultRouter
from addresses import views

router = DefaultRouter()
router.register(r'addresses', views.AddressViewSet, basename="addresses")

urlpatterns = [
    path('', include(router.urls)),
]
