from django.contrib import admin
from .models import Category, Tag, Blog

# Category admin customization
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # Automatically populate slug from name

# Tag admin customization
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Blog admin customization
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'tags', 'author')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}  # Automatically populate slug from title
 
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Blog, BlogAdmin)
