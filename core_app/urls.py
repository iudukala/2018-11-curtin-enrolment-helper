from django.conf.urls import url
from . import views

add_name = 'core_app'

urlpatterns = [
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^report_upload/$', views.report_upload, name='upload'),
]
