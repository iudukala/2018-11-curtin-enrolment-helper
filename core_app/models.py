# TESTING
from django.db import models
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location='/Users/Eugene/SEP1_Project/2017-11.3-enrolment-helper/core_app/storage')

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

# Credential for representing authenticated login info
class Credential(models.Model):
    StaffID = models.CharField(max_length=7, primary_key=True)
    Name = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)

# Student for representing student information.
class Student(models.Model):
    StudentID = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=100)
    CreditsCompleted = models.IntegerField()
    # 1 - good standing, 0 - conditional and -1 - terminated
    AcademicStatus = models.IntegerField(validators=[-1, 0, 1])
    CourseID = models.ForeignKey(Course)

class StudentUnit(models.Model):
    class Meta:
        unique_together = (('StudentID', 'UnitID'),)
    StudentID = models.ForeignKey(Student, on_delete=models.PROTECT)
    UnitID = models.ForeignKey(Unit, on_delete=models.PROTECT)

    Attempts = models.IntegerField()
    # True is pass but False is failed
    Status = models.BooleanField(default=False)
    PrerequisteAchieved = models.BooleanField(default=False)

    # def _str__(self):
    #     # return StudentID + " " + UnitID
    #     return "{} {}".format(self.StudentID, self.UnitID)

#
class CourseTemplate(models.Model):
    class Meta:
        unique_together = (('CourseID', 'UnitID'),)

    #
    CourseID = models.ForeignKey(Course, on_delete=models.CASCADE)
    UnitID = models.ForeignKey(Unit, on_delete=models.PROTECT)

    #
    CourseUnitID = models.IntegerField(primary_key=True)

    #
    Year = models.IntegerField(validators=[1, 2, 3, 4])
    Semester = models.IntegerField(validators=[1, 2])


#Class UploadedFile supports for UploadedFileForm in forms.py and allow us to access to FileField pointer
# class UploadedFile(models.Model):
#     title = models.CharField(max_length=255, unique=True)
#     parsed_file = models.FileField()
#
#     def __unicode__(self):
#         return self.title
#
