from django.contrib import admin

from .models import (
    ContainerOrder,
    CounterPartyOrder,
    ContainerTypeOrder,
    ContainerPreliminaryCost,
    ContainerExpanse,
    ContainerActualCost,
)


class ContainerOrderAdmin(admin.ModelAdmin):
    list_display = ("order",)


admin.site.register(ContainerOrder, ContainerOrderAdmin)


# Register your models here.


class CounterPartyOrderAdmin(admin.ModelAdmin):
    list_display = ("order", "counterparty", "category")


admin.site.register(CounterPartyOrder, CounterPartyOrderAdmin)


class ContainerTypeOrderAdmin(admin.ModelAdmin):
    list_display = ("order", "agreed_rate", "container_type", "quantity")


admin.site.register(ContainerTypeOrder, ContainerTypeOrderAdmin)


class ContainerPreliminaryCostAdmin(admin.ModelAdmin):
    list_display = ("container_type", "counterparty", "preliminary_cost")


admin.site.register(ContainerPreliminaryCost, ContainerPreliminaryCostAdmin)


class ContainerExpanseAdmin(admin.ModelAdmin):
    list_display = ("container_type", "container", "agreed_rate")


admin.site.register(ContainerExpanse, ContainerExpanseAdmin)


class ContainerActualCostAdmin(admin.ModelAdmin):
    list_display = ("counterparty", "actual_cost", "container_expanse")


admin.site.register(ContainerActualCost, ContainerActualCostAdmin)
