# Generated by Django 5.0.6 on 2025-03-19 16:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Donation', '0011_organrequest_bloodgroup'),
        ('Home', '0008_receiverprofile_bloodgroup'),
    ]

    operations = [
        migrations.AddField(
            model_name='organrequest',
            name='Donar',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Home.userprofile'),
        ),
        migrations.AddField(
            model_name='organrequest',
            name='Donar_approval',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='organrequest',
            name='HealthRecord',
            field=models.FileField(default=1, upload_to='HealthFile'),
            preserve_default=False,
        ),
    ]
