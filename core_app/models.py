from django.db import models


# Course Table - Stores all the course that the department provides.
class Course(models.Model):
    CourseID = models.CharField(max_length=10, primary_key=True)
    Name = models.CharField(max_length=100)
    Version = models.CharField(max_length=10)
    TotalCredits = models.IntegerField(validators=[600])


# Unit Table - Stores all the units that the department provides.
class Unit(models.Model):
    UnitID = models.CharField(max_length=100, primary_key=True)
    UnitCode = models.CharField(max_length=10)
    Name = models.CharField(max_length=100)
    Version = models.CharField(max_length=10)
    # Availability: 1 = Semester 1, 2 = Semester 2, 3 = Semester 1 & 2.
    Semester = models.IntegerField(validators=[1, 2, 3])
    Credits = models.DecimalField(decimal_places=1, max_digits=3, validators=[12.5, 25, 50])


# Equivalence Table - Keeps track of which unit is equivalent to which unit.
class Equivalence(models.Model):
    class Meta:
        unique_together = (('EquivID', 'UnitID'),)

    UnitID = models.ForeignKey(Unit, related_name='Unit', on_delete=models.CASCADE)
    EquivID = models.ForeignKey(Unit, related_name='EquivalentUnit', on_delete=models.CASCADE)


# Prerequisite Table - Keeps track of which unit is the prerequisite of which unit.
class Prerequisite(models.Model):
    class Meta:
        unique_together = (('PreUnitID', 'UnitID'),)

    UnitID = models.ForeignKey(Unit, related_name='ThisUnit', on_delete=models.CASCADE)
    PreUnitID = models.ForeignKey(Unit, related_name='PreUnit', on_delete=models.CASCADE)
    # This is to keep track if the prerequisite unit is either an AND or an OR relation to the unit.
    # AND is False, OR is True.
    AndOr = models.BooleanField(default=False)


# Credential Table - Stores access information to eTracker.
#class Credential(models.Model):
#    StaffID = models.CharField(max_length=7, primary_key=True)
#    Name = models.CharField(max_length=100)
#    Password = models.CharField(max_length=100)


# Student Table - Stores essential information of student.
class Student(models.Model):
    StudentID = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=100)
    CreditsCompleted = models.IntegerField()
    # 1 - good standing, 0 - conditional and -1 - terminated
    AcademicStatus = models.IntegerField(validators=[-1, 0, 1])
    CourseID = models.ForeignKey(Course)


# StudentUnit Table - Keeps track of which unit within the student plan.
class StudentUnit(models.Model):
    class Meta:
        unique_together = (('StudentID', 'UnitID'),)

    StudentID = models.ForeignKey(Student, on_delete=models.PROTECT)
    UnitID = models.ForeignKey(Unit, on_delete=models.PROTECT)

    Attempts = models.IntegerField()
    # Student passed or failed status.
    # 1 = Not Done, 2 = passed, 3 = failed
    Status = models.IntegerField(default=1, validators=[1, 2, 3])
    PrerequisiteAchieved = models.BooleanField(default=False)
    Year = models.IntegerField(validators=[1, 2, 3, 4])
    Semester = models.IntegerField(validators=[1, 2])


# CourseTemplate Table - Keeps track of which course contains which units.
class CourseTemplate(models.Model):
    class Meta:
        unique_together = (('CourseID', 'UnitID'),)

    CourseID = models.ForeignKey(Course, on_delete=models.CASCADE)
    UnitID = models.ForeignKey(Unit, on_delete=models.PROTECT)
    CourseUnitID = models.IntegerField(primary_key=True)
    Year = models.IntegerField(validators=[1, 2, 3, 4])
    Semester = models.IntegerField(validators=[1, 2])
