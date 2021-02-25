# Generated by Django 2.2 on 2021-02-24 08:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('depthead', '0025_auto_20210224_1441'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result_Semester_List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Semester', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Syllabus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Syllabus_Name', models.CharField(max_length=100)),
                ('Year_created', models.CharField(max_length=20)),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='depthead.Dept')),
            ],
        ),
        migrations.CreateModel(
            name='Sessions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Batch', models.CharField(max_length=40)),
                ('Session', models.CharField(max_length=20)),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='depthead.Dept')),
                ('syllabus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='depthead.Syllabus')),
            ],
        ),
        migrations.CreateModel(
            name='Result_Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Reg', models.CharField(max_length=20)),
                ('Name', models.CharField(max_length=40)),
                ('Column_01', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_02', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_03', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_04', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_05', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_06', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_07', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_08', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_09', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_10', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_11', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_12', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_13', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_14', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_15', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_16', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_17', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_18', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_19', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_20', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_21', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_22', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_23', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_24', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_25', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_26', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_27', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_28', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_29', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_30', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_31', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_32', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_33', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_34', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_35', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_36', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_37', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_38', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_39', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_40', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_41', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_42', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_43', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_44', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_45', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_46', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_47', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_48', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_49', models.CharField(blank=True, max_length=20, null=True)),
                ('Column_50', models.CharField(blank=True, max_length=20, null=True)),
                ('result_semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='depthead.Result_Semester_List')),
            ],
        ),
        migrations.AddField(
            model_name='result_semester_list',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='depthead.Sessions'),
        ),
        migrations.CreateModel(
            name='Course_Semester_List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Semester', models.CharField(max_length=20)),
                ('syllabus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='depthead.Syllabus')),
            ],
        ),
        migrations.CreateModel(
            name='Course_List_All',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=100)),
                ('credit', models.FloatField(max_length=10)),
                ('course_type', models.CharField(max_length=20)),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='depthead.Dept')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='depthead.Course_Semester_List')),
            ],
        ),
    ]
