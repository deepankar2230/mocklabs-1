from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import os
# Create your models here.

class Rating(models.Model):
    subjects = [
        ('Python', 'Python'),
        ('Java', 'Java'),
        ('MERN', 'MERN'),
        ('Django', 'Django'),
        ('WebTech', 'WebTech'),
        ('SQL', 'SQL'),
        ('MongoDB', 'MongoDB'),
        ('Bootstrap', 'Bootstrap'),
    ]
    raatings = [
        ('*', '*'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    ]
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    subject = models.CharField(max_length=50, choices=subjects, default='Python')
    communicating = models.CharField(max_length=50, choices=raatings, default='1')
    technical = models.CharField(max_length=50, choices=raatings, default='1')
    programming = models.CharField(max_length=50, choices=raatings, default='1')
    remarks = models.CharField(max_length=200)
    conducted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='by')
    conducted_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.student.username


class Schedulings(models.Model):
    subjects = [
        ('Python', 'Python'),
        ('Java', 'Java'),
        ('MERN', 'MERN'),
        ('Django', 'Django'),
        ('WebTech', 'WebTech'),
        ('SQL', 'SQL'),
        ('MongoDB', 'MongoDB'),
        ('Bootstrap', 'Bootstrap'),
    ]
    def get_upload_path(self, filename):
        ext = filename.split('.')[-1]
        filename = f"Slot_{self.trainer.username}.{ext}"
        return os.path.join("Slots", filename)
    
    slot_id = models.IntegerField(primary_key=True)
    students = models.FileField(upload_to=get_upload_path, max_length=100, validators=[FileExtensionValidator(['csv'])])
    subject = models.CharField(max_length=50, choices=subjects)
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='slots')
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return f"{self.trainer.username}_{self.slot_id}"