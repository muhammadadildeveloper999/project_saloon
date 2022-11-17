from django.urls import path,include
from Api.views import *

urlpatterns = [

#web urls  home
path('categoryAdd',categoryAdd.as_view())
]