from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from base.models import Wybory, Uprawnieni, Kandydaci, TypWyborow

# class AccountInline(admin.StackedInline ):
#     model = Osoba
#     can_delete = False
#     verbose_name_plural = "Osoby"
#
# class CustomizedUserAdmin (UserAdmin):
#     inlines = (AccountInline, )
#
# admin.site.unregister(User)
# admin.site.register(User, CustomizedUserAdmin)

class WyboryAdmin(admin.ModelAdmin):
    fields = ['typ', 'nazwa', 'data_rozpoczecia', 'data_zakonczenia', 'czy_aktywne']
    list_display = ['typ', 'nazwa', 'data_rozpoczecia', 'data_zakonczenia', 'czy_aktywne']

class UprawnieniAdmin(admin.ModelAdmin):
    fields = ['id_wyborow', 'pesel', 'CzyZaglosowal']
    readonly_fields = ('CzyZaglosowal',)
    list_display = ['id_wyborow', 'pesel', 'CzyZaglosowal']

class KandydaciAdmin(admin.ModelAdmin):
    fields = ['id_wyborow', 'pesel', 'poparcie']
    readonly_fields = ('poparcie',)
    list_display = ['id_wyborow', 'pesel', 'poparcie']
    list_filter = ['id_wyborow']

class TypWyborowAdmin(admin.ModelAdmin):
    fields = ['typ']

admin.site.register(Wybory, WyboryAdmin)
admin.site.register(Uprawnieni, UprawnieniAdmin)
admin.site.register(Kandydaci, KandydaciAdmin)
admin.site.register(TypWyborow, TypWyborowAdmin)