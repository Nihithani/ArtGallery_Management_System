from django.contrib import admin
from .models import *

#Configuring Artists admin panel
class ArtistsAdmin(admin.ModelAdmin):
    list_display=('name', 'about_artist', 'image_tag') #displays the mentioned categories from the database table= artists on to the Artists admin panel
    search_fields= ('title',)

#configuring arts admin panel
class ArtsAdmin(admin.ModelAdmin):
    list_display=('Art_id','title', 'aboutArt', 'image_tag') #displays the mentioned categories from the database table= arts on to the Arts admin panel
    search_fields= ('title',) # creates a search bar in admin panel 
    list_filter=('ArtistName',) # it creates a column to filter/ show the arts bases on the arist name.
    list_per_page=10 # only displays 5 arts per page


    class Media:
        js= ('js/script.js')



class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_amount', 'shipping_address')
    search_fields = ('user__username', 'shipping_address')
    list_filter = ('created_at',)
    inlines = [OrderItemInline]

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'art', 'quantity', 'price')
    search_fields = ('order__user__username', 'art__title')

    

# Register your models here.
admin.site.register(Artists, ArtistsAdmin)
admin.site.register(Arts,ArtsAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
