# Generated by Django 2.2 on 2021-03-11 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0027_auto_20210310_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='course_result_sessional',
            name='Project_mark',
            field=models.IntegerField(default=0),
        ),
    ]
