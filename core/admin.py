from django.contrib import admin

from core.models import Product, Station


# Register your models here.
class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


admin.site.register(Station, StationAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'hc_code', 'etcng_code')


admin.site.register(Product, ProductAdmin)
