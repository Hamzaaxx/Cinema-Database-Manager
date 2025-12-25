# 🎬 Cinema Database Manager

Système de gestion de base de données pour films et acteurs avec interface Streamlit.

## ✨ Fonctionnalités

- 📊 Dashboard avec statistiques et graphiques
- 🎬 Gestion complète des films
- 👥 Gestion des acteurs et filmographie
- 💰 Conversion Dollar → Dirham (1$ = 9 DH)
- 📈 Statistiques avancées
- 📥 Import/Export CSV

## 🚀 Installation
```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

## 🗄️ Base de Données

- **FILM** : idFilm, titre, realisateur, annee
- **ACTEUR** : idActeur, nom, prenom
- **FILMOGRAPHIE** : idActeur, idFilm, role, salaire

## 🛠️ Technologies

- Python 3.8+
- Streamlit
- SQLite3
- Pandas
- Plotly

## 👨‍🎓 Auteur

Projet universitaire - TD Base de Données
```

#### **2. Créez `requirements.txt`**
```
streamlit==1.28.0
pandas==2.0.3
plotly==5.17.0
```

#### **3. Renommez votre fichier**
- Renommez `test_sqlite.py` → `dashboard.py`

#### **4. Créez `cinema_functions.py`**
Copiez le premier code que je vous ai donné avec toutes les fonctions (AccederBD, CreerTable1, etc.)

---

### 🌟 **Étape 2 : Créer un compte GitHub**

1. Allez sur **https://github.com/signup**
2. Entrez votre email
3. Créez un mot de passe
4. Choisissez un username (exemple: `hamza-dev`)
5. Vérifiez votre email

---

### 📦 **Étape 3 : Créer le Repository**

1. **Connectez-vous** à GitHub

2. Cliquez sur le **bouton vert "New"** en haut à gauche (ou allez sur https://github.com/new)

3. **Remplissez le formulaire** :
   - **Repository name** : `cinema-database-manager`
   - **Description** : `Système de gestion de base de données cinéma avec Streamlit - Projet TD`
   - **Public** : ✅ (pour que votre prof puisse voir)
   - **Add a README** : ❌ (on va l'ajouter nous-même)
   - **Add .gitignore** : Sélectionnez **"Python"**
   - **Choose a license** : Aucune (laissez "None")

4. Cliquez sur **"Create repository"**

---

### 📤 **Étape 4 : Uploader vos fichiers**

Vous allez maintenant voir une page avec plusieurs options.

#### **Option 1 : Upload via interface (RECOMMANDÉ)**

1. Cliquez sur **"uploading an existing file"** (lien en bleu au milieu de la page)

2. **Glissez-déposez** tous vos fichiers :
   - `dashboard.py`
   - `cinema_functions.py`
   - `README.md`
   - `requirements.txt`
   - (Ne mettez PAS `cinema.sqlite` - la base sera créée automatiquement)

3. En bas de la page, dans **"Commit changes"** :
   - Message : `Initial commit - Cinema Database Manager`
   - Description : `Ajout de tous les fichiers du projet`

4. Cliquez sur **"Commit changes"**

---

### ✅ **Étape 5 : Vérifier que tout est en ligne**

Vous devriez maintenant voir votre projet avec :
- ✅ `dashboard.py`
- ✅ `cinema_functions.py`
- ✅ `README.md`
- ✅ `requirements.txt`
- ✅ `.gitignore`

Le README s'affichera automatiquement en bas de la page !

---

### 🔗 **Étape 6 : Obtenir le lien**

1. Copiez l'URL dans la barre d'adresse
2. Elle ressemblera à : `https://github.com/VOTRE_USERNAME/cinema-database-manager`

---

### 📧 **Étape 7 : Email à votre professeur**
```
Objet : Soumission Projet TD 15 - Base de Données Cinéma

Bonjour Professeur,

Je vous soumets mon projet de gestion de base de données cinéma.

🔗 Lien GitHub : https://github.com/VOTRE_USERNAME/cinema-database-manager

Le projet comprend :
✅ 19 fonctions de gestion de base de données (cinema_functions.py)
✅ Interface web Streamlit (dashboard.py)
✅ Dashboard avec statistiques et graphiques
✅ Gestion CRUD complète (Films, Acteurs, Filmographie)
✅ Export/Import CSV
✅ Conversion Dollar → Dirham

Pour tester :
1. pip install -r requirements.txt
2. streamlit run dashboard.py

Cordialement,
Hamza
