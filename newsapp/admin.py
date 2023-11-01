from django.contrib import admin
from .models import Category, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'dateCreation')
    list_filter = ('title', 'text', 'author', 'dateCreation')
    search_fields = ('title', 'text', 'author', 'dateCreation')
    # actions = [runmycommand]


admin.site.register(Category)
admin.site.register(Post, PostAdmin)