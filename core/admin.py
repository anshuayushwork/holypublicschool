from django.contrib import admin
from .models import SiteConfiguration, HomePageContent

# Register the SiteConfiguration model
@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'contact_email', 'updated_at')
    
    # # This is a helpful message to prevent admins from creating more than one config.
    # def has_add_permission(self, request):
    #     # Check if an instance already exists
    #     if self.model.objects.exists():
    #         return False
    #     return super().has_add_permission(request)

    # def has_delete_permission(self, request, obj=None):
    #     # Disable delete action
    #     return False

# Register the HomePageContent model
# @admin.register(HomePageContent)
# class HomePageContentAdmin(admin.ModelAdmin):
#     list_display = ('hero_title', 'updated_at')
    
    # # Apply the same singleton pattern as above
    # def has_add_permission(self, request):
    #     if self.model.objects.exists():
    #         return False
    #     return super().has_add_permission(request)

    # def has_delete_permission(self, request, obj=None):
    #     return False

from django.contrib import admin
from .models import HomePageContent, CarouselImage

class CarouselImageInline(admin.TabularInline):
    model = CarouselImage
    extra = 1  # allows adding one new image inline

@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    list_display = ('hero_title', 'principals_welcome_title')
    inlines = [CarouselImageInline]

@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'homepage')
