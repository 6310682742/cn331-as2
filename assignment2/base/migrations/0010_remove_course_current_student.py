# Generated by Django 4.1.1 on 2022-09-16 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_course_describetion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='current_student',
        ),
    ]