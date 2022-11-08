from django.contrib import admin

from apps.core.models import Product, Station, Container


# Register your models here.
class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


admin.site.register(Station, StationAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'hc_code', 'etcng_code')
    search_fields = ('name', 'hc_code', 'etcng_code')


admin.site.register(Product, ProductAdmin)


class ContainerAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Container, ContainerAdmin)
