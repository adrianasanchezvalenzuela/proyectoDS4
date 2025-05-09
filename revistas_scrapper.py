'''
Scrapper de revistas
'''
import requests
from bs4 import BeautifulSoup

try:
    from bs4 import BeautifulSoup
    import requests

    # Hacemos una petición sencilla a una página web
    url = 'https://example.com'
    response = requests.get(url, timeout=10)

    # Usamos BeautifulSoup para analizar el HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    titulo = soup.find('h1').text.strip()

    print("✅ BeautifulSoup está funcionando correctamente.")
    print(f"Título de la página: {titulo}")

except ImportError as e:
    print("❌ BeautifulSoup NO está instalado.")
    print(e)

except Exception as e:
    print("⚠️ Ocurrió un error al probar BeautifulSoup.")
    print(e)
