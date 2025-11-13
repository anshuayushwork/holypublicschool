# admissions/forms.py

from django import forms
from .models import AdmissionApplication

class StudentParentForm(forms.ModelForm):
    
    # Custom choices for boolean fields to render as Yes/No radio buttons
    BOOLEAN_CHOICES = [(True, 'Yes'), (False, 'No')]

    is_single_parent = forms.TypedChoiceField(
        coerce=lambda x: x == 'True',
        choices=BOOLEAN_CHOICES,
        widget=forms.RadioSelect
    )
    is_interested_in_competitive_exams = forms.TypedChoiceField(
        coerce=lambda x: x == 'True',
        choices=BOOLEAN_CHOICES,
        widget=forms.RadioSelect
    )
    is_physically_handicapped = forms.TypedChoiceField(
        coerce=lambda x: x == 'True',
        choices=BOOLEAN_CHOICES,
        widget=forms.RadioSelect
    )
    wants_transportation = forms.TypedChoiceField(
        coerce=lambda x: x == 'True',
        choices=BOOLEAN_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        model = AdmissionApplication
        # List all the fields from the model that should be in this form
        fields = [
            # Student Details
            'academic_year', 'admission_class', 'first_name', 'middle_name', 'last_name', 
            'gender', 'date_of_birth', 'birth_place', 'blood_group', 'mother_tongue', 
            'category', 'religion', 'is_single_parent', 'primary_contact_number', 
            'email_id', 'aadhaar_number', 'student_type', 'nationality', 'student_photo',

            # Previous School Details
            'previous_school_name', 'previous_class_name',

            # Other Details
            'hobbies', 'is_interested_in_competitive_exams', 'is_physically_handicapped', 
            'pen_number', 'wants_transportation',

            # Father Details (add all father fields from your model here)
            'father_first_name', 'father_annual_income', 'father_photo',
            # 'father_middle_name', 'father_last_name', etc...
            
            # Mother Details (add all mother fields from your model here)
            'mother_first_name', 'mother_photo',
            # 'mother_middle_name', 'mother_last_name', etc...

            # Address Details (add all address fields here)
            'corresponding_address', 'permanent_address', 

            # Sibling & Media Details
            'number_of_daughters', 'number_of_sons', 'sibling_details', 
            'media_permission_facility', 'media_permission_online', 'media_permission_print',
        ]

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.RadioSelect,
            'hobbies': forms.Textarea(attrs={'rows': 3}),
            'corresponding_address': forms.Textarea(attrs={'rows': 3}),
            'permanent_address': forms.Textarea(attrs={'rows': 3}),
            'sibling_details': forms.Textarea(attrs={'rows': 3}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                 if not isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                     field.widget.attrs.update({'class': 'form-control'})

                 if isinstance(field.widget, forms.Select):
                     field.widget.attrs.update({'class': 'form-select'})
                 

           

           
        
        


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = AdmissionApplication
        fields = [
            'birth_certificate',
            'previous_marksheet',
            'transfer_certificate',
        ]
        labels = {
            'birth_certificate': 'Upload Birth Certificate',
            'previous_marksheet': 'Upload Previous Year\'s Marksheet',
            'transfer_certificate': 'Upload Transfer Certificate (TC)',
        }



# admissions/forms.py

class ApplicationSearchForm(forms.Form):
    application_number = forms.CharField(label="Your Application Number")
    date_of_birth = forms.DateField(
        label="Student's Date of Birth",
        widget=forms.DateInput(attrs={'type': 'date'})
    )