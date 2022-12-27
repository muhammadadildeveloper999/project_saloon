from rest_framework import serializers
from .models import*

class UserSaloonSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = category
        fields = ['uid','category_name']




class UserSerializer(serializers.ModelSerializer):

    category_id = UserSaloonSerializer(many=False, read_only=True)

    class Meta:
        model = services_list
        fields = ['category_id','uid','category_name','service_type']