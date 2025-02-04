from . import views
from django.urls import path

urlpatterns = [
    path('', views.PatternList.as_view(), name='home'),
    path('<slug:slug>/', views.pattern_detail, name='pattern_detail'),
]