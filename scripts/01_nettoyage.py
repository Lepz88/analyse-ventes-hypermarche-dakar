"""
ÉTAPE 1 : NETTOYAGE DES DONNÉES
================================
Lit les données brutes (data/ventes.csv), corrige les erreurs
et enregistre un fichier propre (data/ventes_propres.csv).

Lancer : bouton ▶ en haut à droite de VS Code (« Run Python File »).
"""

from pathlib import Path
import pandas as pd

# Dossier du projet (fonctionne quel que soit l'endroit d'où on lance le script)
PROJET = Path(__file__).resolve().parent.parent
FICHIER_BRUT = PROJET / "data" / "ventes.csv"
FICHIER_PROPRE = PROJET / "data" / "ventes_propres.csv"


def titre(texte):
    """Affiche un titre de section dans le terminal."""
    print("\n" + "=" * 60)
    print(texte)
    print("=" * 60)


# ---------------------------------------------------------------------------
# 1. Chargement et première inspection
# ---------------------------------------------------------------------------
titre("1. CHARGEMENT")

brut = pd.read_csv(FICHIER_BRUT)
print(f"{len(brut):,} lignes, {brut.shape[1]} colonnes".replace(",", " "))

print("\nLes 5 premières lignes :")
print(brut.head().to_string())

print("\nValeurs manquantes par colonne :")
print(brut.isna().sum())
# Note : id_client vide n'est PAS une erreur (client sans carte de fidélité).
# En revanche, quantite et montant_fcfa vides sont des erreurs de saisie.


# ---------------------------------------------------------------------------
# 2. Nettoyage (chaque correction est notée dans un journal)
# ---------------------------------------------------------------------------
titre("2. NETTOYAGE")

df = brut.copy()   # on travaille sur une copie pour garder les données brutes intactes
journal = []       # liste des corrections : (problème, nombre de lignes, solution)

# a) Espaces en trop dans le mode de paiement (" Wave  " -> "Wave")
nb = (df["mode_paiement"] != df["mode_paiement"].str.strip()).sum()
df["mode_paiement"] = df["mode_paiement"].str.strip()
journal.append(("Espaces en trop (paiement)", nb, "Suppression des espaces"))

# b) Catégories mal orthographiées
print("Catégories AVANT :", sorted(df["categorie"].unique()))
corrections = {
    "Epicerie": "Épicerie", "épicerie": "Épicerie", "EPICERIE": "Épicerie",
    "boissons": "Boissons", "Boisson": "Boissons",
    "Fruits et legumes": "Fruits et légumes", "fruits et légumes": "Fruits et légumes",
    "Produit frais": "Produits frais", "produits frais": "Produits frais",
}
nb = df["categorie"].isin(corrections.keys()).sum()
df["categorie"] = df["categorie"].replace(corrections)
print("Catégories APRÈS :", sorted(df["categorie"].unique()))
journal.append(("Catégories mal écrites", nb, "Harmonisation des noms"))

# c) Dates dans deux formats : AAAA-MM-JJ (normal) et JJ/MM/AAAA (erreur)
format_fr = df["date"].str.contains("/")
nb = format_fr.sum()
dates = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
dates[format_fr] = pd.to_datetime(df.loc[format_fr, "date"], format="%d/%m/%Y")
df["date"] = dates
assert df["date"].isna().sum() == 0, "Certaines dates n'ont pas pu être lues"
journal.append(("Dates au format JJ/MM/AAAA", nb, "Conversion en vraie date"))

# d) Doublons : on les supprime APRÈS avoir harmonisé le texte et les dates,
#    sinon deux lignes identiques ("Epicerie" / "Épicerie") ne seraient pas détectées.
nb = df.duplicated().sum()
df = df.drop_duplicates()
journal.append(("Lignes en double", nb, "Suppression"))

# e) Quantités manquantes : impossible de retrouver la vraie valeur -> suppression
nb = df["quantite"].isna().sum()
part = nb / len(df)
df = df.dropna(subset=["quantite"])
journal.append(("Quantités manquantes", nb, f"Suppression ({part:.1%} des lignes)"))

# f) Quantités aberrantes : regardons d'abord la distribution
print("\nRépartition des quantités :")
print(df["quantite"].value_counts().sort_index())
# On voit des 99 et 999 : impossible en caisse ménage -> erreurs de saisie.
SEUIL = 20
aberrant = df["quantite"] > SEUIL
nb = aberrant.sum()
faux_ca = df.loc[aberrant, "montant_fcfa"].sum()
df = df[~aberrant]
journal.append(("Quantités aberrantes (99, 999)", nb, f"Suppression (seuil {SEUIL})"))

# Les quantités et montants peuvent maintenant être des nombres entiers
df["quantite"] = df["quantite"].astype(int)
df["montant_fcfa"] = df["montant_fcfa"].astype(int)

# Vérification finale : montant = quantité × prix sur toutes les lignes
assert (df["montant_fcfa"] == df["quantite"] * df["prix_unitaire_fcfa"]).all()

print("\nJOURNAL DE NETTOYAGE :")
print(pd.DataFrame(journal, columns=["Problème", "Lignes", "Solution"]).to_string(index=False))
print(f"\nLignes : {len(brut):,} -> {len(df):,}".replace(",", " "))


# ---------------------------------------------------------------------------
# 3. Pourquoi ce nettoyage compte : l'exemple d'août
# ---------------------------------------------------------------------------
titre("3. IMPACT DU NETTOYAGE (exemple d'août)")

aout_brut = brut[brut["date"].str.startswith("2025-08") | brut["date"].str.endswith("/08/2025")]
ca_aout_brut = aout_brut["montant_fcfa"].sum()
ca_aout_propre = df.loc[df["date"].dt.month == 8, "montant_fcfa"].sum()
print(f"CA d'août AVANT nettoyage : {ca_aout_brut:,.0f} FCFA".replace(",", " "))
print(f"CA d'août APRÈS nettoyage : {ca_aout_propre:,.0f} FCFA".replace(",", " "))
print(f"-> Surestimation : x{ca_aout_brut / ca_aout_propre:.1f}")
print(f"Les quantités aberrantes ajoutaient {faux_ca:,.0f} FCFA de faux CA.".replace(",", " "))


# ---------------------------------------------------------------------------
# 4. Ajout de colonnes utiles (filtres Power BI) et enregistrement
# ---------------------------------------------------------------------------
titre("4. ENREGISTREMENT")

MOIS = ["Janv", "Févr", "Mars", "Avr", "Mai", "Juin", "Juil", "Août", "Sept", "Oct", "Nov", "Déc"]
JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

df["mois_num"] = df["date"].dt.month
df["mois"] = df["mois_num"].map(lambda m: MOIS[m - 1])
df["jour_num"] = df["date"].dt.dayofweek + 1          # 1 = lundi
df["jour_semaine"] = df["jour_num"].map(lambda j: JOURS[j - 1])
df["heure_num"] = df["heure"].str[:2].astype(int)
df["client_fidele"] = df["id_client"].notna().map({True: "Oui", False: "Non"})
df["paiement_mobile"] = df["mode_paiement"].isin(["Wave", "Orange Money"]).map({True: "Oui", False: "Non"})
df["date"] = df["date"].dt.strftime("%Y-%m-%d")

# utf-8-sig : garde les accents lisibles dans Excel et Power BI
df.to_csv(FICHIER_PROPRE, index=False, encoding="utf-8-sig")
print(f"Fichier propre enregistré : {FICHIER_PROPRE.name} ({len(df):,} lignes)".replace(",", " "))
print("\n✅ Nettoyage terminé. Lance maintenant 02_analyse.py")
