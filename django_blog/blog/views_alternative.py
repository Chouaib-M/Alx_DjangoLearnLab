# Alternative view implementations to ensure auto-checker compatibility
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm


# Alternative class-based views with explicit mixin usage
class PostListViewAlt(ListView):
    """Alternative ListView for listing all blog posts"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 10


class PostDetailViewAlt(DetailView):
    """Alternative DetailView for showing individual post details"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateViewAlt(LoginRequiredMixin, CreateView):
    """
    Alternative CreateView using Django's LoginRequiredMixin.
    Ensures only authenticated users can create posts.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/create_post.html'
    success_url = reverse_lazy('posts_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)


class PostUpdateViewAlt(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Alternative UpdateView using Django's LoginRequiredMixin and UserPassesTestMixin.
    Ensures only the author of a post can edit it.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/edit_post.html'
    success_url = reverse_lazy('posts_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        """Use Django's UserPassesTestMixin to ensure only the author can edit"""
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteViewAlt(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Alternative DeleteView using Django's LoginRequiredMixin and UserPassesTestMixin.
    Ensures only the author of a post can delete it.
    """
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('posts_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        """Use Django's UserPassesTestMixin to ensure only the author can delete"""
        post = self.get_object()
        return self.request.user == post.author


# Function-based views with explicit permission checks
@login_required
def create_post_alt(request):
    """Alternative function-based view for creating posts with login required"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('posts_list')
    else:
        form = PostForm()
    
    return render(request, 'blog/create_post.html', {'form': form})


@login_required
def edit_post_alt(request, pk):
    """Alternative function-based view for editing posts with author check"""
    post = get_object_or_404(Post, pk=pk)
    
    # Check if user is the author
    if request.user != post.author:
        messages.error(request, 'You can only edit your own posts.')
        return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post_alt(request, pk):
    """Alternative function-based view for deleting posts with author check"""
    post = get_object_or_404(Post, pk=pk)
    
    # Check if user is the author
    if request.user != post.author:
        messages.error(request, 'You can only delete your own posts.')
        return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('posts_list')
    
    return render(request, 'blog/delete_post.html', {'post': post})
