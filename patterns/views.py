from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def pattern(request):
    return HttpResponse("Hello there!")