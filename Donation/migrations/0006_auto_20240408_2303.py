# Generated by Django 3.1.1 on 2024-04-08 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0002_auto_20240326_1634'),
        ('Donation', '0005_auto_20240408_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surgery',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.userprofile'),
        ),
    ]
