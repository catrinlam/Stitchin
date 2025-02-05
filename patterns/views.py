from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from django.db import IntegrityError
from .models import Pattern, PatternHooksNeedle
from .forms import PatternForm, PatternHooksNeedleFormSet

class PatternList(generic.ListView):
    queryset = Pattern.objects.all().order_by('-created_at')
    template_name = "patterns/index.html"
    paginate_by = 6
    
def pattern_detail(request, slug):
    """
    Display an individual :model:`pattern.Pattern`.

    **Context**

    ``pattern``
        An instance of :model:`pattern.Pattern`.

    **Template:**

    :template:`patterns/pattern_detail.html`
    """
    pattern = get_object_or_404(Pattern, slug=slug)
    hooks_needles = pattern.pattern_hooks_needles.all()
    
    needle_displayed = any(hn.needle_size is not None for hn in hooks_needles)
    hook_displayed = any(hn.hook_size is not None for hn in hooks_needles)

    context = {
        'pattern': pattern,
        'hooks_needles': hooks_needles,
        'needle_displayed': needle_displayed,
        'hook_displayed': hook_displayed,
    }
    return render(request, 'patterns/pattern_detail.html', context)

    # queryset = Pattern.objects.all()
    # pattern = get_object_or_404(queryset, slug=slug)
    # hooks_needles = PatternHooksNeedle.objects.filter(pattern=pattern)
    
    # print(hooks_needles.values())

    # return render(
    #     request,
    #     "patterns/pattern_detail.html",
    #     {"pattern": pattern, "hooks_needles": hooks_needles},
    # )

def post_pattern(request):
    if request.method == "POST":
        form = PatternForm(request.POST, request.FILES)
        formset = PatternHooksNeedleFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            try:
                pattern = form.save(commit=False)
                pattern.author = request.user
                pattern.save()
                formset.instance = pattern
                formset.save()
                messages.success(request, "Pattern posted successfully!")
                return redirect('pattern_detail', slug=pattern.slug)
            except Exception as e:
                messages.error(request, f"Error posting pattern: {e}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PatternForm()
        formset = PatternHooksNeedleFormSet()
    return render(request, 'patterns/post_pattern.html', {'form': form, 'formset': formset})