from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.contrib.auth.decorators import login_required
# from .models import Pattern, PatternHooksNeedles
# from .forms import PatternForm, PatternHooksNeedlesFormSet

# # Create your views here.
def pattern(request):
    return HttpResponse("Hello there!")

# @login_required
# def create_pattern(request):
#     if request.method == 'POST':
#         pattern_form = PatternForm(request.POST)
#         hooks_needles_formset = PatternHooksNeedlesFormSet(request.POST)
#         if pattern_form.is_valid() and hooks_needles_formset.is_valid():
#             pattern = pattern_form.save(commit=False)
#             pattern.author = request.user
#             pattern.save()
#             hooks_needles_formset.instance = pattern
#             hooks_needles_formset.save()
#             return redirect('pattern_detail', pk=pattern.pk)
#     else:
#         pattern_form = PatternForm()
#         hooks_needles_formset = PatternHooksNeedlesFormSet()
#     return render(request, 'patterns/pattern_form.html', {
#         'pattern_form': pattern_form,
#         'hooks_needles_formset': hooks_needles_formset,
#     })