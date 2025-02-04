from django import forms
from django.utils.text import slugify
from .models import Pattern, PatternHooksNeedle
# from django.core.exceptions import ValidationError

class PatternForm(forms.ModelForm):
    class Meta:
        model = Pattern
        fields = ['title', 'description', 'difficulty_level', 'craft', 'yarn_weight', 'size', 'category', 'image']
        error_messages = {
            'title': {
                'unique': "A pattern with this title already exists. Please choose a different title.",
            },
        }
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.slug = slugify(instance.title)
        if commit:
            instance.save()
        return instance

class PatternHooksNeedleForm(forms.ModelForm):
    class Meta:
        model = PatternHooksNeedle
        fields = ['type', 'hook_size', 'needle_size']