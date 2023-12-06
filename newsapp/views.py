from datetime import datetime

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from django.core.cache import cache

from django.views.decorators.cache import cache_page

from .filters import PostFilter
from .models import MyModel, Post, Category, Subscription
from .forms import PostForm

from django.db import models
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy  # импортируем «ленивый» геттекст с подсказкой
# from django.utils.translation import activate, get_supported_language_variant

from rest_framework import viewsets
from rest_framework import permissions

from newsapp.serializers import *
from newsapp.models import *

import pytz

import logging

logger = logging.getLogger(__name__)


class Index(View):
    def get(self, request):
        string = _('Hello world')

        return HttpResponse(string)


class Index(View):
    def get(self, request):
        models = MyModel.objects.all()

        context = {
            'models': models,
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones  # добавляем в контекст все доступные часовые пояса
        }

        return HttpResponse(render(request, 'index.html', context))

    # по пост-запросу будем добавлять в сессию часовой пояс,
    # который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/index/')


class AuthorViewset(viewsets.ModelViewSet):
   queryset = Author.objects.all()
   serializer_class = AuthorSerializer


class PostViewset(viewsets.ModelViewSet):
   queryset = Post.objects.all()
   serializer_class = PostSerializer


class CommentViewest(viewsets.ModelViewSet):
   queryset = Comment.objects.all()
   serializer_class = CommentSerializer


class Categories(models.Model):
    name = models.CharField(max_length=100,
                            help_text=_('category name'))  # добавим переводящийся текст подсказку к полю



class PostsList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news_list.html'
    context_object_name = 'Posts'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'Post'
    pk_url_kwarg = 'pk'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


class PostSearch(ListView):
    form_class = PostFilter
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'Posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = "Следующие новости скоро опубликуем!"
        context['filterset'] = self.filterset
        return context


def create_news(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/news/')

    return render(request, 'news_create.html', {'form': form})


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('newsapp.add_news',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('newsapp.change_news',)
    form_class = PostForm
    model = Post
    template_name = 'news_update.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form)


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('newsapp.delete_news',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news_list.html'
    context_object_name = 'Posts'
    paginate_by = 10


class ArticleDetail(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'Post'
    pk_url_kwarg = 'id'


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('newsapp.add_article',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form)


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('newsapp.update_article',)
    form_class = PostForm
    model = Post
    template_name = 'article_update.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form)


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('newsapp.delete_article',)
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('news_list')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.category).order_by('-dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_subscriber'] = Subscription.objects.filter(user=self.request.user, category=self.category).exists()
        context['category'] = self.category
        return context

# @login_required
# def subscribe(request, pk):
#     user = request.user
#     category = Category.objects.get(id=pk)
#     category.subscribers.add(user)
#
#     message = 'Вы успешно подписались на рассылку новостей категории'
#     return render(request, 'subscriptions.html', {'category': category, 'massage': message})
