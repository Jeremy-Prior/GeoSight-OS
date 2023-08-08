# Generated by Django 3.2.16 on 2023-08-08 08:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('geosight_data', '0082_auto_20230724_0637'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dashboard',
            old_name='description',
            new_name='overview',
        ),
        migrations.AddField(
            model_name='dashboard',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
