# Generated by Django 3.2.16 on 2023-08-21 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_sitepreferences_georepo_azure_authentication_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitepreferences',
            name='landing_page_banner_text',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
