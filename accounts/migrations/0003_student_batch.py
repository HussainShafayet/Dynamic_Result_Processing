# Generated by Django 2.2 on 2020-12-01 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('depthead', '0001_initial'),
        ('accounts', '0002_student_dept'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='batch',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='depthead.Batch'),
        ),
    ]
