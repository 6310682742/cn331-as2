# Generated by Django 4.1.1 on 2022-09-16 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_delete_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_code',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='course',
            name='course_semeter',
            field=models.CharField(default='1', max_length=200),
        ),
        migrations.AddField(
            model_name='course',
            name='course_year',
            field=models.IntegerField(default=2000),
        ),
    ]