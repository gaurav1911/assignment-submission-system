from django.conf.urls import url
from application import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'register/$', views.register, name='register'),
    url(r'login/$', views.login_user, name='login'),
    url(r'profile/$', views.profile, name='profile'),
    url(r'logout/$', views.logout_user, name='logout'),
    url(r'assignment/(?P<assign_id>[0-9]+)$', views.detail, name='detail'),
    url(r'submit/$', views.submit, name='submit'),
]
