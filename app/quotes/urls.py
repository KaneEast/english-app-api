from django.urls import path
from .views import CelebrityListView, QuoteListView

urlpatterns = [
    path('celebrities/', CelebrityListView.as_view(), name='celebrity-list'),
    path('quotes/', QuoteListView.as_view(), name='quote-list'),
]
