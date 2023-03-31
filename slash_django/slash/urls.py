from django.urls import path
from slash_django.slash.views import query, conversation

urlpatterns = [
    path('query/', query, name='query'),
    path('conversation/<str:convo>', conversation, name='conversation'),
]
