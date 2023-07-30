from django.contrib import admin
from users.models import User, EmailVerification
from products.admin import BasketAdmin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_superuser')
    inlines = (BasketAdmin,)

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'expiration')
    fields = ('user', 'code', 'expiration', 'created')
    readonly_fields = ('created',)
    list_filter = ('user', 'created', 'expiration')
    search_fields = ('user', 'code')








