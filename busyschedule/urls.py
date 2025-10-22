# busyschedule/urls.py
from django.urls import path
from . import views

app_name = "busyschedule"  # 👈 este nombre DEBE ser igual al usado en tus templates

urlpatterns = [
    path('', views.schedule_home, name='schedule_home'),
    path('edit/<int:pk>/modal/', views.edit_schedule_modal, name='edit_schedule_modal'),
    path('delete/<int:pk>/', views.delete_schedule, name='delete_schedule'),
    path('delete-block/<int:pk>/', views.delete_block, name='delete_block'),
]
