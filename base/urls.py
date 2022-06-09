from django.urls import path

from base import views

urlpatterns = [
    path('', views.home, name='base'),
    path('wybory/<str:pk>/', views.wybory, name='wybory'),
]

