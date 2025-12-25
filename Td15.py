import sqlite3
# question 1 
def AccederBD(maBase):
    try:
        conn = sqlite3.connect(maBase)
        c = conn.cursor()
        return conn, c
    except sqlite3.Error as e:
        print(f"Erreur deconnexion: {e}")
        return None, None 

# question 2
def CreerTable1(c):
   
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS FILM (
                        idFilm INTEGER PRIMARY KEY,
                        titre TEXT NOT NULL,
                        realisateur TEXT,
                        annee INTEGER
                    )''')
        print("Table FILM créée avec succès")
    except sqlite3.Error as e:
        print(f"Erreur création table FILM: {e}")

# question 3
def CreerTable2(c):
   
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS ACTEUR (
                        idActeur INTEGER PRIMARY KEY,
                        nom TEXT NOT NULL,
                        prenom TEXT NOT NULL
                    )''')
        print("Table ACTEUR créée avec succès")
    except sqlite3.Error as e:
        print(f"Erreur création table ACTEUR: {e}")

# question 4
def CreerTable3(c):
    
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS FILMOGRAPHIE (
                        idActeur INTEGER,
                        idFilm INTEGER,
                        role TEXT,
                        salaire REAL,
                        PRIMARY KEY (idActeur, idFilm),
                        FOREIGN KEY (idActeur) REFERENCES ACTEUR(idActeur),
                        FOREIGN KEY (idFilm) REFERENCES FILM(idFilm)
                    )''')
        print("Table FILMOGRAPHIE créée avec succès")
    except sqlite3.Error as e:
        print(f"Erreur création table FILMOGRAPHIE: {e}")

# question 5
def rech_personne(c, nom, prenom):

    try:
        c.execute("SELECT * FROM ACTEUR WHERE nom=? AND prenom=?", (nom, prenom))
        result = c.fetchone()
        return result is not None
    except sqlite3.Error as e:
        print(f"Erreur recherche personne: {e}")
        return False

# question 6
def insert_acteur(c, id, nom, prenom):
    
    try:
        if rech_personne(c, nom, prenom):
            print(f"L'acteur {prenom} {nom} existe déjà dans la base")
            return False
        c.execute("INSERT INTO ACTEUR (idActeur, nom, prenom) VALUES (?, ?, ?)", 
                  (id, nom, prenom))
        print(f"Acteur {prenom} {nom} inséré avec succès")
        return True
    except sqlite3.Error as e:
        print(f"Erreur insertion acteur: {e}")
        return False

# question 7
def affiche_table(c, nomTable):
    try:
        c.execute(f"SELECT * FROM {nomTable}")
        rows = c.fetchall()
        colonnes = [description[0] for description in c.description]
        
        print(f"\n=== Contenu de la table {nomTable} ===")
        print(" | ".join(colonnes))
        print("-" * 50)
        
        for row in rows:
            print(" | ".join(str(val) for val in row))
        
        print(f"\nNombre total de lignes: {len(rows)}")
    except sqlite3.Error as e:
        print(f"Erreur affichage table: {e}")

# question 8
def affiche_film(c, id):
    try:
        c.execute("SELECT * FROM FILM WHERE idFilm=?", (id,))
        film = c.fetchone()
        
        if film:
            print(f"\n=== Détails du film ===")
            print(f"ID: {film[0]}")
            print(f"Titre: {film[1]}")
            print(f"Réalisateur: {film[2]}")
            print(f"Année: {film[3]}")
        else:
            print(f"Aucun film trouvé avec l'ID {id}")
    except sqlite3.Error as e:
        print(f"Erreur affichage film: {e}")

# question 9
def supr_film(c, id):
    try:
        # Supprimer d'abord les entrées dans FILMOGRAPHIE
        c.execute("DELETE FROM FILMOGRAPHIE WHERE idFilm=?", (id,))
        # Puis supprimer le film
        c.execute("DELETE FROM FILM WHERE idFilm=?", (id,))
        print(f"Film avec ID {id} supprimé avec succès")
    except sqlite3.Error as e:
        print(f"Erreur suppression film: {e}")

# question 10
def modif_FILMOGRAPHIE(c, id1, id2, val):
    try:
        c.execute("UPDATE FILMOGRAPHIE SET salaire=? WHERE idActeur=? AND idFilm=?", 
                  (val, id1, id2))
        if c.rowcount > 0:
            print(f"Salaire modifié avec succès")
        else:
            print("Aucune ligne modifiée - vérifiez les IDs")
    except sqlite3.Error as e:
        print(f"Erreur modification salaire: {e}")

# question 11
def Nbr_acteurs(c, nomFilm):
    try:
        c.execute("""SELECT COUNT(DISTINCT F.idActeur) 
                     FROM FILMOGRAPHIE F
                     JOIN FILM Fi ON F.idFilm = Fi.idFilm
                     WHERE Fi.titre = ?""", (nomFilm,))
        result = c.fetchone()
        return result[0] if result else 0
    except sqlite3.Error as e:
        print(f"Erreur comptage acteurs: {e}")
        return 0

# question 12
def ActeursSansFilms(c):
    try:
        c.execute("""SELECT nom, prenom 
                     FROM ACTEUR 
                     WHERE idActeur NOT IN (SELECT DISTINCT idActeur FROM FILMOGRAPHIE)""")
        acteurs = c.fetchall()
        
        print("\n=== Acteurs sans films ===")
        if acteurs:
            for acteur in acteurs:
                print(f"{acteur[1]} {acteur[0]}")
        else:
            print("Tous les acteurs ont joué dans au moins un film")
    except sqlite3.Error as e:
        print(f"Erreur recherche acteurs sans films: {e}")

# question 13
def ActeursDebutants(c):
    try:
        c.execute("""SELECT A.nom, A.prenom, AVG(F.salaire) as moyenne_salaire
                     FROM ACTEUR A
                     JOIN FILMOGRAPHIE F ON A.idActeur = F.idActeur
                     GROUP BY A.idActeur, A.nom, A.prenom
                     ORDER BY moyenne_salaire DESC""")
        acteurs = c.fetchall()
        
        print("\n=== Acteurs et leur salaire moyen ===")
        for acteur in acteurs:
            print(f"{acteur[1]} {acteur[0]}: ${acteur[2]:.2f}")
    except sqlite3.Error as e:
        print(f"Erreur recherche acteurs débutants: {e}")

# question 14
def ActeursMemeSalaire(c):
    try:
        c.execute("""SELECT DISTINCT A1.nom, A1.prenom, A2.nom, A2.prenom, F1.salaire
                     FROM FILMOGRAPHIE F1
                     JOIN FILMOGRAPHIE F2 ON F1.salaire = F2.salaire AND F1.idActeur < F2.idActeur
                     JOIN ACTEUR A1 ON F1.idActeur = A1.idActeur
                     JOIN ACTEUR A2 ON F2.idActeur = A2.idActeur
                     ORDER BY F1.salaire DESC""")
        paires = c.fetchall()
        
        print("\n=== Paires d'acteurs avec le même salaire ===")
        if paires:
            for paire in paires:
                print(f"{paire[1]} {paire[0]} et {paire[3]} {paire[2]}: ${paire[4]:.2f}")
        else:
            print("Aucune paire d'acteurs avec le même salaire")
    except sqlite3.Error as e:
        print(f"Erreur recherche paires acteurs: {e}")

# question 15
def SalaireDollarToDirham(c):
    try:
        c.execute("""SELECT A.nom, A.prenom, Fi.titre, F.salaire, F.salaire * 9 as salaire_dh
                     FROM FILMOGRAPHIE F
                     JOIN ACTEUR A ON F.idActeur = A.idActeur
                     JOIN FILM Fi ON F.idFilm = Fi.idFilm
                     ORDER BY salaire_dh DESC""")
        salaires = c.fetchall()
        
        print("\n=== Salaires en Dirhams ===")
        for sal in salaires:
            print(f"{sal[1]} {sal[0]} - {sal[2]}: ${sal[3]:.2f} = {sal[4]:.2f} DH")
    except sqlite3.Error as e:
        print(f"Erreur conversion salaires: {e}")

# question 16
def ValiderTrans(conn):
    try:
        conn.commit()
        print("Transactions validées avec succès")
    except sqlite3.Error as e:
        print(f"Erreur validation transactions: {e}")

# question 17
def TableToFile(Fich, c, nomTable):
    try:
        c.execute(f"SELECT * FROM {nomTable}")
        rows = c.fetchall()
        
        with open(Fich, 'w', encoding='utf-8') as f:
            for row in rows:
                ligne = '|'.join(str(val) for val in row)
                f.write(ligne + '\n')
        
        print(f"Table {nomTable} exportée vers {Fich} avec succès")
    except (sqlite3.Error, IOError) as e:
        print(f"Erreur export table vers fichier: {e}")

# question 18
def FileToTable(Fich, c, nomTable):
    try:
        with open(Fich, 'r', encoding='utf-8') as f:
            for ligne in f:
                valeurs = ligne.strip().split('|')
                placeholders = ','.join(['?'] * len(valeurs))
                c.execute(f"INSERT INTO {nomTable} VALUES ({placeholders})", valeurs)
        
        print(f"Fichier {Fich} importé dans {nomTable} avec succès")
    except (sqlite3.Error, IOError) as e:
        print(f"Erreur import fichier vers table: {e}")

# question 19
def FermerConnex(conn):
    try:
        if conn:
            conn.close()
            print("Connexion fermée avec succès")
    except sqlite3.Error as e:
        print(f"Erreur fermeture connexion: {e}")


# Exemple d'utilisation
if __name__ == "__main__":
    maBase = 'cinema.sqlite'
    
    # Connexion à la base
    conn, c = AccederBD(maBase)
    
    if conn and c:
        # Création des tables
        CreerTable1(c)
        CreerTable2(c)
        CreerTable3(c)
        
        # Validation
        ValiderTrans(conn)
        
        # Fermeture
        FermerConnex(conn)