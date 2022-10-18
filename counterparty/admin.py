from django.contrib import admin

from counterparty.models import Counterparty, Category


# Register your models here.

class CounterPartyAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Counterparty, CounterPartyAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Category, CategoryAdmin)
