# LITRevu - Application de Critiques Littéraires

LITRevu est une application web Django permettant aux utilisateurs de demander et publier des critiques de livres et d'articles.

## Fonctionnalités

L'application se présente sous format fil d'actualité dans lequel se trouve les critiques et demandes d'avis d'autres utilisateurs auxquels ont peut répondre.
Un onglet posts permet de gérer nos publications.
Un onglet abonnements permet de suivre / rechercher / bloquer des abonnés.

## Prérequis

- Python 3.13
- pip


## Installation

1. **Cloner le projet**
```bash
git clone <https://github.com/elof-dev/Projet_9_app_Django_LITRevu>
cd Projet_9_app_Django_LITRevu
```

2. **Créer un environnement virtuel**
```bash
python -m venv .venv
```

3. **Activer l'environnement virtuel**
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

4. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

5. **Appliquer les migrations**
```bash
python manage.py migrate
```

6. **Créer un superutilisateur** (optionnel)
```bash
python manage.py createsuperuser
```

7. **Lancer le serveur**
```bash
python manage.py runserver
```

8. **Accéder à l'application**
   - Ouvrir http://127.0.0.1:8000 dans votre navigateur

## Utilisation

1. **S'inscrire** ou se connecter
2. **Créer des tickets** pour demander des critiques
3. **Publier des critiques** sur les tickets des autres ou sur ses propres tickets
4. **S'abonner** à des utilisateurs pour voir leurs publications
5. **Gérer ses abonnements** et bloquer si besoin

## Structure du Projet

```
LITRevu/
├── LITRevu/           # Configuration Django
├── reviews/           # Application principale
│   ├── models.py     # Modèles (Ticket, Review, UserFollows)
│   ├── views.py      # Vues
│   ├── forms.py      # Formulaires
│   ├── urls.py       # URLs de l'app
│   └── templates/    # Templates HTML
├── media/            # Fichiers uploadés
├── db.sqlite3        # Base de données
├── manage.py         # Script Django
└── requirements.txt  # Dépendances
```

## Technologies Utilisées

- **Django 5.2.3**
- **SQLite**
- **Pillow**
- **Tailwind CSS**

