# Generated by Django 4.2.6 on 2023-11-11 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_employees_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employees',
            old_name='image',
            new_name='profile_pic',
        ),
    ]
