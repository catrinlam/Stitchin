from . import views
from django.urls import path

urlpatterns = [
    path('', views.PatternList.as_view(), name='home'),
    path('favourite/', views.favourite_view, name='favourite'),
    path('post/', views.post_pattern, name='post_pattern'),
    path('<slug:slug>/', views.pattern_detail, name='pattern_detail'),
    path('<slug:slug>/toggle-favourite/',
         views.toggle_favourite, name='toggle_favourite'),
    path('<slug:slug>/edit-comment/<int:comment_id>',
         views.edit_comment, name='edit_comment'),
    path('<slug:slug>/delete-comment/<int:comment_id>',
         views.delete_comment, name='delete_comment'),
    # path('<slug:slug>/edit-pattern/',views.pattern_edit, name='pattern_edit'),
]
