from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),

   	# url(r'^$', views.api_root),

   	url(r'^donations$', views.donations, name="donations"),
]
