# Generated by Django 2.2 on 2021-03-03 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('depthead', '0035_auto_20210303_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='batch_name',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='session',
            name='session_name',
            field=models.CharField(default=None, max_length=50),
        ),
    ]