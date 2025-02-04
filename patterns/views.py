from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Pattern

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