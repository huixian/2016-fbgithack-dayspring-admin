from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError, HttpResponseNotFound, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics, permissions, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
import datetime, time, json
import services

# Create your views here.

@csrf_exempt
def donations(request):

	year = request.GET['year']
	response_data = services.get_donation_by_year(year)

	return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), status=200, content_type="application/json")

@csrf_exempt
def target(request):

	year = request.GET['year']
	response_data = services.get_donation_target_by_year(year)

	return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), status=200, content_type="application/json")

@csrf_exempt
def donors_inactive(request):

	unit = request.GET['unit']
	value = request.GET['value']

	response_data = services.get_donation_target_by_year(year)

	return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), status=200, content_type="application/json")
