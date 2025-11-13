from django.db import models
from core.models import BaseModel

class Album(BaseModel):
    """
    Represents a photo album for a specific event or category.
    e.g., "Annual Day 2024", "Sports Meet", "Campus Life"
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='album_covers/', help_text="A representative image for the album.")

    class Meta:
        verbose_name = "Album"
        verbose_name_plural = "Albums"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Photo(BaseModel):
    """
    Represents a single photo within an album.
    """
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='gallery_photos/')
    caption = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Photo"
        verbose_name_plural = "Photos"
        ordering = ['-created_at']

    def __str__(self):
        return self.caption or f"Photo in {self.album.title}"