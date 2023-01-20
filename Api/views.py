from django.shortcuts import render
import datetime
from datetime import datetime, timedelta
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

# User_Account/API

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

# # User-LOGIN/API


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
                              'exp': datetime.utcnow() + timedelta(days=22),
                            #   'iat': datetime.datetime.utcnow(),

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
                              'exp': datetime.utcnow() + timedelta(days=22),
                            #   'iat': datetime.datetime.utcnow(),

                          }


                        access_token = jwt.encode(access_token_payload,config('superadminkey'),algorithm = 'HS256')
                        data = {'uid':fetchAccount.uid,'firstname':fetchAccount.firstname,'lastname':fetchAccount.lastname,'contact':fetchAccount.contact, 'email':fetchAccount.email, 'Login_As':str(fetchAccount.role_id)}

                        whitelistToken(token = access_token, user_agent = request.META['HTTP_USER_AGENT'],created_at = datetime.now(), role_id=fetchAccount).save()


                        return Response({"status":True,"message":"Login Successlly","token":access_token,"superadmindata":data})


                     if fetchAccount.role_id.role == 'manager':
                            access_token_payload = {
                            'id':str(fetchAccount.uid),
                            'firstname':fetchAccount.firstname,
                            'email':fetchAccount.email,
                            'exp': datetime.utcnow() + timedelta(days=22),
                            #  'iat': datetime.datetime.utcnow(),

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
                              'exp': datetime.utcnow() + timedelta(days=22),
                            #   'iat': datetime.datetime.utcnow(),

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

# show category

class Showsaloon(APIView):
    def get(self, request):

        cat = service.objects.all().values('uid' ,'service_name' , 'image')

        return Response({'status':True, 'category': cat})

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

### get multiple service from saloon

class Salon_Sub_detail(APIView):
  def get(self, request):
      uid = request.GET['uid']

      data = category.objects.filter(saloon_id__uid=uid).values('uid','category_name')

      for i in range(len(data)):

        mydata = services_list.objects.filter(category_id__uid=data[i]['uid']).values('uid','name','before_time', 'price', 'service_type')

        if  data:
              data[i]['Survice_Lists'] = mydata

        else:
            data[i]['Student'] =''

      return Response({"status":True,'data':data,})

# Search Services

class search (APIView):
  def get (self,request):

      category_name = request.GET['category_name']

      data = service.objects.filter(category_name__icontains = category_name).values('category_name','price','before_time','service_type')

      return Response({"status":True,"data":data})

# Add multiple Images For Saloon

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

# Add float_list For Saloon Sections

class float_list_data(APIView):
  def get(self, request):
    uid = request.GET['uid']

    data = float_list.objects.filter(saloon_id__uid=uid).values('section_name')
    if  data:

      return Response({"status":True,'Saloon_data':data,})
    else:
        return Response({"status":True,'Msg':'Invalid Id'})

# Add Review for Saloon Section

class Reviews_Data(APIView):
  def get(self, request):
    uid = request.GET['uid']

    data = review.objects.filter(saloon_id__uid=uid).values('comment','star','date_created',
    ServiceName=F('Service_Name__name'), Saloon_Name=F('saloon_id__saloon_name'), by_name=F('Account_id__firstname'))
    if  data:
      return Response({"status":True,'Comments_data':data,})
    else:
        return Response({"status":True,'Msg':'Invalid Id'})

# Add Comments for Saloon Review Section

class commits(APIView):
    def post(self, request):
            requireFields = ['comment','star', 'Account_id', 'Service_Name']
            validator = uc.keyValidation(True ,True,request.data,requireFields)
            if validator:
                return Response(validator,status = 200)
            else:
                my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
                if my_token:

                    comment  = request.data.get('comment')
                    star  = request.data.get('star')
                    Service_Name  = request.data.get('Service_Name')
                    Account_id  = request.data.get('Account_id')
                    float_id  = request.data.get('float_id')
                    saloon_id  = request.data.get('saloon_id')

                    service_obj= services_list.objects.filter(name = Service_Name).first()

                    salon_obj= saloon.objects.filter(saloon_name = saloon_id).first()

                    admin= Account.objects.filter(email=Account_id).first()

                    if admin:
                        user= review.objects.filter(Account_id__email=Account_id).first()
                        if user:
                          return Response({"status":False, "message":"Cannot Post More Than One Comment !"})
                        else:
                            data = review(comment=comment, star=star, date_created = datetime.now(), Account_id=admin, Service_Name=service_obj,saloon_id=salon_obj)

                            data.save()
                            return Response ({"status":True,"message":"Comment Successfully Add"})
                    else:
                        return Response ({"status":False,"message":"Please Signup Here"})
                else:
                    return Response({"status": False, "msg":"Unauthorized"})

# Add Porfolio Images for Saloon Porfolio Section

class Portfolio_Data(APIView):
  def get(self, request):
    uid = request.GET['uid']

    data = portfolio.objects.filter(float_list_id__saloon_id__uid=uid).values('image')
    if  data:
      return Response({"status":True,'Saloon_data':data,})
    else:
        return Response({"status":True,'Msg':'Invalid Id'})

# Add Saloon Detail for Saloon Detail Section

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


      return Response({"status":True,'about us':data,'contact_bussines_hour':mydata,'social_media_shares':userdata,'venue_amenities':youdata,'travel_fees_policy':yourdata,
      'payment_cancellation_policy':yoursdata,'reports':admindata})

# Add Saloon Health Safety Rule for Saloon Health Section

class health_safety_rules(APIView):
  def get(self, request):
    uid = request.GET['uid']

    data = health_safety_rule.objects.filter(saloon_id__uid=uid).values('name')
    if  data:
      return Response({"status":True,'Saloon_data':data,})
    else:
        return Response({"status":True,'Msg':'Invalid Id'})

# Add Employee_Name for Saloon Booking Section
class employe_name(APIView):
  def get(self, request):
    uid = request.GET['uid']

    data = employee_name.objects.filter(saloon_id__uid=uid).values('employee_name','employee_image')
    if  data:
      return Response({"status":True,'Empolyee_Name':data})
    else:
        return Response({"status":True,'Msg':'Invalid Id'})

# Add Employee_Slot for Saloon Booking Section

class employee_timing_slot(APIView):
    def get(self, request):
        uid = request.GET['uid']
        starttime = request.query_params.get('starttime')
        endtime = request.query_params.get('endtime')
        try:
            mydata = employee_timing.objects.filter(employee_name_id__uid=uid).values('starttime','endtime') 
        except employee_timing.DoesNotExist:
            return Response({"status":False,'Msg':'Saloon Id not found'})
        
        starttime = datetime.combine(datetime.now(), mydata[0]["starttime"])
        endtime = datetime.combine(datetime.now(), mydata[0]["endtime"])
        print(mydata[0]["starttime"])
        print(mydata[0]["starttime"])

        intervals = []
        current_time = starttime
        while current_time <= endtime:
            intervals.append(current_time)
            current_time += timedelta(minutes=30)
         
        if  mydata:
            return Response({"status":True ,'Employee_Timing':intervals})
        list index out of range
        slove this error        

# ADMINSIDE ADMINSIDE ADMINSIDE ADMINSIDE ADMINSIDE ADMINSIDE ADMINSIDE  ADMINSIDEADMINSIDE ADMINSIDE ADMINSIDE ADMINSIDE ADMINSIDE ADMINSIDE ADMINSIDEADMINSIDE

# ADMIN SITE CODE

# Role_Account/API

class Register_Admin(APIView):
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

# SuperAdmin Login

class SuperAdminLogin(APIView):
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
                    if fetchAccount.role_id.role == 'superadmin':
                        access_token_payload = {
                              'id':str(fetchAccount.uid),
                              'firstname':fetchAccount.firstname,
                              'exp': datetime.utcnow() + timedelta(days=22),
                            #   'iat': datetime.datetime.utcnow(),
                          }

                        access_token = jwt.encode(access_token_payload,config('superadminkey'),algorithm = 'HS256')
                        data = {'uid':fetchAccount.uid,'firstname':fetchAccount.firstname,'lastname':fetchAccount.lastname,'contact':fetchAccount.contact,'email':fetchAccount.email, 'Login_As':str(fetchAccount.role_id)}

                        whitelistToken(token = access_token, user_agent = request.META['HTTP_USER_AGENT'],created_at = datetime.now(), role_id=fetchAccount).save()

                        return Response({"status":True,"message":"Login Successlly","token":access_token,"admindata":data})
                    else:
                        return Response({"status":False,"message":"Unable to login"})
                  else:
                     return Response({"status":False,"message":"Invalid Creadientialsl"})
              else:
                  return Response({"status":False,"message":"Unable to login"})

# send_mail Api

class Otp_send(APIView):
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

class verify_otp(APIView):
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


# SALOON-POST/API

class Salons(APIView):
    def post(self, request):
        my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            requireFields = ['saloon_name','address','service_name', 'image']
            validator = uc.keyValidation(True,True,request.data,requireFields)

            if validator:
                return Response(validator,status = 200)

            else:
                image = request.data.getlist('image')
                saloon_name = request.data.get('saloon_name')
                saloon_id = request.data.get('saloon_id')
                address = request.data.get('address')
                service_id = request.data.get('service_id')

                objsaloon_id = saloon_image.objects.filter(uid = saloon_id).first()
                objservice = service_id.objects.filter(service_name = service_id).first()

                sliderObj = saloon(saloon_name = saloon_name ,  address = address, service_id=objservice)
                sliderObj.save()


                for i in range(len(image)):

                    imageObj = saloon_image(saloon_id = sliderObj,image =image[i])
                    imageObj.save()

                return Response({"status":True,"message":"images Add successfully"})
        else:
            return Response({"status": False, "msg":"Unauthorized"})

# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# SALOON-GET/API

    def get(self,request):
        my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            data = saloon.objects.all().values('uid','saloon_name','address', Service_Name=F('service_id__service_name'))
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
        else:
            return Response({"status": False, "msg":"Unauthorized"})


####################################################################################################################
# SALOON-PUT/API

    def put(self, request):
        my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            requireFields = ['uid','saloon_name','address','service_id']
            validator = uc.keyValidation(True,True,request.data,requireFields)

            if validator:
                return Response(validator,status = 200)

            else:
                uid = request.data.get('uid')
                saloon_name = request.data.get("saloon_name")
                address = request.data.get("address")
                service_id = request.data.get("service_id")

                objchecked = service.objects.filter(service_name = service_id).first()

                admin = saloon.objects.filter(uid=uid).first()
                if admin:
                    admin.saloon_name=saloon_name
                    admin.address=address
                    admin.category_id=objchecked

                    admin.save()

                    return Response({'status': True, 'Msg': 'data Update Successfully'})

                else:
                    return Response({"status": False, "msg":"invalid_Credentials"})
        else:
            return Response({"status": False, "msg":"Unauthorized"})

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
            uid = request.GET['uid']

            data = saloon.objects.filter(service_id__uid=uid).values('uid','saloon_name','address')

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


# SURVICE-POST/API

class Services(APIView):
    def post(self, request):
        my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            
            combinedata = eval(request.data.get('combinedata'))
            saloon_id  = request.data.get('saloon_id')
            saloon_obj = saloon.objects.filter(saloon_name=saloon_id).first()
            for i in range(len(combinedata)):

                data = category(category_name = combinedata[i]['category_name'], saloon_id=saloon_obj)

                data.save()

            return Response ({"status":True,"message":"Successfully Add"})
        else:
            return Response({"status": False, "msg":"Unauthorized"})           

# SURVICE-PUT/API

    def put(self, request):
        my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            requireFields = ['uid', 'category_name','saloon_id']
            validator = uc.keyValidation(True,True,request.data,requireFields)

            if validator:
                return Response(validator,status = 200)

            else:
                uid = request.data.get('uid')
                category_name = request.data.get("category_name")
                saloon_id = request.data.get("saloon_id")

                obj_saloon = saloon.objects.filter(saloon_name=saloon_id).first()

                admin = category.objects.filter(uid=uid).first()
                if admin:
                    admin.category_name=category_name
                    admin.saloon_id=obj_saloon

                    admin.save()

                    return Response({'status': True, 'Msg': 'data Update Successfully'})

                else:
                    return Response({"status": False, "msg":"invalid_Credentials"})
        else:
            return Response({"status": False, "msg":"Unauthorized"})

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
                data = category.objects.filter(uid=uid).first()
                if data:
                    data.delete()

                    return Response({'status': True, 'Msg': 'data Delete Successfully'})
                else:
                    return Response({"status": False, "msg":"Invalid_Credentials"})
#
        else:
            return Response({"status": False, "msg":"Unauthorized"})


# SURVICE_LIST-POST/API

class Survices_List(APIView):
    def post(self, request):
           
        my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:

            combinedata = eval(request.data.get('combinedata'))
            category_id  = request.data.get('category_id')
            
            cat_obj = category.objects.filter(category_name=category_id).first()
            for i in range(len(combinedata)):

                data = services_list(name = combinedata[i]['name'], before_time = combinedata[i]['before_time'],price = combinedata[i]['price']
                ,service_type = combinedata[i]['service_type'], category_id=cat_obj)

                data.save()

            return Response ({"status":True,"message":"Successfully Add"})
        else:
            return Response({"status": False, "msg":"Unauthorized"})
        
# service_list-get/API

    def get(self, request):
        saloon_name = request.GET['saloon_name']

        data = category.objects.filter(saloon_id__saloon_name=saloon_name).values('uid','category_name')

        for i in range(len(data)):

            mydata = services_list.objects.filter(category_id__uid=data[i]['uid']).values('uid','name','before_time', 'price','name', 'service_type')

            if  data:
                data[i]['Survice_Lists'] = mydata

            else:
                data[i]['Student'] =''

        return Response({"status":True,'data':data,})


# SURVICE-PUT/API

    def put(self, request):
        requireFields = ['name','before_time','service_type','price','category_id']
        validator = uc.keyValidation(True ,True,request.data,requireFields)

        if validator:
            return Response(validator,status = 200)

        else:
            my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:

                uid = request.data.get('uid')
                name = request.data.get("name")
                before_time = request.data.get("before_time")
                service_type = request.data.get("service_type")
                price = request.data.get("price")
                category_id = request.data.get("category_id")

                service_obj = category.objects.filter(category_name=category_id).first() 

                admin = services_list.objects.filter(uid=uid).first()
                if admin:
                    admin.name=name
                    admin.before_time=before_time
                    admin.service_type=service_type
                    admin.price=price
                    admin.category_id=service_obj

                    admin.save()

                    return Response({'status': True, 'Msg': 'data Update Successfully'})

                else:
                    return Response({"status": False, "msg":"invalid_Credentials"})
            else:
                return Response({"status": False, "msg":"Unauthorized"})

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
                data = services_list.objects.filter(uid=uid).first()
                if data:
                    data.delete()

                    return Response({'status': True, 'Msg': 'data Delete Successfully'})
                else:
                    return Response({"status": False, "msg":"Invalid_Credentials"})
#
        else:
            return Response({"status": False, "msg":"Unauthorized"})
# ==================================================================================================================================================
# float list crud

# Float_list-get/API

class Float_list_data(APIView):
  def get(self, request):
    saloon_name = request.GET['saloon_name']

    data = float_list.objects.filter(saloon_id__saloon_name=saloon_name).values('uid','section_name', Saloon_Name=F('saloon_id__saloon_name'))
    if  data:

      return Response({"status":True,'Saloon_data':data,})
    else:
        return Response({"status":True,'Msg':'Invalid Id'})

# Float_list-post/API

  def post (self, request):
      combinedata = eval(request.data.get('combinedata'))
      saloon_id  = request.data.get('saloon_id')
      section_name  = request.data.get('section_name')

      salon_id = saloon.objects.filter(saloon_name=saloon_id).first()

      for i in range(len(combinedata)):


        data = float_list(section_name = combinedata[i]['section_name'],saloon_id=salon_id)
        data.save()
        return Response ({"status":True,"message":"Sections successfully Add"})

# Float_list-update/API

  def put(self, request):
        my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            requireFields = ['section_name','saloon_id','uid']
            validator = uc.keyValidation(True,True,request.data,requireFields)

            if validator:
                return Response(validator,status = 200)

            else:
                uid = request.data.get('uid')
                section_name = request.data.get("section_name")
                saloon_id = request.data.get("saloon_id")


                obj_salon = saloon.objects.filter(saloon_name = saloon_id).first()

                admin = float_list.objects.filter(uid=uid).first()
                if admin:
                    admin.section_name=section_name
                    admin.saloon_id=obj_salon

                    admin.save()

                    return Response({'status': True, 'Msg': 'data Update Successfully'})

                else:
                    return Response({"status": False, "msg":"invalid_Credentials"})
        else:
            return Response({"status": False, "msg":"Unauthorized"})

# Float_list-delete/API

  def delete(self,request):
        my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            requireField = ['uid']
            validator = uc.keyValidation(True,True,request.GET,requireField)

            if validator:
                return Response(validator,status = 200)

            else:
                uid = request.GET['uid']
                data = float_list.objects.filter(uid=uid).first()
                if data:
                    data.delete()

                    return Response({'status': True, 'Msg': 'data Delete Successfully'})
                else:
                    return Response({"status": False, "msg":"Invalid_Credentials"})
        else:
            return Response({"status": False, "msg":"Unauthorized"})


# SERVICE CRUD

# service-get/API

class Float_list_data(APIView):
  def get(self, request):
    uid = request.GET['uid']

    data = float_list.objects.filter(saloon_id__uid=uid).values('section_name')
    if  data:

      return Response({"status":True,'Saloon_data':data,})
    else:
        return Response({"status":True,'Msg':'Invalid Id'})
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# service-post/API

  def post (self, request):
      combinedata = eval(request.data.get('combinedata'))
      saloon_id  = request.data.get('saloon_id')
      section_name  = request.data.get('section_name')

      salon_id = saloon.objects.filter(saloon_name=saloon_id).first()

      for i in range(len(combinedata)):


        data = float_list(section_name = combinedata[i]['section_name'],saloon_id=salon_id)
        data.save()
        return Response ({"status":True,"message":"Sections successfully Add"})

# service-update/API

  def put(self, request):
        my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            requireFields = ['section_name','saloon_id','uid']
            validator = uc.keyValidation(True,True,request.data,requireFields)

            if validator:
                return Response(validator,status = 200)

            else:
                uid = request.data.get('uid')
                section_name = request.data.get("section_name")
                saloon_id = request.data.get("saloon_id")


                obj_salon = saloon.objects.filter(saloon_name = saloon_id).first()

                admin = float_list.objects.filter(uid=uid).first()
                if admin:
                    admin.section_name=section_name
                    admin.saloon_id=obj_salon

                    admin.save()

                    return Response({'status': True, 'Msg': 'data Update Successfully'})

                else:
                    return Response({"status": False, "msg":"invalid_Credentials"})
        else:
            return Response({"status": False, "msg":"Unauthorized"})

# service-delete/API

  def delete(self,request):
        my_token = uc.superadmin(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            requireField = ['uid']
            validator = uc.keyValidation(True,True,request.GET,requireField)

            if validator:
                return Response(validator,status = 200)

            else:
                uid = request.GET['uid']
                data = float_list.objects.filter(uid=uid).first()
                if data:
                    data.delete()

                    return Response({'status': True, 'Msg': 'data Delete Successfully'})
                else:
                    return Response({"status": False, "msg":"Invalid_Credentials"})
        else:
            return Response({"status": False, "msg":"Unauthorized"})


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

############################### #####################################################################################
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
#####################################################################################################################################################
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

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------