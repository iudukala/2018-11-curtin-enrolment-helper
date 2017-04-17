from django.db import models

class Course(models.Model):
    CourseID = models.CharField(max_length=10, primary_key=True)
    Name = models.CharField(max_length=100)
    Version = models.CharField(max_length=10)
    TotalCredits = models.IntegerField(validators=[600])

class Unit(models.Model):
    UnitID = models.CharField(max_length=100, primary_key=True)
    UnitCode = models.CharField(max_length=10)
    Name = models.CharField(max_length=100)
    Version = models.CharField(max_length=10)
    # 1=semster_1, 2=semester_2 and 3=semester(1 and 2)
    Semester = models.IntegerField(validators=[1, 2, 3])
    Credits = models.DecimalField(decimal_places=1, max_digits=3, validators=[12.5, 25, 50])

class Equivalence(models.Model):
    class Meta:
        unique_together = (('EquivaID', 'UnitID'),)
    EquivaID = models.ForeignKey(Unit, related_name='EquivalentUnit', on_delete=models.CASCADE)
    UnitID = models.ForeignKey(Unit, related_name='Unit', on_delete=models.CASCADE)

class Prerequiste(models.Model):
    class Meta:
        unique_together = (('PreUnitID', 'UnitID'),)
    PreUnitID = models.ForeignKey(Unit, related_name='PreUnit', on_delete=models.CASCADE)
    UnitID = models.ForeignKey(Unit, related_name='ThisUnit', on_delete=models.CASCADE)
    # And is false, and Or is true
    AndOr = models.BooleanField(default=False)
