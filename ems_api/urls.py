from django.urls import path, include
from rest_framework import routers
from .views import AuthViewSet, EventViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('api/auth', AuthViewSet, basename='auth')
router.register('api', EventViewSet, basename='event')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
