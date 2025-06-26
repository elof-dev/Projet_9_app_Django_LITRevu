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
git clone https://github.com/elof-dev/Projet_9_app_Django_LITRevu
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

5. **Lancer le serveur** (la base de données avec données de test est incluse)
```bash
python manage.py runserver
```

6. **Accéder à l'application**
   - Ouvrir http://127.0.0.1:8000 dans votre navigateur
   - **Comptes de démonstration disponibles :**
     - Utilisateur :
        - `admin` / `mdp@admin123` (superutilisateur)
        - `sarahj` / `mdp@admin123` (admin abonné à sarahj mais pas l'inverse)
        - `jean_5679` / `mdp@admin123` (admin et jean_5679 se suivent)

## Utilisation principale

1. **S'inscrire** ou se connecter
2. **Demander une critique** en début de feed pour publier un ticket auquel les autres utilisateurs pourront donner leur avis (créer une critique)
3. **Créer une critique** en début de feed pour publier un ticket et une critique en même temps
4. **Créer une critique** dans le feed, en réponse à une demande de critique (à un ticket) d'un autre utilisateur
5. **Modifier ou supprimer ses posts** dans l'onglet posts
6. **Gérer ses abonnements** et bloquer certains utilisateurs si besoin

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
├── db.sqlite3        # Base de données (avec données de test)
├── manage.py         # Script Django
└── requirements.txt  # Dépendances
```

## Technologies Utilisées

- **Django 5.2.3**
- **SQLite**
- **Pillow**
- **Tailwind CSS**

