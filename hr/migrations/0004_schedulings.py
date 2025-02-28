# Generated by Django 5.1.6 on 2025-02-27 06:42

import django.core.validators
import django.db.models.deletion
import hr.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0003_alter_rating_student'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedulings',
            fields=[
                ('slot_id', models.IntegerField(primary_key=True, serialize=False)),
                ('students', models.FileField(upload_to=hr.models.Schedulings.get_upload_path, validators=[django.core.validators.FileExtensionValidator(['csv'])])),
                ('subject', models.CharField(choices=[('Python', 'Python'), ('Java', 'Java'), ('MERN', 'MERN'), ('Django', 'Django'), ('WebTech', 'WebTech'), ('SQL', 'SQL'), ('MongoDB', 'MongoDB'), ('Bootstrap', 'Bootstrap')], max_length=50)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slots', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
