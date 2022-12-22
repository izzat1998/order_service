from django.contrib import admin

from apps.wagon_empty_order.models import WagonEmptyExpanse


class WagonEmptyExpanseAdmin(admin.ModelAdmin):
    list_display = ("order", "wagon", "agreed_rate")


admin.site.register(WagonEmptyExpanse, WagonEmptyExpanseAdmin)