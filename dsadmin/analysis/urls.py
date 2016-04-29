from django.conf.urls import url

from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),

   	# url(r'^$', views.api_root),

    # url(r'^medsurvey/$', views.MedSurveyList.as_view(), name='medsurvey_list'),
    # url(r'^targetbymonth/$', views.target_by_month.as_view(), name='target_by_month'),
]
