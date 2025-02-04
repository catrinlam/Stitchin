from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from django.db import IntegrityError
from .models import Pattern
from .forms import PatternForm

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

    :template:`pattern/pattern_detail.html`
    """

    queryset = Pattern.objects.all()
    pattern = get_object_or_404(queryset, slug=slug)

    return render(
        request,
        "patterns/pattern_detail.html",
        {"pattern": pattern},
    )

def post_pattern(request):
    if request.method == "POST":
        form = PatternForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                pattern = form.save(commit=False)
                pattern.author = request.user
                pattern.save()
                messages.success(request, "Pattern posted successfully!")
                return redirect('pattern_detail', slug=pattern.slug)
            except IntegrityError:
                messages.error(request, "A pattern with this title already exists. Please choose a different title.")
            except Exception as e:
                messages.error(request, f"Error posting pattern: {e}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PatternForm()
    return render(request, 'patterns/post_pattern.html', {'form': form})