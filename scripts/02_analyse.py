"""
ÉTAPE 2 : ANALYSE ET GRAPHIQUES
===============================
Lit les données propres (data/ventes_propres.csv), répond aux 5 questions
business et enregistre les graphiques dans le dossier images/.

À lancer APRÈS 01_nettoyage.py.
Lancer : bouton ▶ en haut à droite de VS Code (« Run Python File »).
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

PROJET = Path(__file__).resolve().parent.parent
FICHIER_PROPRE = PROJET / "data" / "ventes_propres.csv"
DOSSIER_IMAGES = PROJET / "images"
DOSSIER_IMAGES.mkdir(exist_ok=True)

# --- Style des graphiques : une couleur principale (bleu), une pour mettre en avant (orange)
BLEU, ORANGE, GRIS = "#2a78d6", "#eb6834", "#898781"
plt.rcParams.update({
    "figure.figsize": (10, 5), "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "axes.titleweight": "bold", "font.size": 11,
})
millions = mtick.FuncFormatter(lambda x, _: f"{x / 1e6:.1f} M")  # axe en millions de FCFA


def titre(texte):
    print("\n" + "=" * 60)
    print(texte)
    print("=" * 60)


def sauver(nom):
    """Enregistre le graphique en cours dans images/ puis le ferme."""
    plt.tight_layout()
    plt.savefig(DOSSIER_IMAGES / f"{nom}.png", dpi=120, bbox_inches="tight")
    plt.close()
    print(f"   📊 Graphique enregistré : images/{nom}.png")


def fcfa(x):
    """Formate un nombre en FCFA avec des espaces : 7150 -> '7 150 FCFA'."""
    return f"{x:,.0f} FCFA".replace(",", " ")


# ---------------------------------------------------------------------------
# Chargement des données propres
# ---------------------------------------------------------------------------
df = pd.read_csv(FICHIER_PROPRE, parse_dates=["date"])

# Une ligne = un produit. Pour parler de "tickets", on regroupe par id_ticket.
tickets = df.groupby("id_ticket").agg(
    date=("date", "first"),
    heure_num=("heure_num", "first"),
    jour_num=("jour_num", "first"),
    montant=("montant_fcfa", "sum"),
    articles=("quantite", "sum"),
    paiement=("mode_paiement", "first"),
    fidele=("client_fidele", "first"),
)

titre("VUE D'ENSEMBLE")
ca_total = df["montant_fcfa"].sum()
print(f"Chiffre d'affaires 2025 : {fcfa(ca_total)}")
print(f"Nombre de tickets       : {len(tickets):,}".replace(",", " "))
print(f"Panier moyen            : {fcfa(tickets['montant'].mean())}")
print(f"Articles par ticket     : {tickets['articles'].mean():.1f}")


# ---------------------------------------------------------------------------
# Question 1 : quels rayons rapportent le plus ?
# ---------------------------------------------------------------------------
titre("QUESTION 1 : QUELS RAYONS RAPPORTENT LE PLUS ?")

ca_rayon = df.groupby("categorie")["montant_fcfa"].sum().sort_values()
part_rayon = ca_rayon / ca_total
print((part_rayon.sort_values(ascending=False) * 100).round(1).to_string())

top2 = part_rayon.sort_values(ascending=False).head(2)
print(f"\n-> Les 2 premiers rayons ({', '.join(top2.index)}) = {top2.sum():.0%} du CA")

fig, ax = plt.subplots()
couleurs = [ORANGE if c == ca_rayon.index[-1] else BLEU for c in ca_rayon.index]
ax.barh(ca_rayon.index, ca_rayon.values, color=couleurs, height=0.6)
for i, (v, p) in enumerate(zip(ca_rayon.values, part_rayon.values)):
    ax.text(v, i, f"  {p:.0%}", va="center", color="#52514e")
ax.xaxis.set_major_formatter(millions)
ax.set_xlabel("Chiffre d'affaires (millions de FCFA)")
ax.set_title("L'Épicerie porte le magasin")
ax.grid(axis="y", visible=False)
sauver("ca_par_rayon")


# ---------------------------------------------------------------------------
# Question 2 : quand les clients viennent-ils ?
# ---------------------------------------------------------------------------
titre("QUESTION 2a : VENTES PAR MOIS")

MOIS = ["Janv", "Févr", "Mars", "Avr", "Mai", "Juin", "Juil", "Août", "Sept", "Oct", "Nov", "Déc"]
ca_mois = df.groupby("mois_num")["montant_fcfa"].sum()
ecart = ca_mois / ca_mois.mean() - 1
for m in ca_mois.index:
    print(f"{MOIS[m - 1]:5s} : {fcfa(ca_mois[m]):>16s}  ({ecart[m]:+.0%} vs moyenne)")

fig, ax = plt.subplots()
ax.plot(MOIS, ca_mois.values, color=BLEU, linewidth=2, marker="o", markersize=8)
ax.axhline(ca_mois.mean(), color=GRIS, linestyle="--", linewidth=1)
ax.text(11, ca_mois.mean(), " moyenne", color=GRIS, va="bottom", ha="right")
for m, label in [(3, "Ramadan + Korité"), (12, "Fêtes de fin d'année")]:
    ax.annotate(label, (m - 1, ca_mois[m]), textcoords="offset points", xytext=(0, 10),
                ha="center", color=ORANGE, fontweight="bold")
ax.yaxis.set_major_formatter(millions)
ax.set_ylabel("CA (millions de FCFA)")
ax.set_title("Mars et décembre sont les meilleurs mois")
sauver("ventes_par_mois")


titre("QUESTION 2b : L'EFFET TABASKI")

# CA de chaque jour de l'année
ca_jour = df.groupby("date")["montant_fcfa"].sum()
semaine_tabaski = (ca_jour.index >= "2025-05-30") & (ca_jour.index <= "2025-06-06")
hausse_tabaski = ca_jour[semaine_tabaski].mean() / ca_jour[~semaine_tabaski].mean() - 1
print(f"CA moyen par jour la semaine avant la Tabaski : +{hausse_tabaski:.0%} vs le reste de l'année")

# Quels produits se vendent le plus en plus ? (quantité par jour, Tabaski vs normale)
est_tabaski = df["date"].between("2025-05-30", "2025-06-06")
qte_tabaski = df[est_tabaski].groupby("produit")["quantite"].sum() / semaine_tabaski.sum()
qte_normale = df[~est_tabaski].groupby("produit")["quantite"].sum() / (~semaine_tabaski).sum()
multiplicateur = (qte_tabaski / qte_normale).sort_values(ascending=False).head(6)
print("\nProduits qui explosent (ventes par jour vs normale) :")
for produit, x in multiplicateur.items():
    print(f"   {produit:25s} x{x:.1f}")

fig, ax = plt.subplots(figsize=(10, 4))
fenetre = ca_jour["2025-05-01":"2025-06-30"]
couleurs = [ORANGE if pd.Timestamp("2025-05-30") <= d <= pd.Timestamp("2025-06-06") else BLEU
            for d in fenetre.index]
ax.bar(fenetre.index, fenetre.values, color=couleurs, width=0.8)
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x / 1e3:.0f} k"))
ax.set_ylabel("CA par jour (milliers de FCFA)")
ax.set_title("La semaine avant la Tabaski (en orange)")
ax.grid(axis="x", visible=False)
sauver("effet_tabaski")


titre("QUESTION 2c : AFFLUENCE PAR JOUR ET PAR HEURE")

JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
# Tableau croisé : lignes = jours, colonnes = heures, valeurs = nombre de tickets
carte = tickets.pivot_table(index="jour_num", columns="heure_num", values="montant", aggfunc="count").fillna(0)
carte.index = JOURS

fig, ax = plt.subplots(figsize=(11, 4.5))
image = ax.imshow(carte.values, cmap="Blues", aspect="auto")
ax.set_xticks(range(len(carte.columns)), [f"{h}h" for h in carte.columns])
ax.set_yticks(range(7), carte.index)
ax.grid(False)
plt.colorbar(image, ax=ax, label="Nombre de tickets sur l'année")
ax.set_title("Affluence : le vendredi et le samedi en fin de journée")
sauver("affluence_jour_heure")

part_ven_sam = tickets["jour_num"].isin([5, 6]).mean()      # 5 = vendredi, 6 = samedi
part_18_21 = tickets["heure_num"].between(18, 20).mean()    # tickets de 18:00 à 20:59
print(f"Vendredi + samedi = {part_ven_sam:.0%} des tickets (29 % si l'affluence était égale)")
print(f"18 h - 21 h       = {part_18_21:.0%} des tickets")


# ---------------------------------------------------------------------------
# Question 3 : quel est le panier moyen ?
# ---------------------------------------------------------------------------
titre("QUESTION 3 : PANIER MOYEN")

panier_fidelite = tickets.groupby("fidele")["montant"].mean()
print(f"Panier moyen SANS carte de fidélité : {fcfa(panier_fidelite['Non'])}")
print(f"Panier moyen AVEC carte de fidélité : {fcfa(panier_fidelite['Oui'])}")
print("-> Surprise : la carte de fidélité ne fait pas augmenter le panier.")

petits = (tickets["montant"] < 5000).mean()
mediane = tickets["montant"].median()
print(f"{petits:.0%} des tickets font moins de 5 000 FCFA (médiane : {fcfa(mediane)})")

fig, ax = plt.subplots(figsize=(10, 4))
ax.hist(tickets["montant"], bins=40, color=BLEU, edgecolor="white")
ax.axvline(mediane, color=ORANGE, linewidth=2)
ax.text(mediane, ax.get_ylim()[1] * 0.9, f"  médiane : {fcfa(mediane)}", color=ORANGE, fontweight="bold")
ax.set_xlabel("Montant du ticket (FCFA)")
ax.set_ylabel("Nombre de tickets")
ax.set_title("La plupart des paniers sont petits")
sauver("distribution_panier")


# ---------------------------------------------------------------------------
# Question 4 : quels produits sont incontournables ?
# ---------------------------------------------------------------------------
titre("QUESTION 4 : PRODUITS INCONTOURNABLES")

top10 = df.groupby("produit")["montant_fcfa"].sum().sort_values(ascending=False).head(10)
part_top10 = top10.sum() / ca_total
print(f"Le top 10 (sur 40 produits) fait {part_top10:.0%} du CA :")
for produit, ca in top10.items():
    print(f"   {produit:28s} {fcfa(ca):>15s}")

fig, ax = plt.subplots()
ax.barh(top10.index[::-1], top10.values[::-1], color=BLEU, height=0.6)
ax.xaxis.set_major_formatter(millions)
ax.set_xlabel("CA (millions de FCFA)")
ax.set_title(f"Top 10 des produits : {part_top10:.0%} du CA sur 40 références")
ax.grid(axis="y", visible=False)
sauver("top10_produits")


# ---------------------------------------------------------------------------
# Question 5 : comment les clients paient-ils ?
# ---------------------------------------------------------------------------
titre("QUESTION 5 : MODES DE PAIEMENT")

part_paiement = tickets["paiement"].value_counts(normalize=True).sort_values()
print((part_paiement.sort_values(ascending=False) * 100).round(1).to_string())
mobile = part_paiement[["Wave", "Orange Money"]].sum()
print(f"\n-> Paiement mobile (Wave + Orange Money) : {mobile:.0%} des tickets")

fig, ax = plt.subplots(figsize=(10, 3.5))
couleurs = [ORANGE if p in ("Wave", "Orange Money") else BLEU for p in part_paiement.index]
ax.barh(part_paiement.index, part_paiement.values, color=couleurs, height=0.6)
for i, v in enumerate(part_paiement.values):
    ax.text(v, i, f"  {v:.0%}", va="center", color="#52514e")
ax.xaxis.set_major_formatter(mtick.PercentFormatter(1))
ax.set_title("Paiement mobile (en orange) : presque un ticket sur deux")
ax.grid(axis="y", visible=False)
sauver("modes_paiement")


# ---------------------------------------------------------------------------
# Bonus : rentrée scolaire
# ---------------------------------------------------------------------------
fournitures = df[df["categorie"] == "Fournitures scolaires"]
part_rentree = fournitures[fournitures["mois_num"].isin([9, 10])]["montant_fcfa"].sum() / fournitures["montant_fcfa"].sum()


# ---------------------------------------------------------------------------
# Synthèse et recommandations
# ---------------------------------------------------------------------------
titre("SYNTHÈSE")
print(f"• Rayons      : {', '.join(top2.index)} = {top2.sum():.0%} du CA")
print(f"• Tabaski     : +{hausse_tabaski:.0%} de CA par jour la semaine avant")
print(f"• Affluence   : vendredi + samedi = {part_ven_sam:.0%} des tickets ; 18 h-21 h = {part_18_21:.0%}")
print(f"• Panier      : {fcfa(tickets['montant'].mean())} en moyenne ; {petits:.0%} des tickets < 5 000 FCFA")
print(f"• Produits    : top 10 = {part_top10:.0%} du CA")
print(f"• Paiement    : mobile = {mobile:.0%} des tickets")
print(f"• Rentrée     : {part_rentree:.0%} des fournitures scolaires vendues en sept.-oct.")

titre("MES 3 RECOMMANDATIONS")
print("1. Renforcer les caisses le vendredi et le samedi, de 18 h à 21 h.")
print("2. Augmenter les stocks 10 jours avant la Tabaski et la Korité")
print("   (mouton, oignons, pommes de terre, huile, boissons).")
print("3. Revoir le programme de fidélité : avantages à partir d'un montant d'achat,")
print("   compatibles Wave et Orange Money, pour faire grossir les petits paniers.")

print("\n✅ Analyse terminée. Les graphiques sont dans le dossier images/")
