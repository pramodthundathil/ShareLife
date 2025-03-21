# Generated by Django 5.0.6 on 2025-03-19 15:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Donation', '0009_alter_consutation_id_alter_organdonation_id_and_more'),
        ('Home', '0007_userprofile_medical_doc_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organrequest',
            name='Organ',
        ),
        migrations.RemoveField(
            model_name='organrequest',
            name='hospitel',
        ),
        migrations.AddField(
            model_name='organrequest',
            name='approval_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='organrequest',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=20),
        ),
        migrations.AddField(
            model_name='surgery',
            name='completion_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='surgery',
            name='donar',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Home.userprofile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='organrequest',
            name='patient',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Home.receiverprofile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='surgery',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.receiverprofile'),
        ),
        migrations.AlterField(
            model_name='surgery',
            name='surgery_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='organrequest',
            name='organ',
            field=models.CharField(choices=[('Kidneys', 'Kidneys'), ('Liver', 'Liver'), ('Lungs', 'Lungs'), ('Heart', 'Heart'), ('Pancreas', 'Pancreas'), ('Intestines', 'Intestines'), ('Hands', 'Hands'), ('Eye', 'Eye')], default=1, max_length=255),
            preserve_default=False,
        ),
    ]
