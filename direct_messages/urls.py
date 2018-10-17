from django.urls import path
from . import views
from .views import (
InboxView, ThreadView, CreateDirectMessage, DeleteDirectMessage, ViewDirectMessage
)


urlpatterns = [
    path('inbox/', InboxView.as_view(), name='direct_messages-inbox'),
    path('thread/<str:username>/', ThreadView.as_view(), name='direct_messages-thread'),
    path('new/', CreateDirectMessage.as_view(), name='direct_messages-new'),
    path('<int:pk>/', ViewDirectMessage.as_view(), name='direct_messages-detail'),
    path('<int:pk>/delete/', DeleteDirectMessage.as_view(), name='direct_messages-delete'),
    ]
