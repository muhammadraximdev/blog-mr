from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.IndexView.as_view(), name='index'),
    path('articles/<slug:slug>/', views.ArticleDetailsView.as_view(), name='article_detail'),
    path('my-articles/', views.MyArticlesView.as_view(), name='my_articles'),
    path('articles/<slug:slug>/edit/', views.ArticleEditView.as_view(), name='article_edit'),
    path('articles/<slug:slug>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
]
