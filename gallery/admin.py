from django.contrib import admin
from .models import Album, Photo

class PhotoInline(admin.TabularInline):
    """Allows adding photos directly within the Album admin page."""
    model = Photo
    extra = 3  # Show 3 empty slots for new photos by default
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at')
    search_fields = ('title',)
    inlines = [PhotoInline]

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('caption', 'album', 'created_at')
    list_filter = ('album',)
    search_fields = ('caption', 'album__title')