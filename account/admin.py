from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'image')
    raw_id_fields = ('user',)

admin.site.register(Profile, ProfileAdmin)   # register th user extension model to the admin site.