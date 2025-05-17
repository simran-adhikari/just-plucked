from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Blog, Category, Tag

# View to list all Blogs with filtering by category or tag
class BlogListView(ListView):
    model = Blog
    template_name = 'website/blog/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')
        tag_slug = self.kwargs.get('tag_slug')

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)

        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags=tag)

        return queryset

# View to display the details of a specific Blog post
class BlogDetailView(DetailView):
    model = Blog
    template_name = 'website/blog/blog_detail.html'
    context_object_name = 'blog'

# View to display all blogs by a specific author
class AuthorBlogListView(ListView):
    model = Blog
    template_name = 'website/blog/author_blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 5

    def get_queryset(self):
        author = get_object_or_404('auth.User', username=self.kwargs['username'])
        return Blog.objects.filter(author=author)
