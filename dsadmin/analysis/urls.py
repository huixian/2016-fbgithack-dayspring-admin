from django.conf.urls import url

from . import views

urlpatterns = [

   	url(r'^donations/([0-9]{4})/$', views.donations, name="donations"),
]
