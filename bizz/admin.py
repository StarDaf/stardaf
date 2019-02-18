from django.contrib import admin
from .models import Shop, Product, Post
# from comment.admin import CommentAdminTable

# class ProductTable(admin.TabularInline):
#     list_display = ('shop', 'name', 'category', 'price', 'stock', 'created', 'updated', 'available')
#     list_filter = ('created', 'updated', 'available')
#     list_editable = ('price', 'stock', 'available')
#     raw_id_fields = ('shop',)
#     model = Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('shop', 'name', 'category', 'price', 'stock', 'created', 'updated', 'available', 'video')
    list_filter = ('created', 'updated', 'available')
    list_editable = ('price', 'stock', 'available')
    raw_id_fields = ('shop',)
    prepopulated_fields = {'slug':('shop',)}
    # inlines=[CommentAdminTable]

admin.site.register(Product, ProductAdmin)



class ShopAdmin(admin.ModelAdmin):
    list_display = ('owner', 'business_name', 'business_address', 'home_address', 'shop_address','created')
    list_filter = ('business_address', 'home_address', 'shop_address', 'created')
    raw_id_fields = ('owner',)
    # inlines = [ProductTable]

admin.site.register(Shop, ShopAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created', 'image', 'video')
    list_filter = ('user', 'created')
    raw_id_fields = ('user',)

admin.site.register(Post, PostAdmin)    


