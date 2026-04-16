from django.urls import path
from .views import (
    home_view,
    create_channel_view,
    channel_detail_view,
    delete_channel_view,
    create_article_view,
    article_detail_view,
    toggle_like_view,
    add_comment_view,
    toggle_subscription_view,
    notifications_view,
    subscriptions_feed_view,
)

urlpatterns = [
    path('', home_view, name='home'),
    path('notifications/', notifications_view, name='notifications'),
    path('channels/create/', create_channel_view, name='create_channel'),
    path('c/<slug:slug>/', channel_detail_view, name='channel_detail'),
    path('c/<slug:slug>/delete/', delete_channel_view, name='delete_channel'),
    path('c/<slug:slug>/subscribe/', toggle_subscription_view, name='toggle_subscription'),
    path('c/<slug:channel_slug>/write/', create_article_view, name='create_article'),
    path('c/<slug:channel_slug>/<slug:article_slug>/', article_detail_view, name='article_detail'),
    path('c/<slug:channel_slug>/<slug:article_slug>/like/', toggle_like_view, name='toggle_like'),
    path('c/<slug:channel_slug>/<slug:article_slug>/comment/', add_comment_view, name='add_comment'),
    path('feed/', subscriptions_feed_view, name='subscriptions_feed'),
]