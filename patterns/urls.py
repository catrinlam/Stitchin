from . import views
from django.urls import path

urlpatterns = [
    path('', views.PatternList.as_view(), name='home'),
]