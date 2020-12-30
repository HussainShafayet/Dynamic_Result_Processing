# Generated by Django 2.2 on 2020-12-27 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0004_teachers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Session', models.CharField(blank=True, max_length=20, null=True)),
                ('Course', models.CharField(blank=True, max_length=10, null=True)),
                ('Active', models.BooleanField(blank=True, default=True, null=True)),
                ('Batch', models.CharField(blank=True, max_length=30, null=True)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.Teachers')),
            ],
        ),
    ]