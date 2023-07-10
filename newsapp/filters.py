import django_filters
from django_filters import FilterSet, ModelChoiceFilter, IsoDateTimeFilter
from django.forms import DateTimeInput
from .models import *


class PostFilter(FilterSet):
    model = Post
    fields = {'title', 'Category', 'dateCreation'}
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок',
    )
    search_category = ModelChoiceFilter(
        field_name='postCategory',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Все категории',
    )
    date = django_filters.IsoDateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label='Дата',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        )
    )
