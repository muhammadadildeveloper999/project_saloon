from django.shortcuts import render
import datetime
import jwt
from decouple import config
from django.conf import settings
from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import render
from passlib.hash import django_pbkdf2_sha256 as handler
from rest_framework.response import Response
from rest_framework.views import APIView
import Api.usable as uc
from .models import *                                  

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

# User_Register/API

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
         
            if uc.checkemailforamt(email):
               if not uc.passwordLengthValidator(password):
                  return Response({"status":False, "message":"password should not be than 8 or greater than 20"})

               checkemail=register.objects.filter(email=email).first()
               if checkemail:
                  return Response({"status":False, "message":"Email already exists"})

  
               data = register(firstname = firstname, lastname = lastname, email=email, password=handler.hash(password), contact=contact)
              
               data.save()

               return Response({"status":True,"message":"Account Created Successfully"})
            else:
               return Response({"status":False,"message":"Email Format Is Incorrect"})

# Role_Register/API

class Register_role(APIView):
   def post (self,request):
        requireFields = ['firstname','lastname','email','password','contact', 'role_id']
        validator = uc.keyValidation(True,True,request.data,requireFields)
               
        if validator:
            return Response(validator,status = 200)
               
        else:
            my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                firstname = request.data.get('firstname')
                lastname = request.data.get('lastname')
                email = request.data.get('email')
                password = request.data.get('password')
                contact = request.data.get('contact')
                role_id = request.data.get('role_id')
            
                if uc.checkemailforamt(email):
                    if not uc.passwordLengthValidator(password):
                        return Response({"status":False, "message":"password should not be than 8 or greater than 20"})

                    checkemail=register.objects.filter(email=email).first()
                    if checkemail:
                        return Response({"status":False, "message":"Email already exists"})

                    checkSuper_Admin_Id = register.objects.filter(uid = role_id).first()

                    data = register(firstname = firstname, lastname = lastname, email=email, password=handler.hash(password), contact=contact,  role_id=checkSuper_Admin_Id)
                    
                    data.save()

                    return Response({"status":True,"message":"Account Created Successfully"})
                else:
                    return Response({"status":False,"message":"Email Format Is Incorrect"})
            else:
                return Response({"status":False,"message":"Unauthorized"})

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
               fetchAccount = register.objects.filter(email=email).first()
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
                    
                     if fetchAccount.role_id.role  == 'custumer':
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
                    objregister = Role.objects.filter(uid = Added_by).first()

                    data = service(description=description,price=price, saloon_id=objsaloon, Added_by=objregister)
                
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
                objregister = Role.objects.filter(uid = Added_by).first()

                admin = service.objects.filter(uid=uid).first()
                if admin:
                    admin.description=description
                    admin.price=price
                    admin.saloon_id=objsaloon
                    admin.Added_by=objregister

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

            data = service.objects.filter(uid=uid).values('description','price', Saloon_Name=F('saloon_id__saloon_name'), Registerator_User=F('Added_by__role')).first()       
        
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
                objregister = Role.objects.filter(uid = Added_by).first()

                admin = employee.objects.filter(uid=uid).first()
                if admin:
                    admin.name=name
                    admin.contact=contact
                    admin.image=image
                    admin.service_id=objservice
                    admin.saloon_id=objsaloon
                    admin.Added_by=objregister

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
