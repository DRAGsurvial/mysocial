from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db.models import Count

from .forms import ArticleForm, ChannelForm, CommentForm
from .models import Article, Channel, ArticleLike, ArticleView, Comment


def home_view(request):
    articles = Article.objects.filter(status='published').select_related('channel', 'author')[:20]
    featured_channels = Channel.objects.all().order_by('-created_at')[:6]
    return render(request, 'home.html', {'articles': articles, 'featured_channels': featured_channels})


@login_required
def create_channel_view(request):
    if request.method == 'POST':
        form = ChannelForm(request.POST, request.FILES)
        if form.is_valid():
            channel = form.save(commit=False)
            channel.owner = request.user
            channel.save()
            return redirect('channel_detail', slug=channel.slug)
    else:
        form = ChannelForm()
    return render(request, 'channels/create_channel.html', {'form': form})


def channel_detail_view(request, slug):
    channel = get_object_or_404(Channel, slug=slug)
    articles = channel.articles.filter(status='published')
    return render(request, 'channels/channel_detail.html', {'channel': channel, 'articles': articles})


@login_required
def delete_channel_view(request, slug):
    channel = get_object_or_404(Channel, slug=slug, owner=request.user)
    if request.method == 'POST':
        channel.delete()
        return redirect('home')
    return render(request, 'channels/delete_channel.html', {'channel': channel})


@login_required
def create_article_view(request, channel_slug):
    channel = get_object_or_404(Channel, slug=channel_slug, owner=request.user)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.channel = channel
            article.author = request.user
            article.save()
            return redirect('article_detail', channel_slug=channel.slug, article_slug=article.slug)
    else:
        form = ArticleForm()
    return render(request, 'channels/create_article.html', {'form': form, 'channel': channel})


def article_detail_view(request, channel_slug, article_slug):
    article = get_object_or_404(
        Article.objects.select_related('author', 'channel'),
        channel__slug=channel_slug,
        slug=article_slug,
        status='published'
    )

    if not request.session.session_key:
        request.session.create()

    if request.user.is_authenticated:
        ArticleView.objects.get_or_create(article=article, user=request.user)
        user_liked = ArticleLike.objects.filter(article=article, user=request.user).exists()
    else:
        ArticleView.objects.get_or_create(article=article, session_key=request.session.session_key)
        user_liked = False

    comments = article.comments.select_related('author', 'author__profile')
    comment_form = CommentForm()

    recent_commenters = (
        Comment.objects
        .filter(article=article)
        .values('author__profile__avatar')
        .annotate(last_time=Count('id'))
        [:3]
    )

    recent_comment_users = []
    added = set()
    for c in article.comments.select_related('author__profile').order_by('-created_at'):
        if c.author_id not in added:
            recent_comment_users.append(c.author)
            added.add(c.author_id)
        if len(recent_comment_users) == 3:
            break

    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
        'user_liked': user_liked,
        'recent_comment_users': recent_comment_users,
    }
    return render(request, 'channels/article_detail.html', context)


@login_required
@require_POST
def toggle_like_view(request, channel_slug, article_slug):
    article = get_object_or_404(
        Article,
        channel__slug=channel_slug,
        slug=article_slug,
        status='published'
    )

    like, created = ArticleLike.objects.get_or_create(article=article, user=request.user)
    if not created:
        like.delete()

    return redirect('article_detail', channel_slug=channel_slug, article_slug=article_slug)


@login_required
@require_POST
def add_comment_view(request, channel_slug, article_slug):
    article = get_object_or_404(
        Article,
        channel__slug=channel_slug,
        slug=article_slug,
        status='published'
    )

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.author = request.user
        comment.save()

    return redirect('article_detail', channel_slug=channel_slug, article_slug=article_slug)