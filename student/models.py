from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import os

# Create your models here.

class StudentProfile(models.Model):
    courses = [
        ('Python Fullstack Development', 'Python Fullstack Development'),
        ('Java Fullstack Development', 'Java Fullstack Development'),
        ('MERN Fullstack Development', 'MERN Fullstack Development'),
        ('Fullstack Testing', 'Fullstack Testing')
    ]

    def get_upload_path(self, filename):
        ext = filename.split('.')[-1]
        filename = f"{self.username.first_name}_{self.username.last_name}_resume.{ext}"
        return os.path.join("students_resume", filename)
    
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50)
    add = models.CharField(max_length=50)
    course = models.CharField(max_length=50, choices=courses)
    profile_pic = models.ImageField(upload_to='students_profiles/')
    resume = models.FileField(upload_to=get_upload_path, validators=[FileExtensionValidator(['pdf', 'docx'])])

    def __str__(self):
        return self.username.username