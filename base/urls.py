from django.urls import path
from django.contrib import admin

from base import views

urlpatterns = [
    path('', views.home, name='home'),
    path('wybory/<str:pk>/', views.wybory, name='wybory'),
    # path('wybory_form/', views.formularz_kandydatow, name='wybory_form'),
]

admin.site.site_header = "Wybory"
admin.site.site_title = "Strona administrac wyborów"
admin.site.index_title = "Strona Administracyjna Wyborów"
