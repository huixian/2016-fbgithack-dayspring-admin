from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError, HttpResponseNotFound, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics, permissions, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
# from .serializers import MedSurveySerializer, SleepSurveySerializer
import datetime, time


# Create your views here.

def donations(request):

	print("test")

	output = 1

	return HttpResponse(output)
