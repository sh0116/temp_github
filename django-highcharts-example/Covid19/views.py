import json

from django.db.models import Count, Q
from django.shortcuts import render
from django.http import JsonResponse


def home(request):
    return render(request, 'home.html')
