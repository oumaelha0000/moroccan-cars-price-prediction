import streamlit as st
import pandas as pd
import joblib, base64, pathlib

# ░░ CONFIGURATION & FOND ░░
st.set_page_config("🚗 Prédiction de Prix Voiture", layout="wide")

def set_background(image_path: str) -> None:
    encoded = base64.b64encode(pathlib.Path(image_path).read_bytes()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background: url("data:image/jpg;base64,{encoded}") center/cover fixed;
        }}
        .overlay {{
            position: fixed; inset: 0;
            background: rgba(15,23,42,0.60);
            z-index: -1;
        }}
        .glass {{
            max-width: 680px;
            margin: -20px auto 0;
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(6px);
            border: 1px solid rgba(255,255,255,0.18);
            border-radius: 12px;
            padding: 0 2rem 2rem;
            box-shadow: 0 4px 30px rgba(0,0,0,0.2);
        }}

        /* ───── LABELS : VERT MAROC + SHADOW ───── */
        label {{
            background: rgba(22,160,73,0.8);
            padding: 0.3rem 0.8rem;
            border-radius: 6px;
            color: #ffffff !important;
            font-size: 1.05rem;
            font-weight: 700 !important;
            text-shadow: 0 0 6px rgba(0,0,0,.4);
            margin-bottom: 6px;
            display: inline-block;
            box-shadow: 0 2px 6px rgba(0,0,0,0.3);
        }}

        /* ───── TITRE : CARTOUCHE ROUGE 🇲🇦 + ICÔNE ───── */
        .title-box {{
            display: inline-block;
            background: rgba(220, 38, 38, 0.90);
            padding: 0.4rem 1.6rem;
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,.25);
            margin: 0.2rem auto 0.8rem auto;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}
        .title-box h1 {{
            margin: 0;
            font-size: 4.2rem;
            font-weight: 900;
            letter-spacing: 3px;
            color: #fff;
        }}
        </style>
        <div class="overlay"></div>
    """, unsafe_allow_html=True)

set_background("image.png")

# ░░ TITRES ░░
st.markdown("""
<div style="text-align:center">
    <div class="title-box">
        <h1>🇲🇦 MOROCCAN CARS</h1>
    </div>
</div>

<h2 style="
    text-align:center;
    font-size:2.4rem;
    font-weight:700;
    color:#ffffff;
    background-color:#333333;
    padding:0.5rem 1rem;
    border-radius:8px;
    margin-bottom:1.8rem;">
    Prédiction du prix d'un véhicule d'occasion
</h2>
""", unsafe_allow_html=True)

# ░░ CHARGEMENT MODÈLE ░░
model   = joblib.load("random_forest_model.pkl")
scaler  = joblib.load("scaler.pkl")
columns = joblib.load("columns.pkl")

# ░░ FORMULAIRE ░░
with st.container():
    st.markdown('<div class="glass">', unsafe_allow_html=True)

    localisations = sorted([c.replace("localisation_", "") for c in columns if c.startswith("localisation_")])
    boites        = sorted([c.replace("boite_vitesses_", "") for c in columns if c.startswith("boite_vitesses_")])
    carburants    = sorted([c.replace("type_carburant_", "") for c in columns if c.startswith("type_carburant_")])
    origines      = sorted([c.replace("origine_", "") for c in columns if c.startswith("origine_")])
    etats         = sorted([c.replace("etat_", "") for c in columns if c.startswith("etat_")])
    modeles       = sorted([c.replace("modele_", "") for c in columns if c.startswith("modele_")])
    marques       = sorted([c.replace("marque_", "") for c in columns if c.startswith("marque_")])

    _, col, _ = st.columns([1, 2, 1])
    with col:
        localisation      = st.selectbox("Localisation", localisations)
        annee_modele      = st.number_input("Année du modèle", 1980, 2025, step=1)
        marque            = st.selectbox("Marque", marques)
        modele            = st.selectbox("Modèle", modeles)
        boite_vitesses    = st.selectbox("Boîte de vitesses", boites)
        type_carburant    = st.selectbox("Type de carburant", carburants)
        kilometrage       = st.number_input("Kilométrage (km)", 0, 800_000, step=1_000)
        nombre_de_portes  = st.selectbox("Nombre de portes", [2, 3, 4, 5])
        puissance_fiscale = st.number_input("Puissance fiscale", 1, 20)
        origine           = st.selectbox("Origine", origines)
        premiere_main     = st.selectbox("Première main", ["Oui", "Non"])
        etat              = st.selectbox("État", etats)

    input_dict = {
        "annee_modele": annee_modele,
        "kilometrage": kilometrage,
        "nombre_de_portes": nombre_de_portes,
        "puissance_fiscale": puissance_fiscale,
        "premiere_main": 1 if premiere_main == "Oui" else 0,
        f"localisation_{localisation}": 1,
        f"boite_vitesses_{boite_vitesses}": 1,
        f"type_carburant_{type_carburant}": 1,
        f"origine_{origine}": 1,
        f"etat_{etat}": 1,
        f"marque_{marque}": 1,
        f"modele_{modele}": 1,
    }

    X_input = pd.DataFrame([0] * len(columns), index=columns).T
    for k, v in input_dict.items():
        if k in X_input.columns:
            X_input[k] = v

    X_input[scaler.feature_names_in_] = scaler.transform(X_input[scaler.feature_names_in_])

    center_col = st.columns(3)[1]
    with center_col:
        if st.button("📈 Prédire le prix", use_container_width=True):
            price = model.predict(X_input)[0]
            st.markdown(f"""
                <div style='
                    background:rgba(34,197,94,.15);
                    border:1px solid #22c55e;
                    border-radius:12px;
                    padding:1.2rem;
                    font-size:1.8rem;
                    font-weight:bold;
                    text-align:center;
                    color:#bbf7d0;
                    margin-top:1rem;'>
                    💰 Prix estimé : {price:,.0f} MAD
                </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
