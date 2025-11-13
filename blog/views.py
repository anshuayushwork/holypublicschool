from django.shortcuts import render, get_object_or_404
from .models import Post, Category

def post_list_view(request):
    """
    Displays a list of all published posts. 
    Also handles filtering by category.
    """
    # Get all categories to display filter buttons
    categories = Category.objects.all()
    
    # Get all published posts initially
    posts = Post.objects.filter(status='published')

    # Check if a 'category' query parameter exists in the URL (e.g., /blog/?category=news)
    category_filter = request.GET.get('category')
    if category_filter:
        # Filter the posts by the category name
        posts = posts.filter(category__name__iexact=category_filter)

    context = {
        'posts': posts,
        'categories': categories,
        'selected_category': category_filter, # To highlight the active filter
    }
    return render(request, 'blog/post_list.html', context)


def post_detail_view(request, uid):
    """
    Displays the full content of a single post, identified by its UID.
    """
    # Retrieve the specific post by its UID, or show a 404 page if not found
    post = get_object_or_404(Post, uid=uid, status='published')
    
    context = {
        'post': post,
    }
    return render(request, 'blog/post_detail.html', context)
