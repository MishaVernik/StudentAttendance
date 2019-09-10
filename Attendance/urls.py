from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
import imaplib
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    url(r'^accounts/profile/$', views.home, name="home"),
    #url(r'^login/$', django.contrib.auth.views.LoginView, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page="login"), name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
   # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #    views.activate, name='activate'),
]