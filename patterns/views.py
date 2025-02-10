from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Pattern, Favourite, Comment
from .forms import PatternForm, PatternHooksNeedleFormSet, CommentForm


class PatternList(generic.ListView):
    queryset = Pattern.objects.all().order_by('-created_at')
    template_name = "patterns/index.html"
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            favourite = Favourite.objects.get(user=self.request.user)
            context['favourite_patterns'] = favourite.pattern.all()
        else:
            context['favourite_patterns'] = []
        return context


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

    comments = pattern.comments.all().order_by("-created_at")
    comment_count = pattern.comments.count()

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.pattern = pattern
            comment.save()
            messages.success(request, "Comment posted successfully!")

    comment_form = CommentForm()

    favourite_patterns = []
    if request.user.is_authenticated:
        favourite = Favourite.objects.get(user=request.user)
        favourite_patterns = favourite.pattern.all()

    context = {
        'pattern': pattern,
        'hooks_needles': hooks_needles,
        'needle_displayed': needle_displayed,
        'hook_displayed': hook_displayed,
        'favourite_patterns': favourite_patterns,
        "comments": comments,
        "comment_count": comment_count,
        "comment_form": comment_form,
    }
    return render(request, 'patterns/pattern_detail.html', context)


@login_required
def toggle_favourite(request, slug):
    """
    View to add or remove patterns from favourites
    """
    pattern = get_object_or_404(Pattern, slug=slug)
    favourite = Favourite.objects.get(user=request.user)

    if favourite.pattern.filter(id=pattern.id).exists():
        favourite.pattern.remove(pattern)
        messages.success(request, f"{pattern.title} removed from favourites.")
    else:
        favourite.pattern.add(pattern)

    return HttpResponseRedirect(
        request.META.get(
            'HTTP_REFERER', reverse('pattern_detail', args=[slug])
        )
    )


@login_required
def favourite_view(request):
    favourite = Favourite.objects.get(user=request.user)
    patterns = favourite.pattern.all()
    return render(request, 'favourite/favourite.html', {'patterns': patterns})


@login_required
def edit_comment(request, slug, comment_id):
    """
    view to edit comments
    """
    if request.method == "POST":

        pattern = get_object_or_404(Pattern, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.pattern = pattern
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(
                request, messages.ERROR, 'Error updating comment!'
            )

    return HttpResponseRedirect(reverse('pattern_detail', args=[slug]))


@login_required
def delete_comment(request, slug, comment_id):
    """
    view to delete comment
    """
    # pattern = get_object_or_404(Pattern, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(
            request, messages.ERROR, 'You can only delete your own comments!'
        )

    return HttpResponseRedirect(reverse('pattern_detail', args=[slug]))


@login_required
def post_pattern(request):
    """
    View to upload patterns
    """
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
    return render(
        request,
        'patterns/post_pattern.html',
        {'form': form, 'formset': formset}
    )
