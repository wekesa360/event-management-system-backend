from django.urls import path
from .views import dasboard_view
urlpatterns = [
    path('', dasboard_view, name='home'), # homepage url
]