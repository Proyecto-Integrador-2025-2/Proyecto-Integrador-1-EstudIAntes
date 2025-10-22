# chat/urls.py
from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path('', views.chat_home, name='home'),
    path('ai/', views.ai_query, name='ai_query'),
    path('generate/', views.generate_routine_suggestions, name='generate'),
    path('suggestion/<int:suggestion_id>/', views.view_suggestion, name='view_suggestion'),
    path('suggestion/<int:suggestion_id>/apply/', views.apply_suggestion, name='apply_suggestion'),
    path('routine/', views.list_routine_slots, name='list_routine_slots'),
]
