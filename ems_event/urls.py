from django.urls import path
from .views import dasboard_view, signin_view, logout_view, signup_view
urlpatterns = [
    path('', dasboard_view, name='home'), # homepage url
    path('accounts/login/', signin_view, name='signin'), # login page url
    path('accounts/logout/', logout_view, name='logout'), # logout page url
    path('accounts/signup', signup_view, name='signup'), # signup page url
] 