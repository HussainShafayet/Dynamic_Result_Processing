# Generated by Django 2.2 on 2020-12-27 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('depthead', '0021_student_sessions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch_result',
            name='Result_Session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='depthead.Student_Sessions'),
        ),
    ]
