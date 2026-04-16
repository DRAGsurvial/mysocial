from django.contrib import admin
from .models import Channel, Article, ArticleLike, ArticleView, Comment


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'slug', 'created_at')
    search_fields = ('title', 'owner__username', 'slug')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'channel', 'author', 'status', 'created_at')
    search_fields = ('title', 'channel__title', 'author__username')
    list_filter = ('status',)


@admin.register(ArticleLike)
class ArticleLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'user', 'created_at')
    search_fields = ('article__title', 'user__username')


@admin.register(ArticleView)
class ArticleViewAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'user', 'session_key', 'created_at')
    search_fields = ('article__title', 'user__username', 'session_key')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'author', 'created_at')
    search_fields = ('article__title', 'author__username', 'text')