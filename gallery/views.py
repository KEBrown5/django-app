from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Posts, Tag
from .forms import PostsForm

from rest_framework import viewsets
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated

from django.db.models import IntegerField, Case, When, Value, Max

# Returns all posts in the database
# @login_required(login_url = 'users:login')
# def home(request):
#     # posts = Posts.objects.all()
#     posts = Posts.objects.filter(author = request.user)
#     return render(request, 'myapp/index.html', {'posts': posts})

# I used AI to help me build the filtering function
@login_required(login_url = 'users:login')
def home(request):
    tags = Tag.objects.all() # Fetch tags for the dropdown
    selected_tag = request.GET.get('tag')
    
    # Filter by author first to limit the dataset
    posts = Posts.objects.filter(author=request.user)

    if selected_tag:
        # We use Max() here because if a post has multiple tags, 
        # we only care if AT LEAST one of them matches (Value 1).
        posts = posts.annotate(
            is_match=Max(Case(
                When(tags__name=selected_tag, then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            ))
        ).order_by('-is_match', '-created_at')
    else: # Otherwise, just order them by the most recent ones
        posts = posts.order_by('-created_at')

    posts = posts.distinct() # Delete duplicates

    context = {
        'posts': posts,
        'tags': tags,
        'selected_tag': selected_tag
    }
    
    return render(request, 'myapp/index.html', context)

# Returns details of a specific post
@login_required(login_url = 'users:login')
def posts_detail(request, pk):
    posts = Posts.objects.get(pk=pk)
    return render(request, 'myapp/index2.html', {'posts': posts})

@login_required(login_url = 'users:login')
def edit_posts(request, pk):
    posts = get_object_or_404(Posts, pk=pk)
    if request.method == 'POST': # If its a post request, the user finished editing and is uploading it
        form = PostsForm(request.POST, request.FILES, instance=posts)
        if form.is_valid():
            form.save()
            return redirect('blogsite:home')
    else: # otherwise if its a get, the user wants to see the edit form
        form = PostsForm(instance=posts)

    return render(request, 'myapp/edit.html', {'form': form})

@login_required(login_url = 'users:login')
def delete_posts(request, pk):
    posts = get_object_or_404(Posts, pk=pk)
    if request.method == 'POST': # If its a post, the user is deleting
        posts.delete()
        return redirect('blogsite:home')
    return render(request, 'myapp/delete.html', {'posts': posts}) # Otherwise, display the page (confirmation page)

@login_required(login_url = 'users:login')
def about(request):
    return render(request, 'myapp/about.html')

@login_required(login_url = 'users:login')
def account(request):
    return render(request, 'myapp/account.html')

@login_required(login_url = 'users:login')
def create(request):
    if request.method != 'POST':
        form = PostsForm()
    else:
        form = PostsForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('blogsite:home')
        
    context = {'form': form}
    
    return render(request, 'myapp/create.html', context)

class PostViewSet(viewsets.ModelViewSet):    
    def get_queryset(self):
        return Posts.objects.filter(author = self.request.user)
    
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
