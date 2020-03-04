from django.contrib import admin

# Register your models here.
from .models import Machine, Line, Data


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    pass

@admin.register(Line)
class LineAdmin(admin.ModelAdmin):
    pass

@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    pass
