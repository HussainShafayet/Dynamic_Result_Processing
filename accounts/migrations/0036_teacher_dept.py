# Generated by Django 2.2 on 2021-03-11 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('depthead', '0040_auto_20210311_1618'),
        ('accounts', '0035_auto_20210309_0321'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='dept',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='depthead.Dept'),
        ),
    ]
