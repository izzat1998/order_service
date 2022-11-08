from django.contrib import admin

from apps.order.models import Order, WagonOrder, WagonEmptyOrder


# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number',)


admin.site.register(Order, OrderAdmin)




class WagonOrderAdmin(admin.ModelAdmin):
    list_display = ('order',)


admin.site.register(WagonOrder, WagonOrderAdmin)


class WagonEmptyOrderAdmin(admin.ModelAdmin):
    list_display = ('order',)


admin.site.register(WagonEmptyOrder, WagonEmptyOrderAdmin)

