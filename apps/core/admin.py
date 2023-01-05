from django.contrib import admin

from .models import Product, Station, Container, Wagon, Territory


# Register your models here.

class TerritoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(Territory, TerritoryAdmin)


class StationAdmin(admin.ModelAdmin):
    list_display = ("name", "code")


admin.site.register(Station, StationAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "hc_code", "etcng_code")
    search_fields = ("name", "hc_code", "etcng_code")


admin.site.register(Product, ProductAdmin)


class ContainerAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(Container, ContainerAdmin)


class WagonAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(Wagon, WagonAdmin)
