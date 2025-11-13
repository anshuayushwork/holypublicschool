from django.db import models
import uuid

# --- Corrected Base Model ---
class BaseModel(models.Model):
    """
    Abstract base model with a UUID primary key and timestamps.
    """
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
   
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# --- Site-wide Configuration Model ---
class SiteConfiguration(BaseModel):
    """
    Model to store site-wide settings.
    IMPORTANT: There should only be ONE instance of this model.
    """
    school_name = models.CharField(max_length=200, default="Your CBSE School Name")
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    # Social Media Links
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return "Site-wide Configuration"


# --- Home Page Content Model ---
class HomePageContent(BaseModel):
    """
    Model to manage the dynamic content of the home page.
    IMPORTANT: There should also only be ONE instance of this model.
    """
    hero_title = models.CharField(max_length=255,blank=True, null=True, help_text="The main title on the hero banner.")
    hero_subtitle = models.CharField(max_length=500, blank=True, null=True, help_text="A short subtitle or motto.")
    hero_image = models.ImageField(upload_to='homepage/',blank=True, null=True, help_text="Recommended size: 1920x800 pixels.")
    
    principals_welcome_title = models.CharField(max_length=200, default="A Welcome from the Principal")
    principals_welcome_message = models.TextField(help_text="A short welcome message for the home page.")
    principals_photo = models.ImageField(upload_to='homepage/', help_text="A portrait photo of the principal.")

    class Meta:
        verbose_name = "Home Page Content"
        verbose_name_plural = "Home Page Content"

    def __str__(self):
        # Safe __str__ if hero_title is empty
        return self.hero_title or "Home Page Content"

class CarouselImage(models.Model):
    image = models.ImageField(upload_to='homepage/carousel/')
    title = models.CharField(max_length=255, blank=True, null=True)
    homepage = models.ForeignKey(HomePageContent, on_delete=models.CASCADE, related_name='carousel_images')

    def __str__(self):
        return self.title or "Carousel Image"
