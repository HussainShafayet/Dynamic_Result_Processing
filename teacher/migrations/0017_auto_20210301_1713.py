# Generated by Django 2.2 on 2021-03-01 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0016_auto_20210225_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course_result_sessional',
            name='Attendence',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course_result_sessional',
            name='Exam',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course_result_sessional',
            name='Grade_point',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course_result_sessional',
            name='Lab_performance',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course_result_sessional',
            name='Total_mark',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course_result_theory',
            name='Attendence',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course_result_theory',
            name='Exam_Part_A',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course_result_theory',
            name='Exam_Part_B',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course_result_theory',
            name='Grade_point',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course_result_theory',
            name='Term_test',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course_result_theory',
            name='Total_mark',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]