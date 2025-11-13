from django.db import models
from core.models import BaseModel

class StaffProfile(BaseModel):
    """
    Model to store profiles of faculty and staff.
    """
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='faculty_photos/', help_text="A professional headshot.")
    designation = models.CharField(max_length=100, help_text="e.g., Principal, TGT Mathematics, Librarian")
    qualification = models.CharField(max_length=200, help_text="e.g., M.Sc. in Physics, B.Ed.")
    department = models.CharField(max_length=100, help_text="e.g., Science, Humanities, Administration")
    bio = models.TextField(blank=True, null=True, help_text="A short biography or message.")
    display_order = models.PositiveIntegerField(default=0, help_text="Order of display on the page (0 is first).")

    class Meta:
        verbose_name = "Staff Profile"
        verbose_name_plural = "Staff Profiles"
        ordering = ['display_order', 'name'] # Order by display_order, then by name

    def __str__(self):
        return f"{self.name} ({self.designation})"
