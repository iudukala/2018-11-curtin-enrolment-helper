# <<<<<<< HEAD
"""
Various url patterns/routing relating the the main application.
"""
from django.conf.urls import url

from . import views

app_name = 'core_app'

urlpatterns = [

    url(r'^$', views.home, name='index'),
    url(r'^pdfFileUpload$', views.upload_file, name='pdfFileUpload'),
    url(r'^getStudentList$', views.get_student_list, name='getStudentList'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^report_upload/$', views.report_upload, name='report_upload'),
    url(r'^planner/$', views.planner, name='planner'),
    url(r'^home/$', views.home, name='home'),
    url(r'^emailplan$', views.email_to_student, name='emailplan')
]

# =======
# from django.conf.urls import url
# from . import views
#
# app_name = 'core_app'
#
# urlpatterns = [
#     url(r'^login/$', views.login_user, name='login_user'),
#     url(r'^logout/$', views.logout_user, name='logout_user'),
#     url(r'^report_upload/$', views.report_upload, name='report_upload'),
#     url(r'^planner/$', views.planner, name='planner'),
#     url(r'^home/$', views.home, name='home'),
# >>>>>>> develop
# ]
