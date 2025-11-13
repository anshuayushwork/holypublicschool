from django.contrib import admin
from .models import AdmissionApplication

@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the AdmissionApplication model.
    """
    
    # --- List View Configuration ---
    # Defines the columns shown in the list of all applications
    list_display = (
        'application_number',
        'uid', 
        'first_name', 
        'last_name', 
        'admission_class', 
        'status', 
        'created_at'
    )
    
    # Adds a filter sidebar for easy filtering by status and class
    list_filter = ('status', 'admission_class', 'academic_year')
    
    # Adds a search bar to search for applications by key details
    search_fields = (
        'application_number',
        'first_name', 
        'last_name', 
        'email_id', 
        'primary_contact_number', 
        'uid'
    )
    
    # --- Detail View Configuration ---
    # Makes critical, system-generated fields non-editable
    readonly_fields = (
        'application_number',
        'uid', 
        'created_at', 
        'updated_at', 
        'order_id', 
        'payment_id'
    )
    
    # Organizes the many fields into logical, collapsible sections
    fieldsets = (
        ('Application Management', {
            'fields': ('status',)  # Keep the status at the top for easy updates
        }),
        ('Key Application Details', {
            'fields': ('application_number','uid', 'academic_year', 'admission_class')
        }),
        ('Student Information', {
            'fields': (
                'first_name', 'middle_name', 'last_name', 'gender', 'date_of_birth', 
                'birth_place', 'blood_group', 'mother_tongue', 'category', 'religion',
                'nationality', 'aadhaar_number', 'student_type', 'student_photo'
            )
        }),
        ('Contact Information', {
            'fields': ('primary_contact_number', 'email_id')
        }),
        ('Parental & Other Details', {
            'fields': (
                'is_single_parent', 'is_physically_handicapped', 'hobbies',
                'is_interested_in_competitive_exams', 'wants_transportation', 'pen_number'
            )
        }),
        ('Father\'s Details', {
            'fields': ('father_first_name', 'father_annual_income', 'father_photo'),
            'classes': ('collapse',) # This section will be collapsed by default
        }),
        ('Mother\'s Details', {
            'fields': ('mother_first_name', 'mother_photo'),
            'classes': ('collapse',)
        }),
        ('Address Details', {
            'fields': ('corresponding_address', 'permanent_address'),
            'classes': ('collapse',)
        }),
        ('Sibling & Media Permissions', {
            'fields': (
                'number_of_daughters', 'number_of_sons', 'sibling_details', 
                'media_permission_facility', 'media_permission_online', 'media_permission_print'
            ),
            'classes': ('collapse',)
        }),
        ('Uploaded Documents', {
            'fields': ('birth_certificate', 'previous_marksheet', 'transfer_certificate'),
            'classes': ('collapse',)
        }),
        ('Payment Details (Read-Only)', {
            'fields': ('order_id', 'payment_id')
        }),
        ('Timestamps (Read-Only)', {
            'fields': ('created_at', 'updated_at')
        }),
    )