from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Pattern, Favourite, Comment
from .forms import PatternForm, PatternHooksNeedleFormSet, CommentForm
from django.db.models import Q


class PatternList(generic.ListView):
    """
    View to list all patterns, with optional search functionality.
    Patterns are ordered by creation date in descending order.
    Pagination is set to 8 patterns per page.
    """
    queryset = Pattern.objects.all().order_by('-created_at')
    template_name = "patterns/index.html"
    paginate_by = 8

    def get_queryset(self):
        """
        Override the default queryset to include search functionality.
        Filters patterns by title or author's username if a search query is
        provided.
        """
        query = self.request.GET.get('q')
        if query:
            return Pattern.objects.filter(
                Q(title__icontains=query) | Q(
                    author__username__icontains=query)
            ).order_by('-created_at')
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        """
        Add additional context to the template.
        If the user is authenticated, include their favourite patterns in the
        context.
        """
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            favourite = Favourite.objects.get(user=self.request.user)
            context['favourite_patterns'] = favourite.pattern.all()
        else:
            context['favourite_patterns'] = []
        context['search_query'] = self.request.GET.get('q', '')
        return context


def pattern_detail(request, slug):
    """
    View to display the details of a specific pattern.
    Includes hooks and needles associated with the pattern, comments, and a
    form to add new comments.
    If the user is authenticated, their favourite patterns are also included
    in the context.

    Args:
        request (HttpRequest): The request object.
        slug (str): The slug of the pattern to display.

    Returns:
        HttpResponse: The rendered template for the pattern detail page.
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
    View to add or remove a pattern from the user's favourites.
    If the pattern is already in the user's favourites, it will be removed.
    If the pattern is not in the user's favourites, it will be added.

    Args:
        request (HttpRequest): The request object.
        pattern_id (int): The ID of the pattern to toggle in favourites.

    Returns:
        HttpResponseRedirect: Redirects to the pattern detail page.
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
    """
    View to display the user's favourite patterns.
    Retrieves the patterns that the user has marked as favourites and displays
    them in a list.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered template for the favourite patterns page.
    """
    favourite = Favourite.objects.get(user=request.user)
    patterns = favourite.pattern.all()
    return render(request, 'favourite/favourite.html', {'patterns': patterns})


@login_required
def edit_comment(request, slug, comment_id):
    """
    Handle the editing of a comment on a pattern.
    This view handles the POST request to edit an existing comment on a
    pattern.
    It ensures that the comment belongs to the user making the request and that
    the form data is valid before saving the updated comment.
    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The slug of the pattern to which the comment belongs.
        comment_id (int): The ID of the comment to be edited.
    Returns:
        HttpResponseRedirect: Redirects to the pattern detail page after
        processing the form.
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
    Delete a comment if the request user is the author of the comment.
    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The slug of the pattern to which the comment belongs.
        comment_id (int): The ID of the comment to be deleted.
    Returns:
        HttpResponseRedirect: Redirects to the pattern detail page.
    Raises:
        Http404: If the comment with the given ID does not exist.
    """
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
    Handle the posting of a new pattern.
    This view handles both GET and POST requests. On GET requests, it renders
    a form for creating a new pattern. On POST requests, it processes the form
    data and saves the new pattern if the form is valid.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The HTTP response object with the rendered template or a
        redirect.
    Raises:
        Exception: If there is an error while saving the pattern.
    Templates:
        patterns/post_pattern.html: The template for posting a new pattern.
    Context:
        form (PatternForm): The form for creating a new pattern.
        formset (PatternHooksNeedleFormSet): The formset for adding hooks and
        needles to the pattern.
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
