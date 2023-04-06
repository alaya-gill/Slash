from django.urls import path
from config.urls import slash

urlpatterns = [
    path('query/', slash.query, name='query'),
    path('get_level_data/<str:level>/<int:id>', slash.get_level_data, name='get_level_data'),
    path('conversation/<str:convo>', slash.conversation, name='conversation'),
]
