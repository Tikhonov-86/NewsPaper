from django.contrib import admin
from .models import Category, Post, MyModel
from modeltranslation.admin import TranslationAdmin  #импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'dateCreation')
    list_filter = ('title', 'text', 'author', 'dateCreation')
    search_fields = ('title', 'text', 'author', 'dateCreation')
    # actions = [runmycommand]


class CategoryAdmin(TranslationAdmin):
    model = Category


class MyModelAdmin(TranslationAdmin):
    model = MyModel


admin.site.register(MyModel)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)