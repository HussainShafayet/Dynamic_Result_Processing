# Generated by Django 2.2 on 2021-02-20 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_depthead_dept'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depthead',
            name='dept',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='depthead.Dept'),
        ),
    ]
