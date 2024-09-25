# FastAPI PostgreSQL Manga Project with Docker

Ce projet est une API RESTful construite avec **FastAPI**, utilisant **PostgreSQL** pour la gestion d'une collection de mangas. L'application est orchestrée avec **Docker Compose** et inclut également **PgAdmin** pour une gestion simplifiée de la base de données.

## Table des Matières

- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Endpoints](#endpoints)
- [PgAdmin](#pgadmin)
- [Remarques](#remarques)
- [Auteurs](#auteurs)
- [License](#license)

## Fonctionnalités

- CRUD (Créer, Lire, Mettre à jour, Supprimer) pour les mangas
- Gestion de la base de données avec PostgreSQL
- Interface de gestion de base de données avec PgAdmin
- Documentation interactive de l'API avec Swagger UI

## Prérequis

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Installation

1. Clonez ce dépôt sur votre machine :

   ```bash
   git clone https://github.com/yourusername/fastapi-postgres-manga.git
   cd fastapi-postgres-manga
   ```

2. Construisez et lancez les conteneurs Docker :
    ```bash
    docker-compose up --build
    ```
    Cela va démarrer les services suivants :

    - PostgreSQL (db)
    - FastAPI (app)
    - PgAdmin (pgadmin)

## Configuration
Assurez-vous de vérifier et de modifier les paramètres de connexion à la base de données dans le fichier Dockerfile et dans le code FastAPI si nécessaire.

- POSTGRES_USER : Nom d'utilisateur de la base de données.
- POSTGRES_PASSWORD : Mot de passe de la base de données.
- POSTGRES_DB : Nom de la base de données à créer.
Ces paramètres sont définis dans le fichier docker-compose.yml.

## Utilisation
Lancez l'application FastAPI et accédez à l'API à l'adresse suivante : http://localhost:8000.

Accédez à la documentation interactive de l'API à l'adresse suivante : http://localhost:8000/docs.

Pour accéder à PgAdmin, allez à l'adresse suivante : http://localhost:5050 avec les identifiants :

- Email : admin@admin.com
- Mot de passe : admin

Endpoints
- GET /mangas : Récupérer la liste de tous les mangas.
- GET /mangas/{manga_id} : Récupérer un manga spécifique par ID.
- POST /mangas : Ajouter un nouveau manga.
- PUT /mangas/{manga_id} : Mettre à jour un manga existant par ID.
- DELETE /mangas/{manga_id} : Supprimer un manga par ID.

## Exemple de requête
### Ajouter un nouveau manga
```json
POST /mangas
{
    "title": "My Manga Title",
    "author": "Author Name",
    "published_year": 2021,
    "genre": "Action"
}
```

## PgAdmin
PgAdmin est utilisé pour gérer la base de données PostgreSQL. Après vous être connecté avec les identifiants par défaut, vous pouvez ajouter un nouveau serveur avec les détails suivants :

- Nom : PostgreSQL
- Hôte : db (c'est le nom du service défini dans docker-compose.yml)
- Port : 5432
- Nom d'utilisateur : postgres
- Mot de passe : postgres

## Remarques
- Assurez-vous que Docker et Docker Compose sont correctement installés et fonctionnent sur votre machine.

- Pour arrêter les conteneurs, utilisez Ctrl + C dans le terminal où vous avez exécuté docker-compose up. Pour les arrêter en arrière-plan, utilisez :

```bash
docker-compose down
```