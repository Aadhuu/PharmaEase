from django.contrib import admin


from cart.models import Cart, Order

from cart.models import OrderItem

admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)

