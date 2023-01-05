from django.contrib import admin

from apps.code.models import Application


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("number",)


admin.site.register(Application, ApplicationAdmin)
