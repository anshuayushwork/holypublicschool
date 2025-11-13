from django.shortcuts import render
from .models import Department, AcademicDocument

def academic_info_view(request):
    """
    This view retrieves all departments and academic documents
    to display on a single academics page.
    """
    departments = Department.objects.all()
    documents = AcademicDocument.objects.all()
    
    context = {
        'departments': departments,
        'documents': documents,
    }
    return render(request, 'academics/academic_info.html', context)
