# Generated by Django 2.2 on 2020-12-28 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('depthead', '0022_auto_20201227_2308'),
        ('student', '0007_delete_students'),
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
                ('Reg_No', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=100)),
                ('Gender', models.CharField(max_length=10)),
                ('Dept', models.CharField(max_length=10)),
                ('Phone', models.CharField(max_length=20)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='depthead.Student_Sessions')),
            ],
        ),
    ]
