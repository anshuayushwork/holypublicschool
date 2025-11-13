from django.db import models
from core.models import BaseModel

class Department(BaseModel):
    """
    Represents an academic department.
    e.g., "Science", "Mathematics", "Humanities", "Computer Science"
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class AcademicDocument(BaseModel):
    """
    Model for uploading academic-related documents.
    e.g., "Academic Calendar 2024-25", "Syllabus for Class X"
    """
    title = models.CharField(max_length=200)
    document_file = models.FileField(upload_to='academic_documents/')
    description = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = "Academic Document"
        verbose_name_plural = "Academic Documents"
        ordering = ['-created_at']

    def __str__(self):
        return self.title