from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.webhook),
    path('broadcast/', views.broadcast),
    path('broadcast-sise/', views.broadcast_sise),
    
]
