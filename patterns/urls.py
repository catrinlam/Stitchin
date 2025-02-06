from . import views
from django.urls import path

urlpatterns = [
    path('', views.PatternList.as_view(), name='home'),
    path('library/', views.library_view, name='library'),
    path('post/', views.post_pattern, name='post_pattern'),
    path('<slug:slug>/', views.pattern_detail, name='pattern_detail'),
    path('<slug:slug>/add_to_library/', views.add_to_library, name='add_to_library'),
]