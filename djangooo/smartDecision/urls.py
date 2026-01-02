from django.urls import path
from .views import latest_status

urlpatterns = [
    path('status/', latest_status),
]