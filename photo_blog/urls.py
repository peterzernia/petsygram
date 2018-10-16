from django.urls import path
from . import views
from .views import (
Home, ViewPost, CreatePost,
UpdatePost,DeletePost, ViewProfile,
CreateComment,DeleteComment,
LikePostAPI, ViewLikes, ViewNotifications
)


urlpatterns = [
    path('', Home.as_view(), name='photo_blog-home'),
    path('search/', views.search, name='search'),
    path('post/<int:pk>/', ViewPost.as_view(), name='photo_blog-detail'),
    path('post/new/', CreatePost.as_view(), name='photo_blog-create'),
    path('post/<int:pk>/update', UpdatePost.as_view(), name='photo_blog-update'),
    path('post/<int:pk>/delete/', DeletePost.as_view(), name='photo_blog-delete'),
    path('user/<str:username>/', ViewProfile.as_view(), name='photo_blog-profile'),
    path('post/<int:pk>/comment/', CreateComment.as_view(), name='photo_blog-comment'),
    path('comment/<int:pk>/delete/', DeleteComment.as_view(), name='photo_blog-delete_comment'),
    path('post/<int:pk>/like_api/', LikePostAPI.as_view(), name='photo_blog-post_like_api'),
    path('post/<int:pk>/likes/', ViewLikes.as_view(), name='photo_blog-post_likes'),
    path('notifications/', ViewNotifications.as_view(), name='photo_blog-notifications'),
]
