from django.urls import path,include
from Api.views import *

urlpatterns = [

# ADMIN-SITE-URLS

path('superadminLogin',SuperAdminLogin.as_view()),
path('Register_Admin',Register_Admin.as_view()),
path('Otp_send',Otp_send.as_view()),
path('verify_otp',verify_otp.as_view()),
path('Salons',Salons.as_view()),
path('dataget_saloon',dataget_saloon.as_view()),
path('Services',Services.as_view()),
path('Survices_List',Survices_List.as_view()),
path('Float_list_data',Float_list_data.as_view()),
path('Employees',Employees.as_view()),

# USER-SITE-URL

path('login',login.as_view()),
path('Register',Register.as_view()),
path('Otp_sending',Otp_sending.as_view()),
path('verify_otpcode',verify_otpcode.as_view()),
path('Showsaloon',Showsaloon.as_view()),
path('dataget_saloon',dataget_saloon.as_view()),
path('Salon_Sub_detail',Salon_Sub_detail.as_view()),
path('search',search.as_view()),
path('addimages',addimages.as_view()),
path('float_list_data',float_list_data.as_view()),
path('Reviews_Data',Reviews_Data.as_view()),
path('Portfolio_Data',Portfolio_Data.as_view()),
path('Detail_Data',Detail_Data.as_view()),
path('health_safety_rules',health_safety_rules.as_view()),
path('commits',commits.as_view()),
path('employe_name',employe_name.as_view()),
path('employee_timing_slot',employee_timing_slot.as_view()),


]
