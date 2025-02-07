from . import views
from django.urls import path

urlpatterns = [
    path('', views.PatternList.as_view(), name='home'),
    path('favourite/', views.favourite_view, name='favourite'),
    path('post/', views.post_pattern, name='post_pattern'),
    path('<slug:slug>/', views.pattern_detail, name='pattern_detail'),
    path('<slug:slug>/toggle-favourite/', views.toggle_favourite, name='toggle_favourite'),
]