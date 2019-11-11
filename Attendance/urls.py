from django.conf.urls import url
from django.contrib.auth import views as auth_views

import Attendance.Controllers.GetLocation
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    url(r'^accounts/profile/$', views.home, name="home"),
    url(r'^accounts/profile/teacher/$', views.homeTeacher, name="homeTeacher"),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    #url(r'^login/$', django.contrib.auth.views.LoginView, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page="login"), name='logout'),
    url(r'^signup/teacher/$', views.signUpTeacher, name='signupTeacher'),
    url(r'^location/student/$', Attendance.Controllers.GetLocation.getStudentsLocation, name='locationStudent'),
    url(r'^location/teacher/$', Attendance.Controllers.GetLocation.getTeachersLocation, name='locationTeacher'),
    url(r'^signup/$', views.signupStudent, name='signupStudent'),
   # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #    views.activate, name='activate'),
]