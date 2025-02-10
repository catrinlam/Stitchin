from django.contrib import admin
from .models import Pattern, PatternHooksNeedle, Favourite, Comment
from django_summernote.admin import SummernoteModelAdmin


class PatternHooksNeedleInline(admin.TabularInline):
    model = PatternHooksNeedle
    extra = 1  # Number of extra forms to display


@admin.register(Pattern)
class PatternAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'author', 'difficulty_level',
                    'craft', 'yarn_weight', 'created_at')
    search_fields = ('title', 'author__username')
    list_filter = ('difficulty_level', 'craft',
                   'yarn_weight', 'size', 'category')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('description',)
    inlines = [PatternHooksNeedleInline]


@admin.register(PatternHooksNeedle)
class PatternHooksNeedleAdmin(admin.ModelAdmin):
    list_display = ('pattern__title', 'type', 'hook_size',
                    'needle_size', 'pattern__author')
    search_fields = ('pattern__title', 'pattern__author__username')
    list_filter = ('pattern', 'type', 'hook_size', 'needle_size')


@admin.register(Favourite)
class FavouritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username', 'pattern__title')
    list_filter = ('created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'pattern', 'created_at')
    search_fields = ('author__username', 'pattern__title')
    list_filter = ('created_at',)
