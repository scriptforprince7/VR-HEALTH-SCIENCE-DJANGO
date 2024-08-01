from django.contrib import admin
from userauths.models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'email_verified', 'phone_number']
    readonly_fields = ['password', 'email']

class FreeConsultationUsersAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'location']
    readonly_fields = ['email', 'phone', 'name', 'location']


admin.site.register(User, UserAdmin)
admin.site.register(FreeConsultationUsers, FreeConsultationUsersAdmin)
