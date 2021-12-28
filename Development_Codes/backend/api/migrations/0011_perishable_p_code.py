# Generated by Django 3.2.9 on 2021-12-21 11:06

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_perishable_p_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='perishable',
            name='p_code',
            field=models.CharField(default=api.models.generate_unique_code, max_length=8, unique=True),
        ),
    ]
