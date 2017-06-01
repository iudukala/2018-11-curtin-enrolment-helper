# -*- coding: utf-8 -*-
<<<<<<< HEAD
# Generated by Django 1.10.6 on 2017-05-27 15:33
=======
# Generated by Django 1.10.6 on 2017-05-29 12:50
>>>>>>> 369377bd26a2e0abb1860ae7936bc9cefacc74c3
from __future__ import unicode_literals

import core_app.models
from django.db import migrations, models
import django.db.models.deletion
import fernet_fields.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CourseID', models.CharField(max_length=10)),
                ('Name', models.CharField(max_length=100)),
                ('Version', models.CharField(max_length=10)),
                ('TotalCredits', models.IntegerField(validators=[600, 800, 1000])),
            ],
        ),
        migrations.CreateModel(
            name='CourseTemplate',
            fields=[
                ('Option', models.IntegerField(primary_key=True, serialize=False)),
                ('MidYearEntry', models.BooleanField(default=False)),
                ('CourseID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_app.Course')),
            ],
        ),
        migrations.CreateModel(
            name='CourseTemplateOptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Year', models.IntegerField(validators=[1, 2, 3, 4])),
                ('Semester', models.IntegerField(validators=[1, 2])),
                ('Option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_app.CourseTemplate')),
            ],
        ),
        migrations.CreateModel(
            name='Equivalence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Prerequisite',
            fields=[
                ('Option', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('StudentID', models.IntegerField(primary_key=True, serialize=False)),
                ('Name', fernet_fields.fields.EncryptedCharField(max_length=100)),
                ('CreditsCompleted', models.DecimalField(decimal_places=1, max_digits=4)),
                ('AcademicStatus', models.IntegerField(validators=[-1, 0, 1])),
                ('MidYearEntry', models.BooleanField(default=False)),
                ('CourseID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_app.Course')),
            ],
        ),
        migrations.CreateModel(
            name='StudentUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Attempts', fernet_fields.fields.EncryptedIntegerField()),
                ('Status', fernet_fields.fields.EncryptedIntegerField(default=1, validators=[1, 2, 3])),
                ('PrerequisiteAchieved', core_app.models.EncryptedBooleanField(default=False)),
                ('Year', models.IntegerField(default=-1, validators=[-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])),
                ('Semester', models.IntegerField(default=-1, validators=[1, 2])),
                ('StudentID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core_app.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
<<<<<<< HEAD
                ('UnitID', models.AutoField(primary_key=True, serialize=False)),
=======
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
>>>>>>> 369377bd26a2e0abb1860ae7936bc9cefacc74c3
                ('UnitCode', models.CharField(max_length=10)),
                ('Name', models.CharField(max_length=100)),
                ('Version', models.CharField(max_length=10)),
                ('Semester', models.IntegerField(validators=[1, 2, 3])),
                ('Credits', models.DecimalField(decimal_places=1, max_digits=3, validators=[12.5, 25, 50])),
                ('Elective', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='unit',
            unique_together=set([('UnitCode', 'Version', 'Credits')]),
        ),
        migrations.AddField(
            model_name='studentunit',
            name='UnitID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core_app.Unit'),
        ),
        migrations.AddField(
            model_name='prerequisite',
            name='UnitID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ThisUnit', to='core_app.Unit'),
        ),
        migrations.AddField(
            model_name='options',
            name='Option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Opt', to='core_app.Prerequisite'),
        ),
        migrations.AddField(
            model_name='options',
            name='UnitID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='OptUnit', to='core_app.Unit'),
        ),
        migrations.AddField(
            model_name='equivalence',
            name='EquivID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='EquivalentUnit', to='core_app.Unit'),
        ),
        migrations.AddField(
            model_name='equivalence',
            name='UnitID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Unit', to='core_app.Unit'),
        ),
        migrations.AddField(
            model_name='coursetemplateoptions',
            name='UnitID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_app.Unit'),
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together=set([('CourseID', 'Version')]),
        ),
        migrations.AlterUniqueTogether(
            name='studentunit',
            unique_together=set([('StudentID', 'UnitID')]),
        ),
        migrations.AlterUniqueTogether(
            name='prerequisite',
            unique_together=set([('Option', 'UnitID')]),
        ),
        migrations.AlterUniqueTogether(
            name='options',
            unique_together=set([('UnitID', 'Option')]),
        ),
        migrations.AlterUniqueTogether(
            name='equivalence',
            unique_together=set([('EquivID', 'UnitID')]),
        ),
        migrations.AlterUniqueTogether(
            name='coursetemplateoptions',
            unique_together=set([('UnitID', 'Option')]),
        ),
        migrations.AlterUniqueTogether(
            name='coursetemplate',
            unique_together=set([('CourseID', 'Option', 'MidYearEntry')]),
        ),
    ]
