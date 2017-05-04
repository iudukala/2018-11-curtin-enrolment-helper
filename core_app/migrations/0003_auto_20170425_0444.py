# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-25 04:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0002_auto_20170421_0604'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('CourseID', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=100)),
                ('Version', models.CharField(max_length=10)),
                ('TotalCredits', models.IntegerField(validators=[600])),
            ],
        ),
        migrations.CreateModel(
            name='CourseTemplate',
            fields=[
                ('CourseUnitID', models.IntegerField(primary_key=True, serialize=False)),
                ('Year', models.IntegerField(validators=[1, 2, 3, 4])),
                ('Semester', models.IntegerField(validators=[1, 2])),
                ('CourseID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_app.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Credential',
            fields=[
                ('StaffID', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=100)),
                ('Password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Equivalence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Prerequiste',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AndOr', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('StudentID', models.IntegerField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=100)),
                ('CreditsCompleted', models.IntegerField()),
                ('AcademicStatus', models.IntegerField(validators=[-1, 0, 1])),
                ('CourseID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_app.Course')),
            ],
        ),
        migrations.CreateModel(
            name='StudentUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Attempts', models.IntegerField()),
                ('Status', models.BooleanField(default=False)),
                ('PrerequisteAchieved', models.BooleanField(default=False)),
                ('StudentID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core_app.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('UnitID', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('UnitCode', models.CharField(max_length=10)),
                ('Name', models.CharField(max_length=100)),
                ('Version', models.CharField(max_length=10)),
                ('Semester', models.IntegerField(validators=[1, 2, 3])),
                ('Credits', models.DecimalField(decimal_places=1, max_digits=3, validators=[12.5, 25, 50])),
            ],
        ),
        migrations.DeleteModel(
            name='Person',
        ),
        migrations.AddField(
            model_name='studentunit',
            name='UnitID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core_app.Unit'),
        ),
        migrations.AddField(
            model_name='prerequiste',
            name='PreUnitID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='PreUnit', to='core_app.Unit'),
        ),
        migrations.AddField(
            model_name='prerequiste',
            name='UnitID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ThisUnit', to='core_app.Unit'),
        ),
        migrations.AddField(
            model_name='equivalence',
            name='EquivaID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='EquivalentUnit', to='core_app.Unit'),
        ),
        migrations.AddField(
            model_name='equivalence',
            name='UnitID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Unit', to='core_app.Unit'),
        ),
        migrations.AddField(
            model_name='coursetemplate',
            name='UnitID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core_app.Unit'),
        ),
        migrations.AlterUniqueTogether(
            name='studentunit',
            unique_together=set([('StudentID', 'UnitID')]),
        ),
        migrations.AlterUniqueTogether(
            name='prerequiste',
            unique_together=set([('PreUnitID', 'UnitID')]),
        ),
        migrations.AlterUniqueTogether(
            name='equivalence',
            unique_together=set([('EquivaID', 'UnitID')]),
        ),
        migrations.AlterUniqueTogether(
            name='coursetemplate',
            unique_together=set([('CourseID', 'UnitID')]),
        ),
    ]