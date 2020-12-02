# Generated by Django 2.2 on 2020-12-02 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20201201_2034'),
        ('depthead', '0007_delete_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teststudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Student')),
            ],
        ),
    ]
