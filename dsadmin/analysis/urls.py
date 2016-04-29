from django.conf.urls import url

from . import views

urlpatterns = [

	url(r'^donations/$', views.donations, name="donations"),
	url(r'^donations/target/$', views.target, name="target"),

	url(r'^donors/inactive/$', views.donors_inactive, name="donors_inactive"),

]
