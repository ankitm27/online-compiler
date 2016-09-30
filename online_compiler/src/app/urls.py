from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from app import views

urlpatterns = [
	url(r'^$', views.Home.as_view(), name='home'),
	url(r'^register/$', views.Register.as_view(), name='register'),
	url(r'^login/$', views.Login.as_view(), name='login'),
	url(r'^profile/$', views.Profile.as_view(), name='profile'),
	url(r'^change_password/$', views.ChangePassword.as_view(), name='change_password'),
	url(r'^logout/$', views.Logout.as_view(), name='logout'),
	url(r'^contact/$', views.Contact.as_view(), name='contact'),
	url(r'^about/$', views.About.as_view(), name='about'),
	url(r'^forget_password/$', views.ForgetPassword.as_view(), name='forget_password'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
# (u?P<pk>[0-9]+)/