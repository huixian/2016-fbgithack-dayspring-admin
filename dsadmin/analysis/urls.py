from django.conf.urls import url

from . import views

urlpatterns = [

   	url(r'^donations$', views.donations, name="donations"),
]
