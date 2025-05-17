from django.urls import path
from .views import FarmerListView, FarmerDetailView

urlpatterns = [
    path('farmers/', FarmerListView.as_view(), name='farmer-list'),
    path('farmers/<int:pk>/', FarmerDetailView.as_view(), name='farmer-detail'),
]
