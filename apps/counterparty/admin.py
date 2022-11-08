from django.contrib import admin

from apps.counterparty.models import Counterparty, CounterpartyCategory


# Register your models here.

class CounterPartyAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Counterparty, CounterPartyAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(CounterpartyCategory, CategoryAdmin)
