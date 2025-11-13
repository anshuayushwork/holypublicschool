# admissions/models.py


from django.db import models
from .validators import validate_file_size 
from django.db import models
from django.utils.text import slugify
from core.models import BaseModel
from django.core.exceptions import ValidationError
from django.utils import timezone


# --- Reusable Choices ---
# These keep your model clean.


     # --- Status Choices ---
STATUS_CHOICES = [
        ('INCOMPLETE', 'Step 1 Completed'),
        ('PENDING_PAYMENT', 'Pending Payment'),
        ('COMPLETED', 'Application Submitted'),
        # ... other statuses
    ]
ACADEMIC_YEAR_CHOICES = [('2025-26', '2025-26')]

CLASS_CHOICES = [
    ('PLAYGROUP', 'PLAY GROUP'), ('PRENURSERY', 'PRE-NURSERY'), ('NURSERY', 'NURSERY'), 
    ('PREP', 'PREP'), ('II', 'II'), ('III', 'III'), ('V', 'V'), ('VI', 'VI'), 
    ('VII', 'VII'), ('VIII', 'VIII'), ('IX', 'IX'), ('X', 'X'), ('XI', 'XI'),
]

GENDER_CHOICES = [('MALE', 'Male'), ('FEMALE', 'Female'), ('TRANSGENDER', 'Transgender')]

BLOOD_GROUP_CHOICES = [
    ('O-', 'O-'), ('O+', 'O+'), ('A+', 'A+'), ('A-', 'A-'), ('B-', 'B-'), 
    ('B+', 'B+'), ('AB-', 'AB-'), ('AB+', 'AB+'),
]

CATEGORY_CHOICES = [
    ('EWS', 'EWS'), ('GENERAL', 'GENERAL'), ('OBC', 'OBC'), 
    ('SC', 'SC'), ('ST', 'ST'), ('STAFF', 'STAFF'),
]

RELIGION_CHOICES = [
    ('HINDU', 'Hindu'), ('ISLAM', 'Islam'), ('SIKHISM', 'Sikhism'),
    ('CHRISTIANITY', 'Christianity'), ('BUDDHISM', 'Buddhism'), ('JAINISM', 'Jainism'),
    ('OTHERS', 'Others'),
]

NATIONALITY_CHOICES = [('INDIAN', 'Indian'), ('NEPALESE', 'Nepalese'), ('OTHER', 'Other')] # Add all others
STUDENT_TYPES=[('DAY SCHOLAR','Day scholar'),('HOSTEL','hostel')]
QUALIFICATION_CHOICES = [
    ('NON_MATRIC', 'NON-MATRIC'), ('MATRIC', 'Matriculation'), ('INTERMEDIATE', 'INTERMEDIATE'),
    ('GRADUATION', 'Graduation'), ('POST_GRADUATION', 'Post Graduation'), ('PHD', 'P HD'),
] # Add all others

OCCUPATION_CHOICES = [
    ('GOVT_JOB', 'GOVT JOB'), ('PRIVATE_JOB', 'PRIVATE JOB'), ('FARMER', 'FARMER'),
    ('BUSINESS', 'BUSINESS MAN'), ('HOME_MAKER', 'Home Maker'), ('DOCTOR', 'DOCTOR'),
] # Add all others

# --- The Main Model ---

class AdmissionApplication(BaseModel):
    # (Keep your existing status and payment fields)
    status = models.CharField(max_length=20, default='PENDING_PAYMENT')
    application_number = models.CharField(max_length=20, unique=True, blank=True, null=True, editable=False)
    
    # --- Part 1: Student Details ---
    academic_year = models.CharField(max_length=10, choices=ACADEMIC_YEAR_CHOICES)
    admission_class = models.CharField(max_length=20, choices=CLASS_CHOICES)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    birth_place = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True, null=True)
    mother_tongue = models.CharField(max_length=50)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    religion = models.CharField(max_length=20, choices=RELIGION_CHOICES)
    is_single_parent = models.BooleanField(default=False)
    primary_contact_number = models.CharField(max_length=15)
    email_id = models.EmailField()
    aadhaar_number = models.CharField(max_length=12, blank=True, null=True)
    student_type = models.CharField(max_length=20, choices=STUDENT_TYPES)
    nationality = models.CharField(max_length=50, choices=NATIONALITY_CHOICES)
    student_photo = models.ImageField(upload_to='student_photos/', validators=[validate_file_size])

    # --- Previous School Details ---
    previous_school_name = models.CharField(max_length=200, blank=True, null=True)
    previous_class_name = models.CharField(max_length=20, blank=True, null=True)

    # --- Other Details ---
    hobbies = models.TextField(blank=True, null=True)
    is_interested_in_competitive_exams = models.BooleanField(default=False)
    is_physically_handicapped = models.BooleanField(default=False)
    pen_number = models.CharField(max_length=50, blank=True, null=True)
    wants_transportation = models.BooleanField(default=False)
    
    # --- Part 1: Father Details ---
    father_first_name = models.CharField(max_length=100)
    # ... (add middle_name, last_name, age, mobile_no, email, qualification, occupation, etc.)
    father_annual_income = models.CharField(max_length=50, blank=True, null=True)
    father_photo = models.ImageField(upload_to='parent_photos/', validators=[validate_file_size])

    # --- Part 1: Mother Details ---
    mother_first_name = models.CharField(max_length=100)
    # ... (add all other mother fields similar to father)
    mother_photo = models.ImageField(upload_to='parent_photos/', validators=[validate_file_size])

    # --- Part 1: Address Details ---
    corresponding_address = models.TextField()
    # ... (add country, state, city, pincode, distance from school)
    permanent_address = models.TextField()
    # ... (add permanent country, state, city, pincode, etc.)

    # --- Part 1: Sibling & Media Details ---
    number_of_daughters = models.PositiveIntegerField(default=0)
    number_of_sons = models.PositiveIntegerField(default=0)
    sibling_details = models.TextField(blank=True, null=True)
    media_permission_facility = models.BooleanField(default=False)
    media_permission_online = models.BooleanField(default=False)
    media_permission_print = models.BooleanField(default=False)

    # --- Part 2: Document Uploads ---
    birth_certificate = models.FileField(upload_to='documents/birth_certificates/', blank=True, null=True)
    previous_marksheet = models.FileField(upload_to='documents/marksheets/', blank=True, null=True)
    transfer_certificate = models.FileField(upload_to='documents/tc/', blank=True, null=True)

    order_id = models.CharField(max_length=100, blank=True, null=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.application_number:
            current_year = timezone.now().year
            last_application = AdmissionApplication.objects.filter(
                application_number__startswith=f'APP-{current_year}'
            ).order_by('application_number').last()
            
            if last_application:
                last_number = int(last_application.application_number.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.application_number = f'APP-{current_year}-{new_number:04d}'
            
        super().save(*args, **kwargs)
    


    # def __str__(self):
    #     return f"{self.first_name} {self.last_name} - {self.uid}"
    


