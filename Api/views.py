from django.shortcuts import render
import datetime
import jwt
from decouple import config
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import render
from passlib.hash import django_pbkdf2_sha256 as handler
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework import generics
from .serializer import* 
import Api.usable as uc
from .models import *              
import random

# All Roles Crud
# Role Post_Api
class roles(APIView):
    def post(self, request):
            requireFields = ['role']
            validator = uc.keyValidation(True,True,request.data,requireFields)

            if validator:
                return Response(validator,status = 200)   

            else:       
                my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
                if my_token:
                    role  = request.data.get('role')
                    
                    data = Role(role=role)
                    data.save()

                    return Response ({"status":True,"message":"Successfully Add"})
                else:
                    return Response({"status": False, "msg":"Unauthorized"})    
# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# Role get_Api    
    def get(self, request):
        my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            data = Role.objects.all().values('role')
                
            return Response({'status':True, 'data': data})       
        else:
            return Response({"status": False, "msg":"Unauthorized"})  

####################################################################################################################  
# Role Put_Api
  
    def put(self, request):
        my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            requireFields = ['role','uid']
            
            validator = uc.keyValidation(True,True,request.data,requireFields)

            if validator:
                return Response(validator,status = 200)   

            else:       
                uid = request.data.get('uid')       
                role = request.data.get("role")  

                admin = Role.objects.filter(uid=uid).first()
                if admin:
                    admin.role=role
                    admin.save()

                    return Response({'status': True, 'Msg': 'data Update Successfully'}) 

                else:
                    return Response({"status": False, "msg":"invalid_Credentials"})
        else:
            return Response({"status": False, "msg":"Unauthorized"})    
####################################################################################################################################################
# Role delete_Api
    
    def delete(self,request):
        my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            requireField = ['uid']
            validator = uc.keyValidation(True,True,request.GET,requireField)
 
            if validator:
                return Response(validator,status = 200)   

            else:
                uid = request.GET['uid']
                data = Role.objects.filter(uid=uid).first()       
                if data:
                    data.delete()
                    
                    return Response({'status': True, 'Msg': 'data Delete Successfully'})
                else:
                    return Response({"status": False, "msg":"Unauthorized"})
#     
        else:
            return Response({"status": False, "msg":"Unauthorized"})
# ==================================================================================================================================================
# ROLE-GETSPECIFIC/API

class datagets(APIView):
      def get(self,request):
          my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
          if my_token:  
            requireFields = ['uid']
            validator = uc.keyValidation(True,True,request.GET,requireFields)
        
            if validator:
                return Response(validator,status = 200)
        
            else:
                uid = request.GET['uid']

            data = Role.objects.filter(uid=uid).values('role').first()       
        
            if data:
                return Response({'status': True, 'Msg': 'data Get Successfully', 'data': data}) 
            else:
                return Response({"status": False, "msg":"Unauthorized"})
          else:
            return Response({"status": False, "msg":"Token Unauthorized"})    

# Role_Account/API

class Register(APIView):
   def post (self,request):
        requireFields = ['firstname','lastname','email','password','contact']
        validator = uc.keyValidation(True,True,request.data,requireFields)
               
        if validator:
            return Response(validator,status = 200)
               
        else:
            firstname = request.data.get('firstname')
            lastname = request.data.get('lastname')
            email = request.data.get('email')
            password = request.data.get('password')
            contact = request.data.get('contact')
            role_id = request.data.get('role_id')

            objrole = Role.objects.filter(role = 'customer').first()

            if uc.checkemailforamt(email):
                if not uc.passwordLengthValidator(password):
                    return Response({"status":False, "message":"password should not be than 8 or greater than 20"})

                checkemail=Account.objects.filter(email=email).first()
                if checkemail:
                    return Response({"status":False, "message":"Email already exists"})
            
                checkphone=Account.objects.filter(contact=contact).first()
                if checkphone:
                    return Response({"status":False, "message":"phone no already existsplease try different number"})

                data = Account(firstname = firstname, lastname = lastname, email=email, password=handler.hash(password), contact=contact, role_id=objrole)
                
                data.save()

                return Response({"status":True,"message":"Account Created Successfully"})
            else:
                return Response({"status":False,"message":"Email Format Is Incorrect"})


# send_mail Api

class Otp_sending(APIView):
    def post(self, request):
        email = request.data.get('email')
        
        code = random.randint(99999,999999)
                
        if uc.checkemailforamt(email):    
            checkemail=Account.objects.filter(email=email).first()
            if checkemail:
                return Response({"status":False, "message":"Email already exists"})
        
            else:
                send_mail('Verification Email',f'Here is your verification code "{code}"','EMAIL_HOST_USER',[email],fail_silently=False,
)

                return Response({"status":True,"message":"OTP send Successfully!",'otp':code})
        else:
            return Response({"status":False,"message":"Email Format Is Incorrect"})


# verify code_Api

class verify_otpcode(APIView):
        def post(self,request):
            code=request.data.get('code')
            email=request.data.get('email')

            objverify =  Account.objects.filter(email=email).first()
            
            if objverify:
                if (objverify.oTP==int(code)):

                    objverify.oTPStatus='True'
                    objverify.save()
                    return Response({"status":True, 'Msg':' VerifIcation Is True'})      
                else:
                    return Response({"status":False,  'Msg':'Invalid Code'})    
            else:
                return Response({"status":False,  'Msg':'Account doesnot Exists'})

# # ROLE-LOGIN/API

class login(APIView):
     def post(self,request):
         requireFields = ['email','password']
         validator = uc.keyValidation(True,True,request.data,requireFields)
            
         if validator:
            return Response(validator,status = 200)
            
         else:
               email = request.data.get('email')
               password = request.data.get('password')
               fetchAccount = Account.objects.filter(email=email).first()
               if fetchAccount:
                  if handler.verify(password,fetchAccount.password):
                     if fetchAccount.role_id.role == 'admin':
                        access_token_payload = {
                              'id':str(fetchAccount.uid),
                              'firstname':fetchAccount.firstname, 
                              'exp': datetime.datetime.utcnow() + datetime.timedelta(days=22),
                              'iat': datetime.datetime.utcnow(),

                           }

                        
                        access_token = jwt.encode(access_token_payload,config('adminkey'),algorithm = 'HS256')
                        data = {'uid':fetchAccount.uid,'firstname':fetchAccount.firstname,'lastname':fetchAccount.lastname,'contact':fetchAccount.contact,'email':fetchAccount.email, 'Login_As':str(fetchAccount.role_id)}

                        whitelistToken(token = access_token, user_agent = request.META['HTTP_USER_AGENT'],created_at = datetime.datetime.now(), role_id=fetchAccount).save()

                        return Response({"status":True,"message":"Login Successlly","token":access_token,"admindata":data})

                     if fetchAccount.role_id.role == 'superadmin':
                        access_token_payload = {
                              'id':str(fetchAccount.uid),
                              'firstname':fetchAccount.firstname, 
                              'email':fetchAccount.email, 
                              'role':fetchAccount.role_id.role, 
                              'exp': datetime.datetime.utcnow() + datetime.timedelta(days=22),
                              'iat': datetime.datetime.utcnow(),

                           }

                        
                        access_token = jwt.encode(access_token_payload,config('superadminkey'),algorithm = 'HS256')
                        data = {'uid':fetchAccount.uid,'firstname':fetchAccount.firstname,'lastname':fetchAccount.lastname,'contact':fetchAccount.contact, 'email':fetchAccount.email, 'Login_As':str(fetchAccount.role_id)}

                        whitelistToken(token = access_token, user_agent = request.META['HTTP_USER_AGENT'],created_at = datetime.datetime.now(), role_id=fetchAccount).save()

                        
                        return Response({"status":True,"message":"Login Successlly","token":access_token,"superadmindata":data})
                    
                    
                     if fetchAccount.role_id.role == 'manager':
                            access_token_payload = {
                            'id':str(fetchAccount.uid),
                            'firstname':fetchAccount.firstname, 
                            'email':fetchAccount.email, 
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=22),
                            'iat': datetime.datetime.utcnow(),

                            }

                            
                            access_token = jwt.encode(access_token_payload,config('managerkey'),algorithm = 'HS256')
                            data = {'uid':fetchAccount.uid,'firstname':fetchAccount.firstname,'lastname':fetchAccount.lastname,'contact':fetchAccount.contact,'email':fetchAccount.email, 'Login_As':str(fetchAccount.role_id)}

                            whitelistToken(token = access_token, user_agent = request.META['HTTP_USER_AGENT'],created_at = datetime.datetime.now(), role_id=fetchAccount).save()

                            
                            return Response({"status":True,"message":"Login Successlly","token":access_token,"managerdata":data})
                    
                     if fetchAccount.role_id.role  == 'customer':
                        access_token_payload = {
                              'id':str(fetchAccount.uid),
                              'firstname':fetchAccount.firstname, 
                              'email':fetchAccount.email, 
                              'exp': datetime.datetime.utcnow() + datetime.timedelta(days=22),
                              'iat': datetime.datetime.utcnow(),

                           }
                        access_token = jwt.encode(access_token_payload,config('customerkey'),algorithm = 'HS256')
                        data = {'uid':fetchAccount.uid,'firstname':fetchAccount.firstname,'lastname':fetchAccount.lastname,'contact':fetchAccount.contact,'email':fetchAccount.email, 'Login_As':str(fetchAccount.role_id)}

                        whitelistToken(token = access_token, user_agent = request.META['HTTP_USER_AGENT'],created_at = datetime.datetime.now(), role_id=fetchAccount).save()

                        
                        return Response({"status":True,"message":"Login Successlly","token":access_token,"customerdata":data})
                     else:
                        return Response({"status":False,"message":"Unable to login"})
                  else:
                     return Response({"status":False,"message":"Invalid Creadientialsl"})
               else:
                  return Response({"status":False,"message":"Unable to login"})

# SALOON-POST/API

class Salons(APIView):
    def post(self, request):
            requireFields = ['saloon_name','contact','city_id','role_id']
            validator = uc.keyValidation(True,True,request.data,requireFields)

            if validator:
                return Response(validator,status = 200)   

            else:       
                my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
                if my_token:
                    saloon_name  = request.data.get('saloon_name')
                    contact  = request.data.get('contact')
                    city_id  = request.data.get('city_id')
                    role_id  = request.data.get('role_id')

                    objcity = city.objects.filter(uid = city_id).first()
                    objrole = Role.objects.filter(uid = role_id).first()

                    checkphone=saloon.objects.filter(contact=contact).first()
                    if checkphone:
                        return Response({"status" : False, "message":"Contact number already exists please try different number"})

                    data = saloon(saloon_name=saloon_name,contact=contact, city_id=objcity, role_id=objrole)
                
                    data.save()

                    return Response ({"status":True,"message":"Successfully Add"})
                else:
                    return Response({"status": False, "msg":"Unauthorized"})    
# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# SALOON-GET/API
    
    def get(self, request):
        my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            data = saloon.objects.all().values('saloon_name','contact', Employee_Information=F('Employee_Detail__name'), CityName=F('city_id__name'), RoleName=F('role_id__role'))
                
            return Response({'status':True, 'data': data})       
        else:
            return Response({"status": False, "msg":"Unauthorized"})  

####################################################################################################################  
# SALOON-PUT/API
 
    def put(self, request):
        my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            requireFields = ['uid','saloon_name','contact','city_id','role_id']
            validator = uc.keyValidation(True,True,request.data,requireFields)

            if validator:
                return Response(validator,status = 200)   

            else:       
                uid = request.data.get('uid')       
                saloon_name = request.data.get("saloon_name")  
                contact = request.data.get("contact")  
                city_id = request.data.get("city_id")  
                role_id = request.data.get("role_id")  

                objchecked = city.objects.filter(uid = city_id).first()
                objcheck = Role.objects.filter(uid = role_id).first()
                
                admin = saloon.objects.filter(uid=uid).first()
                if admin:
                    admin.saloon_name=saloon_name
                    admin.contact=contact
                    admin.city_id=objchecked
                    admin.role_id=objcheck

                    admin.save()

                    return Response({'status': True, 'Msg': 'data Update Successfully'}) 
                    
                else:
                    return Response({"status": False, "msg":"invalid_Credentials"})
        else:
            return Response({"status": False, "msg":"Unauthorized"})    
####################################################################################################################################################
# SALOON-DELETE/API
   
    def delete(self,request):
        my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            requireField = ['uid']
            validator = uc.keyValidation(True,True,request.GET,requireField)
 
            if validator:
                return Response(validator,status = 200)   

            else:
                uid = request.GET['uid']
                data = saloon.objects.filter(uid=uid).first()       
                if data:
                    data.delete()
                    
                    return Response({'status': True, 'Msg': 'data Delete Successfully'})
                else:
                    return Response({"status": False, "msg":"Invalid_Credentials"})
#     
        else:
            return Response({"status": False, "msg":"Unauthorized"})
# ==================================================================================================================================================
# SALOON-GETSPECIFIC/API

class dataget_saloon(APIView):
      def get(self,request):
          my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
          if my_token:  
            requireFields = ['uid']
            validator = uc.keyValidation(True,True,request.GET,requireFields)
        
            if validator:
                return Response(validator,status = 200)
                
            else:
                uid = request.GET['uid']

            data = saloon.objects.filter(uid=uid).values('saloon_name','contact', CityName=F('city_id__name'), RoleName=F('role_id__role')).first()       
        
            if data:
                return Response({'status': True, 'Msg': 'data Get Successfully', 'data': data}) 
            else:
                return Response({"status": False, "msg":"Invalid_Credentials"})
          else:
            return Response({"status": False, "msg":"Unauthorized"})    


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# SURVICE-POST/API

class Survices(APIView):
    def post(self, request):
            requireFields = ['description','price','saloon_id','Added_by']
            validator = uc.keyValidation(True,True,request.data,requireFields)

            if validator:
                return Response(validator,status = 200)   

            else:       
                my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
                
                if my_token:
                
                    description  = request.data.get('description')
                    price  = request.data.get('price')
                    saloon_id  = request.data.get('saloon_id')
                    Added_by  = request.data.get('Added_by')

                    objsaloon = saloon.objects.filter(uid = saloon_id).first()
                    objAccount = Role.objects.filter(uid = Added_by).first()

                    data = service(description=description,price=price, saloon_id=objsaloon, Added_by=objAccount)
                
                    data.save()

                    return Response ({"status":True,"message":"Successfully Add"}) 
                else:
                    return Response({"status": False, "msg":"Unauthorized"})           
# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# SURVICE-GET/API
    
    def get(self, request):
        my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            data = service.objects.all().values('description','price', Saloon_Name=F('saloon_id__saloon_name'), Added_By=F('Added_by__role'))
                
            return Response({'status':True, 'data': data})       
        else:
            return Response({"status": False, "msg":"Unauthorized"})  

####################################################################################################################  
# SURVICE-PUT/API
 
    def put(self, request):
        my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            requireFields = ['uid', 'description','price','saloon_id','Added_by']
            validator = uc.keyValidation(True,True,request.data,requireFields)

            if validator:
                return Response(validator,status = 200)   

            else:       
                uid = request.data.get('uid')       
                description = request.data.get("description")  
                price = request.data.get("price")  
                saloon_id = request.data.get("saloon_id")  
                Added_by = request.data.get("Added_by")  

                objsaloon = saloon.objects.filter(uid = saloon_id).first()
                objAccount = Role.objects.filter(uid = Added_by).first()

                admin = service.objects.filter(uid=uid).first()
                if admin:
                    admin.description=description
                    admin.price=price
                    admin.saloon_id=objsaloon
                    admin.Added_by=objAccount

                    admin.save()

                    return Response({'status': True, 'Msg': 'data Update Successfully'}) 
                    
                else:
                    return Response({"status": False, "msg":"invalid_Credentials"})
        else:
            return Response({"status": False, "msg":"Unauthorized"})    
####################################################################################################################################################
# SURVICE-DELETE/API

    def delete(self,request):
        my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            requireField = ['uid']
            validator = uc.keyValidation(True,True,request.GET,requireField)
 
            if validator:
                return Response(validator,status = 200)   

            else:
                uid = request.GET['uid']
                data = service.objects.filter(uid=uid).first()       
                if data:
                    data.delete()
                    
                    return Response({'status': True, 'Msg': 'data Delete Successfully'})
                else:
                    return Response({"status": False, "msg":"Invalid_Credentials"})
#     
        else:
            return Response({"status": False, "msg":"Unauthorized"})
# ==================================================================================================================================================
# SURVICE-GETSPECIFIC/API

class dataget_survice(APIView):
      def get(self,request):
          my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
          if my_token:  
            requireFields = ['uid']
            validator = uc.keyValidation(True,True,request.GET,requireFields)
        
            if validator:
                return Response(validator,status = 200)
                
            else:
                uid = request.GET['uid']

            data = service.objects.filter(uid=uid).values('description','price', Saloon_Name=F('saloon_id__saloon_name'), Accountator_User=F('Added_by__role')).first()       
        
            if data:
                return Response({'status': True, 'Msg': 'data Get Successfully', 'data': data}) 
            else:
                return Response({"status": False, "msg":"Invalid_Credentials"})
          else:
            return Response({"status": False, "msg":"Unauthorized"})    

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# EMPLOYEE-POST/API

class Employees(APIView):
    def post(self, request):
            requireFields = ['name','contact','image','saloon_id','service_id','Added_by']
            validator = uc.keyValidation(True,True,request.data,requireFields)

            if validator:
                return Response(validator,status = 200)   

            else:       
                my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
                
                if my_token:
                
                    name  = request.data.get('name')
                    contact  = request.data.get('contact')
                    image  = request.data.get('image')
                    saloon_id  = request.data.get('saloon_id')
                    service_id  = request.data.get('service_id')
                    Added_by  = request.data.get('Added_by')

                    checkphone=employee.objects.filter(contact=contact).first()
                    if checkphone:
                        return Response({"status" : False, "message":"Contact number already exists please try different number"})
                    
                    objsaloon = saloon.objects.filter(uid = saloon_id).first()
                    objservice = service.objects.filter(uid = service_id).first()
                    objAdded_by = Role.objects.filter(uid = Added_by).first()

                    data = employee(name=name,contact=contact,image=image,saloon_id=objsaloon,service_id=objservice,Added_by=objAdded_by)
                
                    data.save()

                    return Response ({"status":True,"message":"Successfully Add"}) 
                else:
                    return Response({"status": False, "msg":"Unauthorized"})           
# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# EMPLOYEE-GET/API
    
    def get(self, request):
        my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            data = employee.objects.all().values('name','contact', Saloon_Name=F('saloon_id__saloon_name'), Survice_Name=F('service_id__description'),  Added_By=F('Added_by__role'))
                
            return Response({'status':True, 'data': data})       
        else:
            return Response({"status": False, "msg":"Unauthorized"})  

####################################################################################################################  
# EMPLOYEE-PUT/API
 
    def put(self, request):
        my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            requireFields = ['name','contact','image','saloon_id','service_id','Added_by']
            validator = uc.keyValidation(True,True,request.data,requireFields)

            if validator:
                return Response(validator,status = 200)   

            else:       
                uid = request.data.get('uid')       
                name = request.data.get("name")  
                contact = request.data.get("contact") 
                image = request.data.get("image")  
                service_id = request.data.get("service_id")  
                saloon_id = request.data.get("saloon_id")  
                Added_by = request.data.get("Added_by")  

                objservice = service.objects.filter(uid = service_id).first()
                objsaloon = saloon.objects.filter(uid = saloon_id).first()
                objAccount = Role.objects.filter(uid = Added_by).first()

                admin = employee.objects.filter(uid=uid).first()
                if admin:
                    admin.name=name
                    admin.contact=contact
                    admin.image=image
                    admin.service_id=objservice
                    admin.saloon_id=objsaloon
                    admin.Added_by=objAccount

                    admin.save()

                    return Response({'status': True, 'Msg': 'data Update Successfully'}) 
                    
                else:
                    return Response({"status": False, "msg":"invalid_Credentials"})
        else:
            return Response({"status": False, "msg":"Unauthorized"})    
####################################################################################################################################################
# EMPLOYEE-DELETE/API
    def delete(self,request):
        my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            requireField = ['uid']
            validator = uc.keyValidation(True,True,request.GET,requireField)
 
            if validator:
                return Response(validator,status = 200)   

            else:
                uid = request.GET['uid']
                data = employee.objects.filter(uid=uid).first()       
                if data:
                    data.delete()
                    
                    return Response({'status': True, 'Msg': 'data Delete Successfully'})
                else:
                    return Response({"status": False, "msg":"Invalid_Credentials"})
#     
        else:
            return Response({"status": False, "msg":"Unauthorized"})
# ==================================================================================================================================================
# EMPLOYEE-GETSPECIFIC/API
class dataget_employee(APIView):
      def get(self,request):
          my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
          if my_token:  
            requireFields = ['uid']
            validator = uc.keyValidation(True,True,request.GET,requireFields)
        
            if validator:
                return Response(validator,status = 200)
                
            else:
                uid = request.GET['uid']

            data = employee.objects.filter(uid=uid).values('name','contact', Saloon_Name=F('saloon_id__saloon_name'), Survice_Name=F('service_id__description'),  Added_By=F('Added_by__role')).first()       
        
            if data:                                                                                                     
                return Response({'status': True, 'Msg': 'data Get Successfully', 'data': data}) 
            else:
                return Response({"status": False, "msg":"Invalid_Credentials"})
          else:
            return Response({"status": False, "msg":"Unauthorized"})    
# show service and saloon

class Showsaloon(APIView):  
    def get(self, request):        
            
        ser = service.objects.all().values('uid' ,'service_name' , 'image')                
        # sal = saloon.objects.all().values('saloon_name','image', 'address')                        
        return Response({'status':True, 'Services': ser})


### get saloon data from service

class dataget_saloon(APIView):
      def get(self,request):
            uid = request.GET['uid']
            
            data = saloon.objects.filter(service_id__uid=uid).values('uid','saloon_name', 'image', 'address')       
            
            for i in range(len(data)):

                student_data = saloon_image.objects.filter(saloon_id = data[i]['uid']).values('image')

                if student_data:
                                                                    
                    imagelist = []
                    for j in range(len(student_data)):
                        
                        imagelist.append(student_data[j]['image'])
                        data[i]['saloon_image'] = imagelist
                else:
                    data[i]['Student'] =''

            return Response({"status":True,'data':data})

class Salon_Sub_detail(APIView):
   def get(self, request):
      uid = request.GET['uid']      
    
      data = category.objects.filter(saloon_id__uid=uid).values('uid','category_name')

      for i in range(len(data)):

        mydata = services_list.objects.filter(category_id__uid=data[i]['uid']).values('uid','name','before_time', 'price')

        if  data:         
              data[i]['Survice_Lists'] = mydata
              
        else:
            data[i]['Student'] =''

      return Response({"status":True,'data':data,})

class search (APIView):
   def get (self,request):
      
      categoryname = request.GET['categoryname']
      
      data = category.objects.filter(categoryname__icontains = categoryname).values('categoryname','price','before_time','service_type')

      return Response({"status":True,"data":data})

class addimages(APIView):
    def post(self, request):    
        image = request.data.getlist('image')
        saloon_name = request.data.get('saloon_name')
        saloon_id = request.data.get('saloon_id')
        address = request.data.get('address')

        objsaloon_id = saloon_image.objects.filter(uid = saloon_id).first()

        sliderObj = saloon(saloon_name = saloon_name , image = image , address = address)
        sliderObj.save()    

 
        for i in range(len(image)):
            
            imageObj = saloon_image(saloon_id = sliderObj,image =image[i])
            imageObj.save()

        return Response({"status":True,"message":"images Add successfully"})
           

class float_list_data(APIView):
   def get(self, request):
    uid = request.GET['uid']

    data = float_list.objects.filter(saloon_id__uid=uid).values('section_name')
    if  data:         
  
      return Response({"status":True,'Saloon_data':data,})
    else:
        return Response({"status":True,'Msg':'Invalid Id'})


class Reviews_Data(APIView):
   def get(self, request):
    uid = request.GET['uid']

    data = review.objects.filter(float_list_id__saloon_id__uid=uid).values('name','description','by_name','by_name','date_created')
    if  data:         
      return Response({"status":True,'Saloon_data':data,})
    else:
        return Response({"status":True,'Msg':'Invalid Id'})


class Portfolio_Data(APIView):
   def get(self, request):
    uid = request.GET['uid']

    data = portfolio.objects.filter(float_list_id__saloon_id__uid=uid).values('image')
    if  data:         
      return Response({"status":True,'Saloon_data':data,})
    else:
        return Response({"status":True,'Msg':'Invalid Id'})


class Detail_Data(APIView):
   def get(self, request):
      uid = request.GET['uid']      

      data = about_us.objects.filter(saloon_id__uid=uid).values('uid','heading','discription')
      main = employee.objects.filter(saloon_id__uid=uid).values('uid','heading','name','image')
      mydata = contact_buss_hour.objects.filter(saloon_id__uid=uid).values('uid','heading','discription','phone_no','monday','tuesday','wednesday','thursday','friday','saturday','sunday')
      userdata = social_media_share.objects.filter(saloon_id__uid=uid).values('uid','heading','icon_name','icon_img')
      youdata = venue_amenitie.objects.filter(saloon_id__uid=uid).values('uid','heading','venue')
      yourdata = travel_fee_policy.objects.filter(saloon_id__uid=uid).values('uid','heading','discription')
      yoursdata = pay_cancellation_policy.objects.filter(saloon_id__uid=uid).values('uid','heading','discription')
      admindata = report.objects.filter(saloon_id__uid=uid).values('uid','heading','discription','name')

    
      return Response({"status":True,'about us':data, 'staffers': main,'contact_bussines_hour':mydata,'social_media_shares':userdata,'venue_amenities':youdata,'travel_fees_policy':yourdata,
      'payment_cancellation_policy':yoursdata,'reports':admindata})


class health_safety_rules(APIView):
   def get(self, request):
    uid = request.GET['uid']

    data = health_safety_rule.objects.filter(saloon_id__uid=uid).values('name')
    if  data:        
      return Response({"status":True,'Saloon_data':data,})
    else:
        return Response({"status":True,'Msg':'Invalid Id'})
