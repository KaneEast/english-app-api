from django.shortcuts import render
from django.db.models import Count
from rest_framework import generics
from .models import Celebrity, Quote
from .serializers import CelebritySerializer, QuoteSerializer

class CelebrityListView(generics.ListAPIView):
    """View for listing celebrities with their quote count"""
    queryset = Celebrity.objects.annotate(quote_count=Count('quotes'))
    serializer_class = CelebritySerializer

class QuoteListView(generics.ListAPIView):
    """View for listing quotes with full celebrity information"""
    queryset = Quote.objects.select_related('celebrity').all()
    serializer_class = QuoteSerializer
