import requests
import sqlite3
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

# URL du sitemap
# A quoi sert ce commentaire ?
sitemap_url = "https://readi.fi/sitemap.xml"

# Connexion à la base SQLite
conn = sqlite3.connect("readi_assets.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS assets (
        url TEXT PRIMARY KEY,
        title TEXT,
        description TEXT
    )
''')
conn.commit()

# Récupérer et parser le sitemap
response = requests.get(sitemap_url)
if response.status_code == 200:
    root = ET.fromstring(response.content)
    asset_urls = [url.text for url in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc") if url.text.startswith("https://readi.fi/asset")]
    print(f"Nombre de liens trouvés : {len(asset_urls)}")

    # Parcourir chaque URL pour extraire le contenu
    for url in asset_urls:
        page = requests.get(url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            title = soup.title.string if soup.title else "No title"
            meta_desc = soup.find("meta", {"name": "description"})
            description = meta_desc["content"] if meta_desc else "No description"

            # Insertion dans la base de données
            cursor.execute('''
                INSERT OR REPLACE INTO assets (url, title, description) VALUES (?, ?, ?)
            ''', (url, title, description))
            print(f"Données insérées pour {url}")

# Enregistrer et fermer la connexion
conn.commit()
conn.close()

