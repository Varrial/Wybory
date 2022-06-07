from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('wybory/<str:pk>/', views.wybory, name='wybory'),
]

