from django.contrib import admin
from.models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'email', 'body', 'active', 'created', 'updated')
    list_Filter = ('active', 'created', 'updated')
    raw_id_fields = ('product', 'user')

admin.site.register(Comment, CommentAdmin)
