# Generated by Django 5.0.6 on 2025-03-19 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0007_userprofile_medical_doc_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiverprofile',
            name='Bloodgroup',
            field=models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], default=1, max_length=255),
            preserve_default=False,
        ),
    ]
