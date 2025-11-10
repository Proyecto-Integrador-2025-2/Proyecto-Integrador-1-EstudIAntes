from django.urls import path
from . import views

app_name = "content"

urlpatterns = [
    path("desafios/", views.challenges_list, name="challenges_list"),
    path("desafios/<slug:slug>/", views.challenge_detail, name="challenge_detail"),
    path("historias/", views.stories_list, name="stories_list"),
    path("historias/<slug:slug>/body/", views.story_body_partial, name="story_body_partial"),
]
