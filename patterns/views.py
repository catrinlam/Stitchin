from django.shortcuts import render, redirect
from django.views import generic
from .models import Pattern

class PatternList(generic.ListView):
    queryset = Pattern.objects.all().order_by('-created_at')
    template_name = "patterns/index.html"
    paginate_by = 6