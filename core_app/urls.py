from django.conf.urls import url
from . import views

app_name = 'core_app'

urlpatterns = [
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^report_upload/$', views.report_upload, name='report_upload'),
    url(r'^home/$', views.home, name='home'),
]
