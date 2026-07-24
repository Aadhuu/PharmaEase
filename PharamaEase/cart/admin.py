from django.contrib import admin
from cart.models import Cart, Order
from cart.models import OrderItem

admin.site.register(Cart)
admin.site.register(OrderItem)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=('user','order_id','ordered_date','amount','payment_method','delivery_status','is_ordered')
    list_editable = ('delivery_status',)



