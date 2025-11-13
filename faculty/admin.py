from django.contrib import admin
from .models import StaffProfile

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'department', 'display_order')
    list_filter = ('department', 'designation')
    search_fields = ('name', 'qualification')
    list_editable = ('display_order',)
