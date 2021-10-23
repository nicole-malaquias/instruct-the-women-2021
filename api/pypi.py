import requests
import json

# Referências sobre o uso do requests:
#
# Fazendo requisições:
# https://docs.python-requests.org/en/master/user/quickstart/#make-a-request
# Usando JSON retornado:
# https://docs.python-requests.org/en/master/user/quickstart/#json-response-content

def version_exists(package_name, version):
    
    request = requests.get(f'https://pypi.org/pypi/{package_name}/json')
    response = json.loads(request.content)

    if  version in response['releases']:
        return True

    return False


def latest_version(package_name):
 
    request = requests.get(f'https://pypi.org/pypi/{package_name}/json')
    if request.status_code == 404 :
        return None

    response = json.loads(request.content)
    last_version = response['info']['version']

    latest_version  = list(releases.keys())[-1]
    
    return latest_version
