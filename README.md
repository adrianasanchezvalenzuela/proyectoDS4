
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

1. **Preparar un archivo JSON de entrada.**
   Este archivo debe ser un diccionario donde cada clave es el nombre de una revista, por ejemplo:

   
   {
     "Nature": {},
     "Science": {},
     "Lancet": {}
   }


2. **Ejecuta el scraper desde línea de comandos:**

   ```
   python app.py -a <ruta/archivo_entrada.json> -p <indice_inicio> -u <indice_fin> -o <archivo_salida.json>
   ```

   - -a: ruta al archivo JSON de entrada con los nombres de las revistas.
   - -p: índice inicial para empezar el scraping.
   - -u: índice final. El scraping se detiene antes de este índice.
   - -o: ruta al archivo donde se guardarán los resultados en formato JSON.

3. **Ejemplo:**


   python app.py -a datos/json/revistas.json -p 0 -u 50 -o datos/json/revistas_info.json

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

Durante el desarrollo de este scrapper, utilicé ChatGPT como asistente para mejorar un poco la flexibilidad del programa.

**Normalización de caracteres especiales**

ChatGPT recomendó emplear la librería unidecode para convertir títulos de revistas con acentos, diéresis u otros signos diacríticos en su equivalente ASCII. Esto asegura que las URL y las búsquedas en SCImago no fallen por diferencias en codificación.

**Parámetros por línea de comandos**

Para permitir la ejecución en paralelo y con distintos rangos de datos, ChatGPT sugirió utilizar el módulo estándar argparse. Esto fue de mucha ayuda pues nos permitió correr el codigo de manera paralela con los demas integrantes del equipo haciendo que el tiempo que se empleó en la busqueda de revistas sea mucho menor.
