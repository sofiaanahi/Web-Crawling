import requests
from bs4 import BeautifulSoup
import json


# URL del sitio web
url = 'https://wv5n.cuevana.biz/'

def Extraer_datos_web(url):
    # Creo una lista vacia para almacenar tos los datos 
    datos = {}

    # Realizo una  solicitud GET a la URL 
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Parsear el contenido HTML usando BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar todas las etiquetas <a> con sus enlaces
        enlaces = soup.find_all('a')

        # Recorrer cada enlace encontrado
        for link in enlaces:
            # Obtener la URL del enlace
            link_url = link.get('href')

            # Verifico si la URL es válida
            if link_url.startswith('http'):
                # Realizar una nueva solicitud GET a la URL del enlace 
                link_response = requests.get(link_url)

                # Verificar si la solicitud fue exitosa
                if link_response.status_code == 200:
                    # Parsear el contenido HTML del enlace
                    link_soup = BeautifulSoup(link_response.text, 'html.parser')

                    # Encontrar todas las etiquetas <h1> y <p> en el contenido del enlace
                    etiqueta_h1 = link_soup.find_all('h1')
                    etiqueta_p = link_soup.find_all('p')

                    # Almacenar los elementos encontrados en un diccionario
                    link_almacenar_datos = {
                        'h1': [h1.text.strip() for h1 in etiqueta_h1],
                        'p': [p.text.strip() for p in etiqueta_p]
                    }

                    # Agregar los datos al diccionario principal usando la URL del enlace como clave
                    datos[link_url] = link_almacenar_datos

    return datos


# Llamar a la función para rastrear el sitio web y obtener los datos
resultado = Extraer_datos_web(url)

# Guardar los datos en un archivo JSON
with open('datos_recolectados.json', 'w') as json_file:
    json.dump(resultado, json_file, indent=4)

print("Los datos se han almacenado correctamente en 'Información_extraída.json'")
