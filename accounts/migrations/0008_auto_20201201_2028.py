# Generated by Django 2.2 on 2020-12-01 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20201201_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='reg_no',
            field=models.IntegerField(default=0),
        ),
    ]
