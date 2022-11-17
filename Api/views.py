from django.shortcuts import render
import datetime
import jwt
# import api.emailpattern as em
from decouple import config
from django.conf import settings
from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import render
from passlib.hash import django_pbkdf2_sha256 as handler
from rest_framework.response import Response
from rest_framework.views import APIView
# import stripe

# import Api.usable as uc
from .models import *
# Create your views here.

class categoryAdd(APIView):

### CATEGORY ADD
   def post(self,request):
      requireFields = ['name','description']
      validator = uc.keyValidation(True,True,request.data,requireFields)
            
      if validator:
         return Response(validator,status = 200)
            
      else:
         my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
         if my_token:
            name  = request.data.get('name')
            description = request.data.get('description')
            
            access = Category.objects.filter(name = name ).first()
            if access:
               return Response({"status":False,"message":"Category Name Already Exist"})
               
            data = Category(name = name, description = description)
            data.save()

            return Response ({"status":True,"message":"Category Successlly Add"})

         else:
            return Response ({"status":False,"message":"Unauthorized"})