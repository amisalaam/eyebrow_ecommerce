from django.contrib import admin
from .models import UserProfile,Banner,BrandaAd
from django.utils.html import format_html


# Register your models
class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="boarder-radius:50%;" >'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Banner)
admin.site.register(BrandaAd)


