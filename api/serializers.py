from rest_framework import serializers

import json
import requests
from .models import PackageRelease, Project
from .pypi import version_exists, latest_version
from collections import OrderedDict
from django.core.exceptions import ValidationError 
from rest_framework import status
class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageRelease
        fields = ["name", "version"]
        extra_kwargs = {"version": {"required": False}}

    def validate(self,data):

        
        new_data = data.items()

        arr = [{item[0]:item[1]}for item in new_data]

        name_tech = arr[0]['name']
        
        if len(arr) == 1 :
        
            last = latest_version(name_tech)
            
            if  last == None :
                
                raise serializers.ValidationError({"error": "One or more packages doesn't exist"})

            response = {"name":name_tech, "version":last}
        
            return response

        version = arr[1]['version']
       
        is_exists = version_exists(name_tech,version)
      
        if is_exists == True:
            response = {"name":name_tech, "version":version}
            return response

        raise serializers.ValidationError({"error": "One or more packages doesn't exist"})
       
        
     

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "packages"]

    packages = PackageSerializer(many=True)

    def create(self, validated_data):

        arr_packages = []

        for item in validated_data['packages'] :

            is_exist = False

            for i in arr_packages :

                if i['name'] == item['name'] :
                    is_exist = True
            
            if not is_exist :
                arr_packages.append(item)

        projeto = Project.objects.create(name=validated_data["name"])

        for lib in arr_packages :
        
            PackageRelease.objects.create(name=lib['name'],version=lib['version'],project=projeto)

        del validated_data['packages']
        validated_data['packages'] = arr_packages

        return validated_data

