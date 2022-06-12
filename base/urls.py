from django.urls import path
from django.contrib import admin

from base import views

urlpatterns = [
    path('', views.home, name='home'),
    path('wybory/<str:pk>/', views.wybory, name='wybory'),
    path('wyniki/', views.wyniki, name='wyniki'),
    path('wyniki/<str:pk>/', views.konkretne_wyniki, name='konkretne_wyniki'),
    path('zarzadzaj_kandydatami/', views.zarzadzaj_kandydatami, name='zarzadzaj_kandydatami'),
]

admin.site.site_header = "Wybory"
admin.site.site_title = "Strona administrac wyborów"
admin.site.index_title = "Strona Administracyjna Wyborów"
