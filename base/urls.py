from django.urls import path
from django.contrib import admin

from base import views

urlpatterns = [
    path('', views.home, name='home'),
    path('wybory/<str:pk>/', views.wybory, name='wybory'),
    path('wyniki/', views.wyniki, name='wyniki'),
    path('wyniki/<str:pk>/', views.konkretne_wyniki, name='konkretne_wyniki'),
    path('zarzadzaj_kandydatami/', views.zarzadzaj_kandydatami, name='zarzadzaj_kandydatami'),
    path('zarzadzaj_kandydatami/<str:pk>/', views.zarzadzaj_kandydatami_users, name='zarzadzaj_kandydatami_users'),
    path('zarzadzaj_uprawnionymi/', views.zarzadzaj_uprawnionymi, name='zarzadzaj_uprawnionymi'),
    path('zarzadzaj_uprawnionymi/<str:pk>/', views.zarzadzaj_uprawnionymi_users, name='zarzadzaj_uprawnionymi_users'),
    path('dodaj_wybory/', views.dodaj_wybory, name='dodaj_wybory'),
    path('zarzadzaj_wyborami/', views.zarzadzaj_wyborami, name='zarzadzaj_wyborami')
]

admin.site.site_header = "Wybory"
admin.site.site_title = "Strona administrac wyborów"
admin.site.index_title = "Strona Administracyjna Wyborów"
