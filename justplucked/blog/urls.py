from django.urls import path
from .views import BlogListView, BlogDetailView, AuthorBlogListView

urlpatterns = [
    path('blogs/', BlogListView.as_view(), name='blog-list'),
    path('blogs/category/<slug:category_slug>/', BlogListView.as_view(), name='blog-list-by-category'),
    path('blogs/tag/<slug:tag_slug>/', BlogListView.as_view(), name='blog-list-by-tag'),
    path('blogs/<slug:slug>/', BlogDetailView.as_view(), name='blog-detail'),
    path('author/<str:username>/blogs/', AuthorBlogListView.as_view(), name='author-blog-list'),
]
