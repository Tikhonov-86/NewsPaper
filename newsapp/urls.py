from .views import subscriptions
from django.urls import path
from . import views


urlpatterns = [
   path('news/', views.PostsList.as_view(), name='news_list'),
   path('news/<int:pk>/', views.PostDetail.as_view(), name='news_detail'),
   path('search/', views.PostSearch.as_view(), name='news_search'),
   path('news/create/', views.PostCreate.as_view(), name='news_create'),
   path('news/<int:pk>/update/', views.PostUpdate.as_view(), name='news_update'),
   path('news/<int:pk>/delete/', views.PostDelete.as_view(), name='news_delete'),

   path('article/', views.ArticleList.as_view(), name='article_list'),
   path('article/<int:id>/', views.ArticleDetail.as_view(), name='article_detail'),
   path('article/create/', views.ArticleCreate.as_view(), name='article_create'),
   path('article/<int:pk>/update/', views.ArticleUpdate.as_view(), name='article_update'),
   path('article/<int:pk>/delete/', views.ArticleDelete.as_view(), name='article_delete'),
   path('subscriptions/', subscriptions, name='subscriptions'),
   # path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),
   path('categories/<int:pk>', views.CategoryListView.as_view(), name='category_list'),
   path('index/', views.Index.as_view()),
]