# Generated by Django 4.1.3 on 2022-12-31 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0003_rename_profile_pic_employee_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='Address',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='Title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]