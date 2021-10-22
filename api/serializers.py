from rest_framework import serializers

from .models import PackageRelease, Project
from .pypi import version_exists, latest_version


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageRelease
        fields = ["name", "version"]
        extra_kwargs = {"version": {"required": False}}

    def validate(self, data):

       

        new_data = data.items()

        name = [{name[0]:name[1]} for name in new_data if name[0] == 'name'][0]
        version = [{version[0]:version[1]} for version in new_data if version[0] == 'version'][0]
      
        import json
        import requests
        query = name['name']

        request = requests.get(f'https://pypi.org/pypi/{query}/json')

        if request.status_code == 404 :
            raise serializers.ValidationError()

        response = json.loads(request.content)

        if  version['version'] in response['releases']:
            
            return data

        raise serializers.ValidationError()
  
        
       









        # TODO
        # Validar o pacote, checar se ele existe na versão especificada.
        # Buscar a última versão caso ela não seja especificada pelo usuário.
        # Subir a exceção `serializers.ValidationError()` se o pacote não
        # for válido.
        return data


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "packages"]

    packages = PackageSerializer(many=True)

    def create(self, validated_data):
        # TODO
        # Salvar o projeto e seus pacotes associados.
        #
        # Algumas referência para uso de models do Django:
        # - https://docs.djangoproject.com/en/3.2/topics/db/models/
        # - https://www.django-rest-framework.org/api-guide/serializers/#saving-instances
        packages = validated_data["packages"]
        return Project(name=validated_data["name"])
