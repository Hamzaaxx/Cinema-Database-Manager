import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="Cinema Database Manager",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fonctions de base de données
def AccederBD(maBase):
    """Établit une connexion avec la base de données"""
    try:
        conn = sqlite3.connect(maBase)
        c = conn.cursor()
        return conn, c
    except sqlite3.Error as e:
        st.error(f"Erreur de connexion: {e}")
        return None, None

def CreerTables(c):
    """Crée toutes les tables nécessaires"""
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS FILM (
                        idFilm INTEGER PRIMARY KEY,
                        titre TEXT NOT NULL,
                        realisateur TEXT,
                        annee INTEGER
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS ACTEUR (
                        idActeur INTEGER PRIMARY KEY,
                        nom TEXT NOT NULL,
                        prenom TEXT NOT NULL
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS FILMOGRAPHIE (
                        idActeur INTEGER,
                        idFilm INTEGER,
                        role TEXT,
                        salaire REAL,
                        PRIMARY KEY (idActeur, idFilm),
                        FOREIGN KEY (idActeur) REFERENCES ACTEUR(idActeur),
                        FOREIGN KEY (idFilm) REFERENCES FILM(idFilm)
                    )''')
        return True
    except sqlite3.Error as e:
        st.error(f"Erreur création tables: {e}")
        return False

def initialiser_donnees(conn, c):
    """Initialise la base avec des données exemple"""
    try:
        c.execute("SELECT COUNT(*) FROM FILM")
        if c.fetchone()[0] > 0:
            return
        
        films = [
            (1, "Inception", "Christopher Nolan", 2010),
            (2, "The Dark Knight", "Christopher Nolan", 2008),
            (3, "Interstellar", "Christopher Nolan", 2014),
            (4, "Casablanca", "Yacine Fennane", 2023),
            (5, "Le Méchoui du Roi", "Hicham Lasri", 2022),
            (6, "Much Loved", "Nabil Ayouch", 2015)
        ]
        c.executemany("INSERT OR IGNORE INTO FILM VALUES (?, ?, ?, ?)", films)
        
        acteurs = [
            (1, "DiCaprio", "Leonardo"),
            (2, "Bale", "Christian"),
            (3, "Hathaway", "Anne"),
            (4, "Caine", "Michael"),
            (5, "El Hasnaoui", "Said"),
            (6, "Talbi", "Abdelilah"),
            (7, "Loubna", "Abidar"),
            (8, "Hardy", "Tom")
        ]
        c.executemany("INSERT OR IGNORE INTO ACTEUR VALUES (?, ?, ?)", acteurs)
        
        filmographie = [
            (1, 1, "Dom Cobb", 20000000),
            (3, 1, "Ariadne", 5000000),
            (2, 2, "Batman", 15000000),
            (4, 2, "Alfred", 3000000),
            (1, 3, "Cooper", 25000000),
            (3, 3, "Brand", 8000000),
            (4, 3, "Professeur Brand", 4000000),
            (5, 4, "Hassan", 500000),
            (6, 5, "Omar", 500000),
            (7, 6, "Noha", 300000),
            (8, 2, "Bane", 10000000)
        ]
        c.executemany("INSERT OR IGNORE INTO FILMOGRAPHIE VALUES (?, ?, ?, ?)", filmographie)
        
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Erreur initialisation: {e}")

# CSS Simple et Épuré
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #f5f7fa;
    }
    
    .main {
        padding: 2rem;
    }
    
    h1, h2, h3 {
        color: #1e293b;
        font-weight: 600;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #3b82f6;
    }
    
    /* Boutons */
    .stButton > button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #2563eb;
        box-shadow: 0 4px 6px rgba(59, 130, 246, 0.2);
    }
    
    /* Inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1rem;
        background-color: #f8fafc;
        color: #64748b;
        border: 1px solid #e2e8f0;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f1f5f9;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #3b82f6;
        color: white;
        border-color: #3b82f6;
    }
    
    /* Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    /* DataFrames */
    .stDataFrame {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background-color: #10b981;
        color: white;
        border-radius: 8px;
    }
    
    .stDownloadButton > button:hover {
        background-color: #059669;
    }
    </style>
""", unsafe_allow_html=True)

# Connexion à la base de données
maBase = 'cinema.sqlite'
conn, c = AccederBD(maBase)

if conn and c:
    CreerTables(c)
    initialiser_donnees(conn, c)
    
    # Sidebar
    with st.sidebar:
        st.title("🎬 Cinema DB")
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["Dashboard", "Films", "Acteurs", "Filmographie", "Ajouter", "Statistiques", "Gestion"]
        )
        
        st.markdown("---")
        st.caption("Database: cinema.sqlite")
    
    # PAGE DASHBOARD
    if page == "Dashboard":
        st.title("📊 Dashboard")
        
        # Métriques
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            c.execute("SELECT COUNT(*) FROM FILM")
            st.metric("Films", c.fetchone()[0])
        
        with col2:
            c.execute("SELECT COUNT(*) FROM ACTEUR")
            st.metric("Acteurs", c.fetchone()[0])
        
        with col3:
            c.execute("SELECT AVG(salaire) FROM FILMOGRAPHIE")
            avg_sal = c.fetchone()[0]
            st.metric("Salaire Moyen", f"${avg_sal/1000000:.1f}M" if avg_sal else "$0")
        
        with col4:
            c.execute("SELECT COUNT(*) FROM FILMOGRAPHIE")
            st.metric("Rôles", c.fetchone()[0])
        
        st.markdown("---")
        
        # Graphiques
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Films par Réalisateur")
            df_real = pd.read_sql_query("""
                SELECT realisateur, COUNT(*) as nombre
                FROM FILM
                GROUP BY realisateur
                ORDER BY nombre DESC
            """, conn)
            fig = px.bar(df_real, x='realisateur', y='nombre', color_discrete_sequence=['#3b82f6'])
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis_title="",
                yaxis_title="Nombre de films"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Top 5 Acteurs - Revenus")
            df_top = pd.read_sql_query("""
                SELECT A.prenom || ' ' || A.nom as acteur, SUM(F.salaire) as total
                FROM ACTEUR A
                JOIN FILMOGRAPHIE F ON A.idActeur = F.idActeur
                GROUP BY A.idActeur
                ORDER BY total DESC
                LIMIT 5
            """, conn)
            fig = px.pie(df_top, values='total', names='acteur', 
                        color_discrete_sequence=px.colors.sequential.Blues)
            fig.update_layout(paper_bgcolor='white')
            st.plotly_chart(fig, use_container_width=True)
        
        # Tableau récapitulatif
        st.subheader("Derniers Films Ajoutés")
        df_recent = pd.read_sql_query("""
            SELECT titre, realisateur, annee 
            FROM FILM 
            ORDER BY annee DESC 
            LIMIT 5
        """, conn)
        st.dataframe(df_recent, use_container_width=True, hide_index=True)
    
    # PAGE FILMS
    elif page == "Films":
        st.title("🎬 Gestion des Films")
        
        tab1, tab2, tab3, tab4 = st.tabs(["Liste", "Rechercher", "Ajouter", "Supprimer"])
        
        with tab1:
            df_films = pd.read_sql_query("SELECT * FROM FILM ORDER BY annee DESC", conn)
            st.dataframe(df_films, use_container_width=True, height=400, hide_index=True)
            
            csv = df_films.to_csv(index=False).encode('utf-8')
            st.download_button("Télécharger CSV", csv, "films.csv", "text/csv")
        
        with tab2:
            col1, col2 = st.columns([3, 1])
            with col1:
                film_id = st.number_input("ID du film", min_value=1, step=1)
            with col2:
                search_btn = st.button("Rechercher", use_container_width=True)
            
            if search_btn:
                film = pd.read_sql_query(f"SELECT * FROM FILM WHERE idFilm={film_id}", conn)
                if not film.empty:
                    st.success("Film trouvé")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Titre:**", film['titre'].values[0])
                        st.write("**Réalisateur:**", film['realisateur'].values[0])
                    with col2:
                        st.write("**Année:**", film['annee'].values[0])
                        st.write("**ID:**", film['idFilm'].values[0])
                    
                    st.subheader("Distribution")
                    df_cast = pd.read_sql_query(f"""
                        SELECT A.prenom || ' ' || A.nom as Acteur, F.role as Rôle, F.salaire as Salaire
                        FROM ACTEUR A
                        JOIN FILMOGRAPHIE F ON A.idActeur = F.idActeur
                        WHERE F.idFilm = {film_id}
                    """, conn)
                    st.dataframe(df_cast, use_container_width=True, hide_index=True)
                else:
                    st.error("Film non trouvé")
        
        with tab3:
            with st.form("add_film"):
                col1, col2 = st.columns(2)
                with col1:
                    new_id = st.number_input("ID", min_value=1, step=1)
                    new_titre = st.text_input("Titre")
                with col2:
                    new_real = st.text_input("Réalisateur")
                    new_annee = st.number_input("Année", min_value=1900, max_value=2030, value=2024)
                
                if st.form_submit_button("Ajouter Film"):
                    try:
                        c.execute("INSERT INTO FILM VALUES (?, ?, ?, ?)", 
                                (new_id, new_titre, new_real, new_annee))
                        conn.commit()
                        st.success("Film ajouté avec succès!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erreur: {e}")
        
        with tab4:
            col1, col2 = st.columns([3, 1])
            with col1:
                del_id = st.number_input("ID du film à supprimer", min_value=1, step=1)
            with col2:
                if st.button("Supprimer", use_container_width=True, type="primary"):
                    try:
                        c.execute("DELETE FROM FILMOGRAPHIE WHERE idFilm=?", (del_id,))
                        c.execute("DELETE FROM FILM WHERE idFilm=?", (del_id,))
                        conn.commit()
                        st.success(f"Film supprimé")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erreur: {e}")
    
    # PAGE ACTEURS
    elif page == "Acteurs":
        st.title("👥 Gestion des Acteurs")
        
        tab1, tab2, tab3 = st.tabs(["Liste", "Filmographie", "Ajouter"])
        
        with tab1:
            df_acteurs = pd.read_sql_query("SELECT * FROM ACTEUR ORDER BY nom", conn)
            st.dataframe(df_acteurs, use_container_width=True, height=400, hide_index=True)
            
            st.subheader("Acteurs sans films")
            df_sans = pd.read_sql_query("""
                SELECT * FROM ACTEUR 
                WHERE idActeur NOT IN (SELECT DISTINCT idActeur FROM FILMOGRAPHIE)
            """, conn)
            if not df_sans.empty:
                st.dataframe(df_sans, use_container_width=True, hide_index=True)
            else:
                st.info("Tous les acteurs ont des films")
        
        with tab2:
            col1, col2 = st.columns([3, 1])
            with col1:
                acteur_id = st.number_input("ID de l'acteur", min_value=1, step=1)
            with col2:
                if st.button("Voir filmographie", use_container_width=True):
                    df_filmo = pd.read_sql_query(f"""
                        SELECT F.titre as Film, Fi.role as Rôle, Fi.salaire as Salaire, F.annee as Année
                        FROM FILM F
                        JOIN FILMOGRAPHIE Fi ON F.idFilm = Fi.idFilm
                        WHERE Fi.idActeur = {acteur_id}
                        ORDER BY F.annee DESC
                    """, conn)
                    if not df_filmo.empty:
                        st.dataframe(df_filmo, use_container_width=True, hide_index=True)
                        total = df_filmo['Salaire'].sum()
                        st.metric("Total des gains", f"${total:,.0f}")
                    else:
                        st.warning("Aucun film trouvé")
        
        with tab3:
            with st.form("add_acteur"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    new_id_act = st.number_input("ID", min_value=1, step=1)
                with col2:
                    new_nom = st.text_input("Nom")
                with col3:
                    new_prenom = st.text_input("Prénom")
                
                if st.form_submit_button("Ajouter Acteur"):
                    try:
                        c.execute("SELECT * FROM ACTEUR WHERE nom=? AND prenom=?", (new_nom, new_prenom))
                        if c.fetchone():
                            st.warning("Acteur déjà existant")
                        else:
                            c.execute("INSERT INTO ACTEUR VALUES (?, ?, ?)", 
                                    (new_id_act, new_nom, new_prenom))
                            conn.commit()
                            st.success("Acteur ajouté!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Erreur: {e}")
    
    # PAGE FILMOGRAPHIE
    elif page == "Filmographie":
        st.title("💰 Filmographie")
        
        df_full = pd.read_sql_query("""
            SELECT A.prenom || ' ' || A.nom as Acteur,
                   F.titre as Film,
                   Fi.role as Rôle,
                   Fi.salaire as 'Salaire ($)',
                   Fi.salaire * 9 as 'Salaire (DH)'
            FROM FILMOGRAPHIE Fi
            JOIN ACTEUR A ON Fi.idActeur = A.idActeur
            JOIN FILM F ON Fi.idFilm = F.idFilm
            ORDER BY Fi.salaire DESC
        """, conn)
        
        st.dataframe(df_full, use_container_width=True, height=400, hide_index=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribution des Salaires")
            fig = px.histogram(df_full, x='Salaire ($)', nbins=15, color_discrete_sequence=['#3b82f6'])
            fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Acteurs - Même Salaire")
            df_meme = pd.read_sql_query("""
                SELECT DISTINCT A1.prenom || ' ' || A1.nom as Acteur1,
                       A2.prenom || ' ' || A2.nom as Acteur2,
                       F1.salaire as Salaire
                FROM FILMOGRAPHIE F1
                JOIN FILMOGRAPHIE F2 ON F1.salaire = F2.salaire AND F1.idActeur < F2.idActeur
                JOIN ACTEUR A1 ON F1.idActeur = A1.idActeur
                JOIN ACTEUR A2 ON F2.idActeur = A2.idActeur
            """, conn)
            if not df_meme.empty:
                st.dataframe(df_meme, use_container_width=True, hide_index=True)
            else:
                st.info("Aucune paire trouvée")
    
    # PAGE AJOUTER
    elif page == "Ajouter":
        st.title("➕ Ajouter un Rôle")
        
        with st.form("add_role"):
            col1, col2 = st.columns(2)
            with col1:
                id_act = st.number_input("ID Acteur", min_value=1, step=1)
                id_film = st.number_input("ID Film", min_value=1, step=1)
            with col2:
                role = st.text_input("Rôle")
                salaire = st.number_input("Salaire ($)", min_value=0, step=100000)
            
            if st.form_submit_button("Ajouter Rôle"):
                try:
                    c.execute("INSERT INTO FILMOGRAPHIE VALUES (?, ?, ?, ?)", 
                            (id_act, id_film, role, salaire))
                    conn.commit()
                    st.success("Rôle ajouté!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur: {e}")
    
    # PAGE STATISTIQUES
    elif page == "Statistiques":
        st.title("📊 Statistiques")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            c.execute("SELECT MIN(salaire) FROM FILMOGRAPHIE")
            st.metric("Salaire Min", f"${c.fetchone()[0]:,.0f}")
        
        with col2:
            c.execute("SELECT AVG(salaire) FROM FILMOGRAPHIE")
            st.metric("Salaire Moyen", f"${c.fetchone()[0]:,.0f}")
        
        with col3:
            c.execute("SELECT MAX(salaire) FROM FILMOGRAPHIE")
            st.metric("Salaire Max", f"${c.fetchone()[0]:,.0f}")
        
        st.markdown("---")
        
        st.subheader("Salaire Moyen par Acteur")
        df_avg = pd.read_sql_query("""
            SELECT A.prenom || ' ' || A.nom as Acteur, 
                   AVG(F.salaire) as Salaire_Moyen,
                   COUNT(*) as Nombre_Films
            FROM ACTEUR A
            JOIN FILMOGRAPHIE F ON A.idActeur = F.idActeur
            GROUP BY A.idActeur
            ORDER BY Salaire_Moyen DESC
        """, conn)
        
        fig = px.bar(df_avg, x='Acteur', y='Salaire_Moyen', 
                     color='Nombre_Films', 
                     color_continuous_scale='Blues')
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Nombre d'Acteurs par Film")
        df_count = pd.read_sql_query("""
            SELECT F.titre, COUNT(*) as nombre
            FROM FILM F
            JOIN FILMOGRAPHIE Fi ON F.idFilm = Fi.idFilm
            GROUP BY F.idFilm
            ORDER BY nombre DESC
        """, conn)
        
        fig = px.bar(df_count, x='titre', y='nombre', color_discrete_sequence=['#3b82f6'])
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
    
    # PAGE GESTION
    elif page == "Gestion":
        st.title("⚙️ Gestion")
        
        tab1, tab2, tab3 = st.tabs(["Modifier", "Exporter", "Importer"])
        
        with tab1:
            st.subheader("Modifier un Salaire")
            col1, col2, col3 = st.columns(3)
            with col1:
                mod_act = st.number_input("ID Acteur", min_value=1, step=1, key="m1")
            with col2:
                mod_film = st.number_input("ID Film", min_value=1, step=1, key="m2")
            with col3:
                new_sal = st.number_input("Nouveau Salaire", min_value=0, step=100000)
            
            if st.button("Modifier"):
                try:
                    c.execute("UPDATE FILMOGRAPHIE SET salaire=? WHERE idActeur=? AND idFilm=?",
                            (new_sal, mod_act, mod_film))
                    conn.commit()
                    if c.rowcount > 0:
                        st.success("Salaire modifié!")
                    else:
                        st.warning("Aucune modification")
                except Exception as e:
                    st.error(f"Erreur: {e}")
        
        with tab2:
            table_exp = st.selectbox("Table à exporter", ["FILM", "ACTEUR", "FILMOGRAPHIE"])
            if st.button("Générer Export"):
                df = pd.read_sql_query(f"SELECT * FROM {table_exp}", conn)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(f"Télécharger {table_exp}.csv", csv, 
                                 f"{table_exp.lower()}.csv", "text/csv")
                st.success(f"{len(df)} lignes prêtes")
        
        with tab3:
            table_imp = st.selectbox("Table cible", ["FILM", "ACTEUR", "FILMOGRAPHIE"])
            uploaded = st.file_uploader("Fichier CSV", type=['csv'])
            
            if uploaded and st.button("Importer"):
                try:
                    df = pd.read_csv(uploaded)
                    df.to_sql(table_imp, conn, if_exists='append', index=False)
                    st.success(f"{len(df)} lignes importées!")
                except Exception as e:
                    st.error(f"Erreur: {e}")
        
        st.markdown("---")
        st.subheader("Informations Système")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            c.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            st.metric("Tables", c.fetchone()[0])
        with col2:
            import os
            if os.path.exists(maBase):
                size = os.path.getsize(maBase) / 1024
                st.metric("Taille DB", f"{size:.2f} KB")
        with col3:
            c.execute("SELECT COUNT(*) FROM FILMOGRAPHIE")
            st.metric("Enregistrements", c.fetchone()[0])
    
    conn.close()

else:
    st.error("❌ Impossible de se connecter à la base de données")
    st.info("Créez le fichier cinema.sqlite d'abord")