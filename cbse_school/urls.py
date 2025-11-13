from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('gallery/', include('gallery.urls')),
    
    path('', include('core.urls')),
    path('faculty',include('faculty.urls')),
    path('academics/', include('academics.urls')),
    path('admissions/',include('admissions.urls')),
    
    


]

# This is crucial for serving user-uploaded media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

