"""
URL configuration for schedule project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from busyschedule.views import main_home, routine_view

urlpatterns = [
    path('', main_home, name='home'),
    path('horarios/', include(('busyschedule.urls', 'busyschedule'), namespace='busyschedule')),
    # Redirigir /rutina/ a la vista de chat/routine para mantener compatibilidad
    # path('rutina/', routine_view, name='routine'),  # Comentado, ahora se usa chat:list_routine_slots
    path('contenido/', include(('content.urls', 'content'), namespace='content')),
    path('chat/', include(('chat.urls', 'chat'), namespace='chat')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('admin/', admin.site.urls),
]

