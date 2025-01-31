from django.contrib import admin
from .models import Pattern, PatternHooksNeedles

class PatternHooksNeedlesInline(admin.TabularInline):
    model = PatternHooksNeedles
    extra = 1  # Number of extra forms to display

class PatternAdmin(admin.ModelAdmin):
    inlines = [PatternHooksNeedlesInline]

admin.site.register(Pattern, PatternAdmin)
admin.site.register(PatternHooksNeedles)