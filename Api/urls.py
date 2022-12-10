from django.urls import path,include
from Api.views import *

urlpatterns = [

#web urls  home
path('login',login.as_view()),
path('Register',Register.as_view()),
path('roles',roles.as_view()),
path('dataget_saloon',dataget_saloon.as_view()),
path('datagets',datagets.as_view()),
path('Salons',Salons.as_view()),
path('Survices',Survices.as_view()),
path('dataget_survice',dataget_survice.as_view()),
path('Employees',Employees.as_view()),
path('Otp_sending',Otp_sending.as_view()),
path('verify_otpcode',verify_otpcode.as_view()),
path('Showsaloon',Showsaloon.as_view()),
path('dataget_saloon',dataget_saloon.as_view()),
path('service_detail_saloon',service_detail_saloon.as_view()),
path('Stu_Class_Get',Stu_Class_Get.as_view()),

]
