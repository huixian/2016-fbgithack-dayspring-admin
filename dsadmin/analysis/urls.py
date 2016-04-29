from django.conf.urls import url

from . import views

urlpatterns = [

   	url(r'^donations/([0-9]{4})/$', views.donations, name="donations"),
   	url(r'^donations/target/([0-9]{4})/$', views.target, name="target"),

   	# test
   	url(r'^donations/(?P<year>[0-9]{4})/$', views.donations, name="donations"),

]
