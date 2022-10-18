from django.contrib import admin

from order.models import Order, ContainerOrder, WagonOrder, WagonEmptyOrder, CounterPartyOrder, ContainerTypeOrder, \
    ContainerPreliminaryCost, ContainerExpanse, Container


# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number',)


admin.site.register(Order, OrderAdmin)


class ContainerOrderAdmin(admin.ModelAdmin):
    list_display = ('order',)


admin.site.register(ContainerOrder, ContainerOrderAdmin)


class WagonOrderAdmin(admin.ModelAdmin):
    list_display = ('order',)


admin.site.register(WagonOrder, WagonOrderAdmin)


class WagonEmptyOrderAdmin(admin.ModelAdmin):
    list_display = ('order',)


admin.site.register(WagonEmptyOrder, WagonEmptyOrderAdmin)


class CounterPartyOrderAdmin(admin.ModelAdmin):
    list_display = ('order', 'counterparty', 'category')


admin.site.register(CounterPartyOrder, CounterPartyOrderAdmin)


class ContainerTypeOrderAdmin(admin.ModelAdmin):
    list_display = ('order', 'agreed_rate', 'container_type', 'quantity')


admin.site.register(ContainerTypeOrder, ContainerTypeOrderAdmin)


class ContainerPreliminaryCostAdmin(admin.ModelAdmin):
    list_display = ('container_type', 'counterparty', 'preliminary_cost')


admin.site.register(ContainerPreliminaryCost, ContainerPreliminaryCostAdmin)


class ContainerExpanseAdmin(admin.ModelAdmin):
    list_display = ('counterparty', 'container', 'container_type', 'actual_cost')


admin.site.register(ContainerExpanse, ContainerExpanseAdmin)


class ContainerAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Container, ContainerAdmin)
