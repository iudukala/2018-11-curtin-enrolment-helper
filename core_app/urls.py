'''
Various url patterns/routing relating the the main application.
'''
from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$', views.index, name='index'),
    # url(r'^testView$', views.test_view, name='test'),
    url(r'^pdfFileUpload$', views.upload_file, name='pdfFileUpload'),
    url(r'^getStudentList$', views.get_student_list, name='getStudentList'),
    # url(r'^parseDataIsValid$', views.check_parsed_information, name='check_parsed_information'),

]
