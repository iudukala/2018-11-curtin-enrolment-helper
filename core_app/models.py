from django.db import models


# Course Table - Stores all the course that the department provides.
class Course(models.Model):
    CourseID = models.CharField(max_length=10, primary_key=True)
    Name = models.CharField(max_length=100)
    Version = models.CharField(max_length=10)
    TotalCredits = models.IntegerField(validators=[600])


# Unit Table - Stores all the units that the department provides.
class Unit(models.Model):
    UnitID = models.AutoField(primary_key=True)
    UnitCode = models.CharField(max_length=10)
    Name = models.CharField(max_length=100)
    Version = models.CharField(max_length=10)
    # Availability: 1 = Semester 1, 2 = Semester 2, 3 = Semester 1 & 2.
    Semester = models.IntegerField(validators=[1, 2, 3])
    Credits = models.DecimalField(decimal_places=1, max_digits=3, validators=[12.5, 25, 50])
    Elective = models.BooleanField(default=False)

# Equivalence Table - Keeps track of which unit is equivalent to which unit.
class Equivalence(models.Model):
    class Meta:
        unique_together = (('EquivID', 'UnitID'),)

    UnitID = models.ForeignKey(Unit, related_name='Unit', on_delete=models.CASCADE)
    EquivID = models.ForeignKey(Unit, related_name='EquivalentUnit', on_delete=models.CASCADE)


# Prerequisite Table - This table can be a representation of an AND's table. This table stores units to an option,
#                      which when getting a particular unit it will give all records of that unit which gives a set of
#                      options.
class Prerequisite(models.Model):
    class Meta:
        unique_together = (('Option', 'UnitID'),)

    UnitID = models.ForeignKey(Unit, related_name='ThisUnit', on_delete=models.CASCADE)
    Option = models.IntegerField(primary_key=True)


# Options Table - This table can be a representation of an OR's table. This table stores units to an option, which when
#                 getting the option record will give all the units in the option.
class Options(models.Model):
    class Meta:
        unique_together = (('UnitID', 'Option'),)

    UnitID = models.ForeignKey(Unit, related_name='OptUnit', on_delete=models.CASCADE)
    Option = models.ForeignKey(Prerequisite, related_name='Opt', on_delete=models.CASCADE)


# Credential Table - Stores access information to eTracker.
# class Credential(models.Model):
#      StaffID = models.CharField(max_length=7, primary_key=True)
#      Name = models.CharField(max_length=100)
#      Password = models.CharField(max_length=100)


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
    Year = models.IntegerField()
    Semester = models.IntegerField(validators=[1, 2])


# CourseTemplate Table - Table can be a representation of an AND's table. Each course has a couple of option records,
#                        which can be used to find which the list of units in that course.
class CourseTemplate(models.Model):
    class Meta:
        unique_together = (('CourseID', 'Option'),)

    Option = models.IntegerField(primary_key=True)
    CourseID = models.ForeignKey(Course, on_delete=models.CASCADE)


# CourseTemplateOptions Table - Table can be a representation of an OR's table. Each option has a unit linked to it.
#                               A list of unit for that option will be given when an option is queried.
class CourseTemplateOptions(models.Model):
    class Meta:
        unique_together = (('UnitID', 'Option'),)

    Option = models.ForeignKey(CourseTemplate, on_delete=models.CASCADE)
    UnitID = models.ForeignKey(Unit, on_delete=models.CASCADE)
    Year = models.IntegerField(validators=[1, 2, 3, 4])
    Semester = models.IntegerField(validators=[1, 2])
