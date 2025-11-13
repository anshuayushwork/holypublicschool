from django.shortcuts import render
from .models import StaffProfile

def staff_list_view(request):
    """
    This view retrieves all staff profiles from the database,
    ordered by their display_order, and renders them to a template.
    """
    # The .all() method fetches all records from the StaffProfile table.
    # The ordering is handled automatically by the 'ordering' Meta option in the model.
    staff_list = StaffProfile.objects.all()
    
    # The context is a dictionary that passes data to the template.
    # The key 'staff_members' will be used to access the list in the HTML file.
    context = {
        'staff_members': staff_list,
    }
    
    # Renders the request, template, and context to produce the final HTML.
    return render(request, 'faculty/staff_list.html', context)
