from django.urls import path
from config.urls import slash

urlpatterns = [
    path('query/', slash.query, name='query'),
    path('conversation/<str:convo>', slash.conversation, name='conversation'),
]
