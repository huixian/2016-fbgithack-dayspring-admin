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

	try:
		year = int(year)
	except Exception as e:
		return HttpResponse(0, status=500, content_type="application/json")

	response_data = services.get_donation_by_year(year)

	return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), status=200, content_type="application/json")

@csrf_exempt
def target(request):

	year = request.GET['year']

	try:
		year = int(year)
	except Exception as e:
		return HttpResponse(0, status=500, content_type="application/json")

	response_data = services.get_donation_target_by_year(year)

	return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), status=200, content_type="application/json")

@csrf_exempt
def donors_inactive(request):

	unit_list = ['days', 'weeks', 'months', 'years']

	unit = request.GET['unit']
	value = request.GET['value']

	if not (unit in unit_list):
		return HttpResponse(0, status=500, content_type="application/json")

	try:
		value = int(value)
	except Exception as e:
		return HttpResponse(0, status=500, content_type="application/json")

	response_data = services.get_lapsed_donors(unit, value)
	return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), status=200, content_type="application/json")

@csrf_exempt
def donors_top(request):

	year = request.GET['year']
	num = request.GET['num']

	try:
		year = int(year)
	except Exception as e:
		return HttpResponse(0, status=500, content_type="application/json")

	try:
		num = int(num)
	except Exception as e:
		return HttpResponse(0, status=500, content_type="application/json")

	response_data = services.get_top_donor_list_by_year(year, num)

	return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), status=200, content_type="application/json")