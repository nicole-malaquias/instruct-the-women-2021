from rest_framework import serializers
import json
import requests
from .models import PackageRelease, Project
from .pypi import version_exists, latest_version


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageRelease
        fields = ["name", "version"]
        extra_kwargs = {"version": {"required": False}}

    def validate(self,data ):

        new_data = data.items()
      
        if (len(new_data)) > 1 : 
          
            name = [{name[0]:name[1]} for name in new_data if name[0] == 'name'][0]
            
            version = [{version[0]:version[1]} for version in new_data if version[0] == 'version'][0]

            name_tech = name['name']

            request = requests.get(f'https://pypi.org/pypi/{name_tech}/json')

            if request.status_code == 404 :
                raise serializers.ValidationError()

            response = json.loads(request.content)

            if  version['version'] in response['releases']:
                return data

            else :
                raise serializers.ValidationError()

        else :

            name = [{name[0]:name[1]} for name in new_data if name[0] == 'name'][0]
                
            name_tech = name['name']

            request = requests.get(f'https://pypi.org/pypi/{name_tech}/json')
        
            response = json.loads(request.content)

            last_version = response['info']['version']

            from collections import OrderedDict

            response = OrderedDict()
            response['name'] = name['name']
            response['version'] =  last_version
              
            return response



class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "packages"]

    packages = PackageSerializer(many=True)

    def create(self, validated_data):
        # TODO
        
        lib = PackageRelease( validated_data["packages"])
        projeto = Project(validated_data['name'])

        
        # Salvar o projeto e seus pacotes associados.
        #
        # Algumas referência para uso de models do Django:
        # - https://docs.djangoproject.com/en/3.2/topics/db/models/
        # - https://www.django-rest-framework.org/api-guide/serializers/#saving-instances
        packages = validated_data["packages"]
        return Project(name=validated_data["name"])
