from django.urls import path
from . import views
from .views import CreateDirectMessage, DeleteDirectMessage, ViewDirectMessage


urlpatterns = [
    path('inbox/', views.inbox, name='direct_messages-inbox'),
    path('sent/', views.sent, name='direct_messages-sent'),
    path('new/', CreateDirectMessage.as_view(), name='direct_messages-new'),
    path('<int:pk>/', ViewDirectMessage.as_view(), name='direct_messages-detail'),
    path('<int:pk>/delete/', DeleteDirectMessage.as_view(), name='direct_messages-delete'),
    ]
