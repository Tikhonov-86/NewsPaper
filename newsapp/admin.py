from django.contrib import admin
from .models import Category, Post, Comment
from modeltranslation.admin import TranslationAdmin  #импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'dateCreation')
    list_filter = ('title', 'text', 'author', 'dateCreation')
    search_fields = ('title', 'text', 'author', 'dateCreation')
    # actions = [runmycommand]


class CategoryAdmin(TranslationAdmin):
    model = Category


class CommentAdmin(TranslationAdmin):
    model = Comment


class TransPostAdmin(PostAdmin, TranslationAdmin):
    model = Comment


admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, TransPostAdmin)