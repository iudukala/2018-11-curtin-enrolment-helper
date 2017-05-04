from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Unit)
admin.site.register(Equivalence)
admin.site.register(Prerequiste)
admin.site.register(Credential)
admin.site.register(StudentUnit)
admin.site.register(CourseTemplate)
