from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Article
from .forms import ArticleForm


class IndexView(View):
    def get(self, request):
        articles = Article.objects.select_related('author').prefetch_related('tags').order_by('-created_at')
        form = ArticleForm() if request.user.is_authenticated else None
        return render(request, 'main/index.html', {'articles': articles, 'form': form})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            form.save_m2m()
            return redirect('index')
        articles = Article.objects.select_related('author').prefetch_related('tags').order_by('-created_at')
        return render(request, 'main/index.html', {'articles': articles, 'form': form})


class ArticleDetailsView(View):
    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        return render(request, 'main/article_detail.html', {'article': article})


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class MyArticlesView(View):
    def get(self, request):
        articles = Article.objects.filter(author=request.user).prefetch_related('tags').order_by('-created_at')
        return render(request, 'main/my_articles.html', {'articles': articles})


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ArticleEditView(View):
    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug, author=request.user)
        form = ArticleForm(instance=article)
        return render(request, 'main/article_edit.html', {'form': form, 'article': article})

    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug, author=request.user)
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', slug=article.slug)
        return render(request, 'main/article_edit.html', {'form': form, 'article': article})


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ArticleDeleteView(View):
    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug, author=request.user)
        return render(request, 'main/article_delete.html', {'article': article})

    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug, author=request.user)
        article.delete()
        return redirect('my_articles')
