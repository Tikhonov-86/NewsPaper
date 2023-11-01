from django.urls import path
from . import views
from .views import upgrade_user

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('upgrade/', upgrade_user, name='account_upgrade'),
]