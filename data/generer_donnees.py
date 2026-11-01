"""
Génération de données de ventes SIMULÉES pour un hypermarché fictif à Dakar.
Année couverte : 2025 (1er janvier -> 31 décembre).

Les données sont fictives : produits, prix (approximatifs, en FCFA), clients et
tickets sont inventés. Des erreurs sont ajoutées volontairement à la fin pour
servir d'exercice de nettoyage.

Utilisation : python generer_donnees.py   -> crée ventes.csv
"""

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)  # graine fixe = résultats reproductibles

# ---------------------------------------------------------------------------
# 1. Catalogue produits (prix approximatifs en FCFA, à titre d'exemple)
# ---------------------------------------------------------------------------
produits = [
    # (id, nom, catégorie, prix, popularité relative)
    ("P001", "Riz brisé parfumé 5 kg", "Épicerie", 3250, 10),
    ("P002", "Riz brisé 25 kg", "Épicerie", 15000, 3),
    ("P003", "Huile végétale 1 L", "Épicerie", 1350, 9),
    ("P004", "Huile végétale 5 L", "Épicerie", 6500, 4),
    ("P005", "Sucre en morceaux 1 kg", "Épicerie", 900, 8),
    ("P006", "Sucre en poudre 1 kg", "Épicerie", 750, 7),
    ("P007", "Lait en poudre 400 g", "Épicerie", 2500, 7),
    ("P008", "Pâtes spaghetti 500 g", "Épicerie", 450, 6),
    ("P009", "Concentré de tomate 400 g", "Épicerie", 600, 7),
    ("P010", "Bouillon cube (boîte)", "Épicerie", 1200, 6),
    ("P011", "Café Touba 250 g", "Épicerie", 1500, 5),
    ("P012", "Thé vert 200 g", "Épicerie", 1100, 5),
    ("P013", "Couscous de mil 1 kg", "Épicerie", 1200, 4),
    ("P014", "Oignons 1 kg", "Fruits et légumes", 600, 9),
    ("P015", "Pommes de terre 1 kg", "Fruits et légumes", 700, 7),
    ("P016", "Tomates fraîches 1 kg", "Fruits et légumes", 900, 6),
    ("P017", "Bananes 1 kg", "Fruits et légumes", 1000, 5),
    ("P018", "Mangues 1 kg", "Fruits et légumes", 800, 3),
    ("P019", "Poulet entier 1,2 kg", "Boucherie", 3500, 5),
    ("P020", "Viande de bœuf 1 kg", "Boucherie", 4500, 4),
    ("P021", "Viande de mouton 1 kg", "Boucherie", 5000, 2),
    ("P022", "Thiof 1 kg", "Poissonnerie", 5500, 2),
    ("P023", "Yaourt nature x4", "Produits frais", 1400, 5),
    ("P024", "Thiakry 500 g", "Produits frais", 1000, 4),
    ("P025", "Beurre 250 g", "Produits frais", 1800, 3),
    ("P026", "Fromage portions x8", "Produits frais", 1500, 3),
    ("P027", "Pain baguette", "Boulangerie", 150, 10),
    ("P028", "Croissant", "Boulangerie", 400, 4),
    ("P029", "Eau minérale 1,5 L", "Boissons", 400, 9),
    ("P030", "Eau minérale pack 6 x 1,5 L", "Boissons", 2200, 4),
    ("P031", "Jus de bissap 1 L", "Boissons", 1000, 5),
    ("P032", "Soda 1,5 L", "Boissons", 1000, 6),
    ("P033", "Savon de ménage x3", "Hygiène et entretien", 750, 5),
    ("P034", "Lessive en poudre 1 kg", "Hygiène et entretien", 1500, 5),
    ("P035", "Eau de javel 1 L", "Hygiène et entretien", 600, 4),
    ("P036", "Dentifrice 100 ml", "Hygiène et entretien", 900, 4),
    ("P037", "Couches bébé x30", "Bébé", 6000, 2),
    ("P038", "Cahiers 100 pages x5", "Fournitures scolaires", 1500, 1),
    ("P039", "Stylos x10", "Fournitures scolaires", 1000, 1),
    ("P040", "Cartable enfant", "Fournitures scolaires", 8000, 1),
]
catalogue = pd.DataFrame(
    produits, columns=["id_produit", "produit", "categorie", "prix_unitaire_fcfa", "popularite"]
)

# ---------------------------------------------------------------------------
# 2. Saisonnalité et événements (dates 2025 approximatives)
# ---------------------------------------------------------------------------
jours = pd.date_range("2025-01-01", "2025-12-31", freq="D")

def coefficient_jour(d):
    """Multiplicateur du nombre de tickets selon le jour."""
    c = 1.0
    c *= {0: 0.85, 1: 0.85, 2: 0.9, 3: 0.95, 4: 1.15, 5: 1.35, 6: 1.1}[d.weekday()]
    if d.day >= 25 or d.day <= 3:            # fin / début de mois (salaires)
        c *= 1.2
    if pd.Timestamp("2025-02-25") <= d <= pd.Timestamp("2025-03-29"):  # Ramadan
        c *= 1.15
    if pd.Timestamp("2025-03-25") <= d <= pd.Timestamp("2025-03-30"):  # avant Korité
        c *= 1.4
    if pd.Timestamp("2025-05-30") <= d <= pd.Timestamp("2025-06-06"):  # avant Tabaski
        c *= 1.6
    if pd.Timestamp("2025-09-25") <= d <= pd.Timestamp("2025-10-15"):  # rentrée scolaire
        c *= 1.1
    if pd.Timestamp("2025-12-20") <= d <= pd.Timestamp("2025-12-31"):  # fêtes de fin d'année
        c *= 1.25
    return c

def poids_produits(d):
    """Popularité des produits ajustée selon la période."""
    p = catalogue["popularite"].astype(float).copy()
    ids = catalogue["id_produit"]
    if pd.Timestamp("2025-02-25") <= d <= pd.Timestamp("2025-03-29"):    # Ramadan
        p[ids.isin(["P005", "P006", "P007", "P024", "P031", "P017"])] *= 2.0
    if pd.Timestamp("2025-05-30") <= d <= pd.Timestamp("2025-06-06"):    # Tabaski
        p[ids.isin(["P014", "P015", "P003", "P004", "P021", "P032", "P029"])] *= 3.0
    if pd.Timestamp("2025-09-25") <= d <= pd.Timestamp("2025-10-15"):    # rentrée
        p[ids.isin(["P038", "P039", "P040"])] *= 12.0
    if 4 <= d.month <= 7:                                                # saison des mangues
        p[ids == "P018"] *= 4.0
    if d.month in (4, 5, 6, 7, 8, 9):                                    # chaleur
        p[ids.isin(["P029", "P030", "P031", "P032"])] *= 1.5
    return (p / p.sum()).to_numpy()

# Heures d'affluence (8 h - 22 h)
heures = np.arange(8, 22)
poids_heures = np.array([2, 3, 4, 5, 6, 5, 4, 4, 5, 7, 9, 9, 7, 4], dtype=float)
poids_heures /= poids_heures.sum()

modes_paiement = ["Espèces", "Wave", "Orange Money", "Carte bancaire"]
poids_paiement = [0.40, 0.30, 0.15, 0.15]

clients_fidelite = [f"C{n:04d}" for n in range(1, 801)]
# quelques clients très fidèles, beaucoup d'occasionnels
poids_clients = rng.pareto(1.5, len(clients_fidelite)) + 0.1
poids_clients /= poids_clients.sum()

# ---------------------------------------------------------------------------
# 3. Génération des tickets et des lignes de vente
# ---------------------------------------------------------------------------
lignes = []
num_ticket = 1
TICKETS_PAR_JOUR_BASE = 13

for d in jours:
    n_tickets = rng.poisson(TICKETS_PAR_JOUR_BASE * coefficient_jour(d))
    w = poids_produits(d)
    for _ in range(n_tickets):
        heure = rng.choice(heures, p=poids_heures)
        minute = rng.integers(0, 60)
        horodatage = d + pd.Timedelta(hours=int(heure), minutes=int(minute))
        id_ticket = f"T{num_ticket:06d}"
        num_ticket += 1

        paiement = rng.choice(modes_paiement, p=poids_paiement)
        client = rng.choice(clients_fidelite, p=poids_clients) if rng.random() < 0.45 else None
        caisse = int(rng.integers(1, 9))

        n_articles = min(1 + rng.poisson(2.2), 12)
        idx = rng.choice(len(catalogue), size=n_articles, replace=False, p=w)
        for i in idx:
            prod = catalogue.iloc[i]
            qte = 1 + rng.poisson(0.6) if prod["prix_unitaire_fcfa"] < 3000 else 1
            lignes.append({
                "id_ticket": id_ticket,
                "date": horodatage.strftime("%Y-%m-%d"),
                "heure": horodatage.strftime("%H:%M"),
                "id_produit": prod["id_produit"],
                "produit": prod["produit"],
                "categorie": prod["categorie"],
                "quantite": int(qte),
                "prix_unitaire_fcfa": int(prod["prix_unitaire_fcfa"]),
                "montant_fcfa": int(qte * prod["prix_unitaire_fcfa"]),
                "mode_paiement": paiement,
                "id_client": client,
                "caisse": caisse,
            })

df = pd.DataFrame(lignes)

# ---------------------------------------------------------------------------
# 4. Ajout VOLONTAIRE d'erreurs (exercice de nettoyage)
# ---------------------------------------------------------------------------
n = len(df)

# a) Lignes en double (~1 %)
doublons = df.sample(frac=0.01, random_state=1)
df = pd.concat([df, doublons], ignore_index=True)

# b) Quantités manquantes (~0,5 %) -> montant aussi manquant
idx = df.sample(frac=0.005, random_state=2).index
df.loc[idx, ["quantite", "montant_fcfa"]] = np.nan

# c) Catégories mal orthographiées / casse incohérente (~2 %)
variantes = {
    "Épicerie": ["Epicerie", "épicerie", "EPICERIE"],
    "Boissons": ["boissons", "Boisson"],
    "Fruits et légumes": ["Fruits et legumes", "fruits et légumes"],
    "Produits frais": ["Produit frais", "produits frais"],
}
idx = df.sample(frac=0.02, random_state=3).index
for i in idx:
    cat = df.at[i, "categorie"]
    if cat in variantes:
        df.at[i, "categorie"] = rng.choice(variantes[cat])

# d) Dates dans un autre format (~1 %) : JJ/MM/AAAA au lieu de AAAA-MM-JJ
idx = df.sample(frac=0.01, random_state=4).index
df.loc[idx, "date"] = pd.to_datetime(df.loc[idx, "date"]).dt.strftime("%d/%m/%Y")

# e) Quantités aberrantes (erreurs de saisie) : 15 lignes avec 99 ou 999
idx = df.sample(n=15, random_state=5).index
df.loc[idx, "quantite"] = rng.choice([99, 999], size=15)
df.loc[idx, "montant_fcfa"] = df.loc[idx, "quantite"] * df.loc[idx, "prix_unitaire_fcfa"]

# f) Espaces parasites dans les modes de paiement (~1 %)
idx = df.sample(frac=0.01, random_state=6).index
df.loc[idx, "mode_paiement"] = " " + df.loc[idx, "mode_paiement"] + "  "

# Mélange léger de l'ordre des lignes (comme un export réel)
df = df.sample(frac=1, random_state=7).reset_index(drop=True)

df.to_csv("ventes.csv", index=False, encoding="utf-8-sig")
print(f"ventes.csv créé : {len(df)} lignes, {df['id_ticket'].nunique()} tickets")
