
# Proyecto Desarrollo de Sistemas IV
Integrantes: Adriana Sanchez, Marco Quintanar y Samara Acosta

Este proyecto está dividido en tres partes, que permiten construir un sistema completo para consultar revistas académicas clasificadas por área, catálogo y más. Usa Python, Web Scraping, y una interfaz web con Flask + Bootstrap.

# Parte 1 (Archivos CSV y JSON)

Esta parte del proyecto permite procesar y leer archivos CSV para así generar un diccionario estructurado con títulos de revistas.

# Funcionalidades del programa

- Lee todos los archivos CSV del directorio datos/csv/areas y datos/csv/catalogos.

- Construye un diccionario donde cada llave es el título de una revista, y el valor es un subdiccionario con:
   - Las áreas a las que pertenece (ej. CIENCIAS_EXA, INGENIERÍA)
   - Los catálogos en los que aparece (ej. JCR, SCOPUS)

- El resultado se guarda como un archivo JSON llamado revistas.json dentro del directorio datos/json.

- Si el archivo ya existe, no se sobrescribirá.

- El JSON resultante puede ser leído y reutilizado por las siguientes partes del proyecto (scraper y sitio web).

# Instrucciones para ejecutar

1. Se puede ejecutar directamente con el archivo parte1.py o ejecutar "python parte1.py" 

2. Asegurar que se encuentra dentro de la carpeta proyectoDS4

3. Seguido de eso se le mostrará el mensaje "JSON cargado exitosamente."

4. Finalmente en la carpeta de datos/json estará "revistas.json" si es que no se ha generado anteriomente.

# Herramientas de asistencia
Para esta primera parte, se utilizó la asistencia de ChatGPT y de trabajos anteriores en clase.


# Parte 2 (scrapper)

# SCImago Journal Scraper

Esta parte del proyecto consiste en un scraper en python que permite extraer información sobre revistas que se encuentra en el sitio "SCImago Journal Rank (SJR)" que se puede encontrar visitando este enlace https://www.scimagojr.com/. El programa recibe un archivo JSON con nombres de revistas, y guarda en un nuevo archivo JSON la información obtenida de cada una de ellas.

# Funcionalidades del programa

- Carga nombres de revistas desde un archivo JSON.
- Busca automáticamente cada revista en SCImago.
- Extrae los siguientes datos:
  - Sitio web oficial de la revista
  - H-Index
  - Área temática
  - Editorial
  - ISSN
  - Widget (imágen)
  - Tipo de publicación
  - Fecha de última visita
- Guarda los resultados en un archivo JSON limpio y estructurado.
- Permite ejecutar scraping por rangos para poder pararelizar el trabajo ya que eran mas de 42,000 revistas y hacerlo solo podria tardar hasta 36 horas.

# Estructura del Proyecto

- app.py: programa principal para extraer información de revistas desde scimago
- scimago_scrapper.py: Funciones de scrapper para SCImago

# Instrucciones para hacer funcionar el programa

1. Preparar un archivo JSON de entrada.
   Este archivo debe ser un diccionario donde cada clave es el nombre de una revista, por ejemplo:

   
   {
     "Nature": {},
     "Science": {},
     "Lancet": {}
   }


2. Ejecuta el scraper desde línea de comandos:

   ```
   python app.py -a <ruta/archivo_entrada.json> -p <indice_inicio> -u <indice_fin> -o <archivo_salida.json>
   ```

   - -a: ruta al archivo JSON de entrada con los nombres de las revistas.
   - -p: índice inicial para empezar el scraping.
   - -u: índice final. El scraping se detiene antes de este índice.
   - -o: ruta al archivo donde se guardarán los resultados en formato JSON.

3. Ejemplo:


   python app.py -a ../datos/json/revistas.json -p 0 -u 50 -o ../datos/json/revistas_info.json

   Esto procesará las primeras 50 revistas del archivo y guardará la información en revistas_info.json.

# Requisitos

Instalar las dependencias:

- requests
- beautifulsoup4
- unidecode

¿Como instalarlas?

pip install requests
pip install beautifulsoup4
pip install unidecode


# Herramientas de asistencia

Durante el desarrollo de este scrapper, se utilizó ChatGPT como asistente para mejorar un poco la flexibilidad del programa.

**Normalización de caracteres especiales**

ChatGPT recomendó emplear la librería unidecode para convertir títulos de revistas con acentos, diéresis u otros signos diacríticos en su equivalente ASCII. Esto asegura que las URL y las búsquedas en SCImago no fallen por diferencias en codificación.

**Parámetros por línea de comandos**

Para permitir la ejecución en paralelo y con distintos rangos de datos, ChatGPT sugirió utilizar el módulo estándar argparse. Esto fue de mucha ayuda pues nos permitió correr el codigo de manera paralela con los demas integrantes del equipo haciendo que el tiempo que se empleó en la busqueda de revistas sea mucho menor.

# Parte 3 (Página Web)

Esta parte del proyecto proporciona una interfaz web interactiva para consultar las revistas almacenadas en el JSON generado por el scraper. Asimismo toma imagen de un Repositorio de Revistas Académico

# Funcionalidades de la página web

- Inicio: Página de bienvenida 
- Áreas: Muestra todas las áreas disponibles. Al hacer click en una, se desplegará una tabla con las revistas y su H-Index
- Catálogos: Navegación por catálogo
- Explorar 

# Estructura del Proyecto

- app.py: Archivo principal que lanza el servidor web con Flask. Contiene las rutas y vistas para cada sección del sitio.

- funciones.py: Archivo donde contiene todas las funcionalidades principales del programa (página web).

- static:  Carpeta que contiene los archivos estáticos como estilos y logos.
   - css/estilos.css:  estilos personalizados utilizando los colores institucionales de la Universidad de Sonora.
   - img: imagenes utilizadas

- templates: Carpeta que contiene las plantillas HTML utilizadas por Flask. Incluye:
   - area_detalle.html
   - area.html
   - base.html
   - busqueda.html
   - catalogo_detalle.html
   - catalogos.html
   - creditos.html
   - explora.html
   - explorar.html
   - index.html
   - login.html
   - revista.html

# Instrucciones para hacer funcionar el programa

1. Se ingresa a la carpeta "app" con "cd app" en la terminal

2. Ejecuta el servidor Flask con "python app.py". A la par procurar que la carpeta datos se encuentre dentro de app

3. En la terminal se reflejará el navegador parecido a "http://127.0.0.1:5000/"

4. Ingresar a esa dirección URL para abrir la página web

# Requisitos

Instalar las dependencias:

- flask

¿Como instalarlas?

pip install flask

# Herramientas de asistencia
Para el desarrollo de esta última parte del proyecto, se utilizó el apoyo de ChatGPT como de DeepSeek para cuidar cada detalle de la página web.
