Le script scrappy.py accomplit les tâches suivantes :

Se connecte à une base de données SQLite nommée readi_assets.db.
Crée une table assets (si elle n'existe pas déjà) pour stocker des URL, des titres et des descriptions.
Récupère et parse un sitemap XML à partir de l'URL https://readi.fi/sitemap.xml.
Parcourt chaque URL d'asset trouvée dans le sitemap, extrait le titre et la description de la page correspondante.
Insère ou met à jour les données extraites dans la base de données SQLite.
