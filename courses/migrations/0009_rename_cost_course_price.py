# Generated by Django 5.0.6 on 2024-08-15 01:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_demomaterial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='cost',
            new_name='price',
        ),
    ]
