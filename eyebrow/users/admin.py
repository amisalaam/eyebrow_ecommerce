from django.contrib import admin
from .models import UserProfile,Banner,BrandAd
from django.utils.html import format_html


# Register your models
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'state', 'country')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Banner)
admin.site.register(BrandAd)


