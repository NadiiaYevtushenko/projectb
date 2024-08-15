# Generated by Django 5.0.6 on 2024-08-14 22:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_review_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_tests', to='courses.course'),
        ),
    ]
