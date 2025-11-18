# chat/urls.py
from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path('', views.chat_home, name='home'),
    path('ai/', views.ai_query, name='ai_query'),
    path('ai/update_routine/', views.ai_update_routine, name='ai_update_routine'),
    path('generate/', views.generate_routine_suggestions, name='generate'),
    path('suggestion/<int:suggestion_id>/', views.view_suggestion, name='view_suggestion'),
    path('suggestion/<int:suggestion_id>/apply/', views.apply_suggestion, name='apply_suggestion'),
    path('routine/', views.list_routine_slots, name='list_routine_slots'),
    path('routine/delete/<int:slot_id>/', views.delete_routine_slot, name='delete_routine_slot'),
    path('routine/delete-all/', views.delete_all_routine_slots, name='delete_all_routine_slots'),
]

