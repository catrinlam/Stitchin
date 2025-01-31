from django.shortcuts import render, redirect
from django.views import generic
from .models import Pattern, PatternHooksNeedles

class PatternList(generic.ListView):
    model = Pattern
    queryset = Pattern.objects.all()
    template_name = "patterns/patterns_list.html"