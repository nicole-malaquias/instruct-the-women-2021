from rest_framework import serializers
import json
import requests
from .models import PackageRelease, Project
from .pypi import version_exists, latest_version
from collections import OrderedDict

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageRelease
        fields = ["name", "version"]
        extra_kwargs = {"version": {"required": False}}

    def validate(self,data):

        # try :

        new_data = data.items()

        arr = [{item[0]:item[1]}for item in new_data]

        name_tech = arr[0]['name']
    
        if len(arr) == 1 :
        
            last = latest_version(name_tech)

            if not last :
                raise serializers.ValidationError()

            response = {"name":name_tech, "version":last}
        
            return response

        version = arr[1]['version']
        
        is_exists = version_exists(name_tech,version)
    
        if is_exists == True:

            response = {"name":name_tech, "version":version}
            return response
           
   
        return serializers.ValidationError()


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "packages"]

    packages = PackageSerializer(many=True)

    def create(self, validated_data):
       
        try :

            lib_name = validated_data["packages"][0]['name']
            lib_version = validated_data["packages"][0]['version']
         
            projeto = Project.objects.create(name=validated_data["name"])
    
            package = PackageRelease.objects.create(name=lib_name,version=lib_version,project=projeto)
        
            return validated_data

        except :
            return {"erro":"não deu certo"}

