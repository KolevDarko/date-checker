from django.contrib import admin
from .models import User as MyUser
from django.contrib.auth.admin import UserAdmin

class MyUserAdmin(UserAdmin):
    model = MyUser

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('company',)}),
            (None, {'fields': ('store',)}),
    )

admin.site.register(MyUser, MyUserAdmin)
