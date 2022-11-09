from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from . models import Account
# from users.models import UserProfile



# Register your models here.class AccountAdmin(UserAdmin):


class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name',
                    'last_name', 'date_joined', 'last_login', 'is_active')
    list_display_links = ('username', 'email')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
# userprofile address and all





admin.site.register(Account, AccountAdmin)
