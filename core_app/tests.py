from django.test import TestCase
from django.http import cookie
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import *
# from .views import *
from .forms import UploadedFile
from django.test import RequestFactory
# from .views import UploadedFile

# Create your tests here.

class pdf_validation(TestCase):
    @classmethod
    def setUpTestData(cls):
        # cls.student = Student.objects.create(StudentID='17080170', Name='Jack')
        # TODO: Creating a database which should pass.
        cls.course1 = Course.objects.create(CourseID=307808, Version=2, TotalCredits=12.5)
        cls.course2 = Course.objects.create(CourseID=313605, Version=1, TotalCredits=25)
        cls.student = Student.objects.create(StudentID=1171921, Name='Jack', CreditsCompleted=300, AcademicStatus=1, CourseID=cls.course1)

        request_factory = RequestFactory()

        request_data = {"course":
                          {"307808": "2",
                           "313605": "1",
                           },
                      "id": "1171921",
                      "name": "Mr Campbell James Pedersen",
                      "date": "21 Feb 2017"
                      }
        # cls.file_data =

        test_request = request_factory.post('/pdfFileUpload', data=request_data)

        # file = SimpleUploadedFile('testfile.txt', str(data).encode('utf-8', 'strict'))
        # cls.test_form = UploadedFile(file.POST, file)
        cls.test_form = UploadedFile(test_request.POST, test_request.FILES)

    def testFile(self):
        assert isinstance(self.student, Student)
        assert isinstance(self.course1, Course)
        assert isinstance(self.course2, Course)
        self.assertTrue(self.test_form.is_valid, "Should not fail")
        self.assertFalse(self.test_form.is_valid, "Should fail")
        # test_form = UploadedFile(self.file.POST, self.file.FILES)
        # self.assertTrue(self.test_form.is_valid())
        # self.assertEquals(True, self.test_form.is_valid())
        # self.assertEquals(False, self.test_form.is_valid())
        # self.assertEqual(self, False, UploadedFile(self.file.POST, self.file.FILES), "Should fail")


# class MyTests(TestCase):
# class DatabaseTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Place to setup data for the entire TestCase.
#         # cls.person = Person.objects.create()
#         cls.student = Student.objects.create()
#         cls.student.StudentID = '17080170'
#         cls.student.Name = 'Jack'
#
#     def testName(self):
#         assert isinstance(self.student, Student)
#         self.assertEqual(self.student.StudentID, "17080170", "Checking constructors first_name")
#         self.assertEqual(self.student.Name, "Wrong name", "Checking constructors last_name")

