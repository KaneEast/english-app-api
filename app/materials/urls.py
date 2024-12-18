from django.urls import path
from .views import MaterialListView

urlpatterns = [
    path('materials/', MaterialListView.as_view(), name='materials-list'),
]
