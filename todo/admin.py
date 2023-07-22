from django.contrib import admin
from .models import ToDo
# Register your models here.


class Admin(admin.ModelAdmin):
    readonly_fields = ('creation_time', )


admin.site.register(ToDo, Admin)
