# Generated by Django 2.2 on 2021-02-20 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_auto_20210221_0253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depthead',
            name='designation',
            field=models.CharField(max_length=100),
        ),
    ]