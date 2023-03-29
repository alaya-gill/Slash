from django.urls import path
from slash_django.slash.views import query

urlpatterns = [
path('query/', query, name='query'),
]