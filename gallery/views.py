from django.shortcuts import render, get_object_or_404
from .models import Album

def album_list_view(request):
    """
    This view retrieves all Album objects from the database
    and renders them to a template that displays the list of albums.
    """
    albums = Album.objects.all()
    
    context = {
        'albums': albums
    }
    return render(request, 'gallery/album_list.html', context)


def album_detail_view(request, uid):
    """
    This view retrieves a single Album by its UID and all the photos
    associated with it, then renders them to a detail template.
    """
    # Get the specific album or return a 404 error if it's not found.
    album = get_object_or_404(Album, uid=uid)
    
    # The related photos are automatically accessible via 'album.photos.all()'
    # because of the 'related_name' we set in the Photo model.
    context = {
        'album': album
    }
    return render(request, 'gallery/album_detail.html', context)
