from django.contrib import admin
from .models import Action

class ActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'verb', 'target', 'created')
    list_filter = ('created',)
    raw_id_fields = ('user',)
    date_hierarchy = 'created'

admin.site.register(Action, ActionAdmin)