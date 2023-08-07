import requests

class Georefar():
    def get_provincias(self):
        default_provincia = [('', '-- Seleccione provincia --')]

        url = 'https://apis.datos.gob.ar/georef/api/provincias?campos=nombre&orden=nombre'

        try:
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            provincias = data['provincias']
            lista_provincias = default_provincia + [(d['id'], d['nombre']) for d in provincias]
            return lista_provincias
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
            return None
        
    def get_localidades(self, provincia_id):
        default_localidad = [('', '-- Seleccione localidad --')]

        if not provincia_id:
            return default_localidad
        
        url = f'https://apis.datos.gob.ar/georef/api/localidades-censales?provincia={provincia_id}&campos=nombre&orden=nombre&max=5000'

        try:
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            localidades = data['localidades_censales']
            lista_localidades = default_localidad + [(d['id'], d['nombre']) for d in localidades]
            return lista_localidades
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
            return None
        

georefar = Georefar()