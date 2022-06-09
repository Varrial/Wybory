from django.urls import path

from base import views

urlpatterns = [
    path('', views.home, name='home'),
    path('wybory/<str:pk>/', views.wybory, name='wybory'),
    # path('wybory_form/', views.formularz_kandydatow, name='wybory_form'),
]

