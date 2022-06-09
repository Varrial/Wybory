from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from base.models import Wybory, Uprawnieni, Kandydaci

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

admin.site.register(Wybory)
admin.site.register(Uprawnieni)
admin.site.register(Kandydaci)