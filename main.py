import requests
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Función genérica que escribe un archivo a partir de un texto
# Puede utilizarse para escribir un archivo HTML copia local
# de la página que vamos a leer
def escribirArchivo(texto, archivo):
    f = open(archivo, "w")
    f.write(texto)
    f.close()

def devolverSoup(url):
  resp = requests.get(url)
  # resp = urlopen(url).read().decode('utf-8')

  if resp.status_code == 200:
    # print(resp.encoding)
    # resp.encoding = 'utf-8'
    # print(resp.encoding)
    contenido = resp.content
    
    print(contenido)
    soup = BeautifulSoup(contenido, 'html.parser')        
    return soup

# Función genérica que crea un archivo JSON de nombre "nombre" y
# con los datos "datos"
def crearJSON(nombre, datos):
  result = {}
  result[nombre] = datos

  with open(nombre + ".json", "w") as write_file:
    json.dump(result, write_file, indent=2)

# Función específica a la página y la información que queremos
# extraer
def extraerProductos(soup):
  productos = soup.find_all('tr')
  result = []

  for producto in productos:
    objProducto = {}

    # Recuperamos el nombre del producto y el primer precio en COP
    nombre = producto.find('td', class_='product-name')
    precio = producto.find('td', class_='price')

    # Para no tratar el encabezado
    if None in (nombre, precio):
      continue
    
    objProducto['nombre'] = nombre.text.strip()
    precioAux = precio.text.strip().replace('$', '').replace(',', '.')
    objProducto['precio'] = float(precioAux)

    result.append(objProducto)

  return result


# Dada la URL, creamos un objeto soup que contiene la página
# Luego extraemos la información que necesitamos
# Finalemente creamos un archivo JSON con los datos extraidos
if __name__ == "__main__":

  url = "https://preciosmundi.com/colombia/precios-supermercado"

  soup = devolverSoup(url)
  productos = extraerProductos(soup)

  crearJSON("productos", productos)
 

