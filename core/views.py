from django.shortcuts import render
from core.models import HomePageContent
from blog.models import Post
from faculty.models import StaffProfile
from gallery.models import Album
from academics.models import Department, AcademicDocument

def home_view(request):
    """
    View for the homepage.
    """
    # Fetch content for each section
    homepage_content = HomePageContent.objects.first()
    faculty_members = StaffProfile.objects.all()[:6]  # Show the first 6 faculty members
    latest_posts = Post.objects.filter(status='published')[:3]  # Show the 3 latest posts
    latest_albums = Album.objects.all()[:3]  # Show the 3 latest albums
    departments = Department.objects.all()
    academic_documents = AcademicDocument.objects.all()
    carousel_images = homepage_content.carousel_images.all() if homepage_content else []

    context = {
        'content': homepage_content,
        'faculty_members': faculty_members,
        'latest_posts': latest_posts,
        'latest_albums': latest_albums,
        'departments': departments,
        'academic_documents': academic_documents,  # for circulars/latest news
        'carousel_images': carousel_images,
    }

    return render(request, 'core/index.html', context)


def contact_view(request):
    return render(request,'core/contact.html')