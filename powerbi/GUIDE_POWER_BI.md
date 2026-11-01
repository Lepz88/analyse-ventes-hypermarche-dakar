# 📊 Guide : construire le tableau de bord Power BI pas à pas

**Durée :** 2 soirées d'environ 2 h 30.
**Il te faut :** Power BI Desktop (gratuit, sur Windows), à installer depuis le Microsoft Store.
**Fichiers :** `data/ventes_propres.csv` (données déjà nettoyées par le script `01_nettoyage.py`) et `powerbi/theme_projet.json` (couleurs du projet).

> ℹ️ Les noms des menus peuvent varier légèrement selon ta version de Power BI.
> Si tu ne trouves pas un bouton, cherche un nom proche ou envoie-moi une capture d'écran.

---

## 🎯 Le résultat visé : une page qu'un directeur de magasin comprend en 10 secondes

```
┌──────────────────────────────────────────────────────────────────┐
│  Ventes 2025 : hypermarché à Dakar (données simulées)            │
├─────────────┬─────────────┬─────────────┬────────────────────────┤
│  CA total   │  Tickets    │ Panier moyen│ % paiement mobile      │
├─────────────┴─────────────┴──────┬──────┴────────────────────────┤
│  CA par mois (courbe)            │  CA par rayon (barres)        │
├──────────────────────────────────┼───────────────────────────────┤
│  Affluence jour × heure (matrice)│  Top 10 produits (barres)     │
├──────────────────────────────────┴───────────────────────────────┤
│  Filtres : Mois · Rayon · Mode de paiement · Client fidèle       │
└──────────────────────────────────────────────────────────────────┘
```

---

# SOIRÉE 1 : données, mesures et indicateurs

## Étape 1 : importer les données (10 min)
1. Ouvre Power BI Desktop, puis **Accueil** → **Obtenir les données** → **Texte/CSV**.
2. Choisis `ventes_propres.csv`.
3. Dans l'aperçu, vérifie que les accents s'affichent bien (« Épicerie »). Si ce n'est pas le cas, choisis **Origine du fichier : 65001 : Unicode (UTF-8)**.
4. Clique sur **Transformer les données** (pas « Charger » directement).

## Étape 2 : vérifier les types de colonnes dans Power Query (15 min)
Clique sur l'icône à gauche du nom de chaque colonne pour corriger son type si besoin :

| Colonne | Type attendu |
|---|---|
| `date` | Date |
| `quantite`, `prix_unitaire_fcfa`, `montant_fcfa`, `mois_num`, `jour_num`, `heure_num`, `caisse` | Nombre entier |
| Toutes les autres | Texte |

Clique ensuite sur **Fermer et appliquer**.

> 💡 Si la colonne `date` affiche des erreurs, fais un clic droit sur la colonne → **Modifier le type** → **Utilisation des paramètres régionaux…** → Date, **Anglais (États-Unis)**.

## Étape 3 : appliquer le thème du projet (5 min)
**Affichage** → **Thèmes** (la flèche) → **Rechercher les thèmes** → choisis `theme_projet.json`.
Tes graphiques prendront les mêmes couleurs que ceux du script Python (bleu et orange).

## Étape 4 : trier les mois et les jours dans le bon ordre (10 min)
Sans cette étape, Power BI trie par ordre alphabétique (Août, Avr, Déc…).
1. Vue **Données** (icône tableau à gauche), puis clique sur la colonne `mois`.
2. **Outils de colonne** → **Trier par colonne** → `mois_num`.
3. Même chose pour `jour_semaine`, triée par `jour_num`.

## Étape 5 : créer les mesures DAX (30 min)
Une **mesure** est un calcul qui se met à jour selon les filtres. C'est la base de Power BI.

**Accueil** → **Nouvelle mesure**, puis colle chaque formule une par une :

```DAX
CA = SUM(ventes_propres[montant_fcfa])
```
```DAX
Nb tickets = DISTINCTCOUNT(ventes_propres[id_ticket])
```
```DAX
Panier moyen = DIVIDE([CA], [Nb tickets])
```
```DAX
Articles par ticket = DIVIDE(SUM(ventes_propres[quantite]), [Nb tickets])
```
```DAX
% paiement mobile =
DIVIDE(
    CALCULATE([Nb tickets], ventes_propres[paiement_mobile] = "Oui"),
    [Nb tickets]
)
```
```DAX
Part du CA =
DIVIDE([CA], CALCULATE([CA], ALL(ventes_propres[categorie])))
```

**Formats** (clique sur la mesure, puis l'onglet **Outils de mesure**) :
- `CA` et `Panier moyen` : nombre entier, séparateur de milliers activé.
- `% paiement mobile` et `Part du CA` : pourcentage, 0 décimale.

> 🗣️ **À savoir expliquer en entretien :** `DISTINCTCOUNT` compte les tickets *uniques*, car un ticket a plusieurs lignes (une par produit). `DIVIDE` évite une erreur si on divise par zéro.

## Étape 6 : les 4 indicateurs en haut (20 min)
Ajoute 4 visuels **Carte**, un par mesure : `CA`, `Nb tickets`, `Panier moyen`, `% paiement mobile`.

### ✅ Vérification : tu dois obtenir exactement ces chiffres (sans filtre)
| Mesure | Valeur attendue |
|---|---|
| CA | 38 633 700 FCFA |
| Nb tickets | 5 403 |
| Panier moyen | 7 150 FCFA |
| % paiement mobile | 47 % |

Si un chiffre est différent, vérifie les types de colonnes (étape 2) ou envoie-moi une capture.

---

# SOIRÉE 2 : graphiques, filtres et finitions

## Étape 7 : CA par mois (15 min)
Visuel **Graphique en courbes** :
- **Axe X :** `mois`
- **Axe Y :** `CA`

Titre : « Mars et décembre sont les meilleurs mois ».

## Étape 8 : CA par rayon (15 min)
Visuel **Graphique à barres groupées** (barres horizontales) :
- **Axe Y :** `categorie`
- **Axe X :** `CA`
- Trie par CA décroissant (les **…** du visuel → **Trier l'axe**).
- Active les **étiquettes de données**.

Titre : « L'Épicerie fait près de la moitié du CA ».

## Étape 9 : affluence jour × heure (20 min)
Visuel **Matrice** :
- **Lignes :** `jour_semaine`
- **Colonnes :** `heure_num`
- **Valeurs :** `Nb tickets`
- **Mise en forme** → **Éléments de cellule** → active **Couleur d'arrière-plan** (du blanc au bleu foncé).

Tu obtiens la même carte de chaleur que dans le script Python. Titre : « Pic d'affluence : vendredi et samedi, 17 h-20 h ».

## Étape 10 : top 10 des produits (15 min)
Visuel **Graphique à barres groupées** :
- **Axe Y :** `produit`, **Axe X :** `CA`
- Dans le volet **Filtres** de ce visuel : `produit` → **Type de filtre : N premiers** → **Afficher les éléments : Haut, 10** → **Par valeur : CA** → **Appliquer le filtre**.

## Étape 11 : les filtres (segments) (15 min)
Ajoute 4 visuels **Segment** : `mois`, `categorie`, `mode_paiement`, `client_fidele`.

🧪 **Teste-les :** clique sur « Mars » et regarde tous les chiffres changer. C'est ça, l'intérêt d'un dashboard par rapport à un graphique fixe.

## Étape 12 : finitions (20 min)
- **Titre de la page** (zone de texte) : « Ventes 2025 : hypermarché à Dakar (données simulées) ».
- Aligne les visuels (**Format** → **Aligner**) et laisse de l'espace entre eux.
- Pas plus de 2 couleurs principales : bleu pour les données, orange pour mettre en avant.
- Renomme la page en bas : « Vue d'ensemble ».

## Étape 13 : enregistrer et exporter pour GitHub (15 min)
1. **Fichier** → **Enregistrer sous** → `powerbi/dashboard_ventes.pbix`.
2. **Fichier** → **Exporter** → **Exporter au format PDF** → `powerbi/dashboard_ventes.pdf`.
3. Fais une capture d'écran du dashboard (touches **Windows + Maj + S**) et enregistre-la dans `images/dashboard_powerbi.png`.

---

## ⭐ Étape bonus : flèches d'évolution par rapport au mois précédent (1 h 30)

> **Ne la fais qu'une fois les étapes 1 à 13 terminées.** Un dashboard simple et fini vaut mieux
> qu'un dashboard ambitieux et cassé la veille du salon.

**Le but :** quand on clique sur « Mars », une carte affiche **▲ 25,9 %** en vert (hausse par rapport à février).
C'est ce qu'on appelle l'**intelligence temporelle** (*time intelligence*), une compétence très demandée.

### B1. Créer une table de dates
Les fonctions de temps de Power BI ont besoin d'une table qui contient **tous** les jours de l'année.

**Modélisation** → **Nouvelle table**, puis colle :

```DAX
Dates =
ADDCOLUMNS(
    CALENDAR(DATE(2025, 1, 1), DATE(2025, 12, 31)),
    "Mois num", MONTH([Date]),
    "Mois", SWITCH(MONTH([Date]),
        1, "Janv", 2, "Févr", 3, "Mars", 4, "Avr", 5, "Mai", 6, "Juin",
        7, "Juil", 8, "Août", 9, "Sept", 10, "Oct", 11, "Nov", 12, "Déc")
)
```

Ensuite :
1. Sélectionne la table `Dates` → **Outils de table** → **Marquer comme table de dates** → colonne `Date`.
2. Trie la colonne `Dates[Mois]` par `Dates[Mois num]` (comme à l'étape 4).

### B2. Relier la table de dates aux ventes
1. Vue **Modèle** (3e icône à gauche).
2. Fais glisser `Dates[Date]` sur `ventes_propres[date]`.
3. Vérifie la relation : **Un à plusieurs (1:*)**, direction **Unique**, de `Dates` vers `ventes_propres`.

### B3. ⚠️ Utiliser le mois de la table Dates
Le filtre doit maintenant venir de la table `Dates`, sinon l'évolution ne fonctionne pas :
- Dans le **segment** des mois, remplace `ventes_propres[mois]` par `Dates[Mois]`.
- Dans la **courbe** du CA par mois, remplace l'axe X par `Dates[Mois]`.

### B4. Les 3 mesures
```DAX
CA mois précédent =
CALCULATE([CA], DATEADD(Dates[Date], -1, MONTH))
```
```DAX
Évolution vs mois précédent =
DIVIDE([CA] - [CA mois précédent], [CA mois précédent])
```
```DAX
Évolution (affichage) =
VAR e = [Évolution vs mois précédent]
RETURN
    IF(
        NOT HASONEVALUE(Dates[Mois]) || ISBLANK(e),
        "Choisis un mois",
        IF(e >= 0, "▲ ", "▼ ") & FORMAT(ABS(e), "0.0%")
    )
```

> 🗣️ **À savoir expliquer :** `DATEADD(…, -1, MONTH)` décale la période d'un mois en arrière.
> `HASONEVALUE` vérifie qu'un seul mois est sélectionné : sans ça, comparer « toute l'année »
> au « mois précédent » n'a pas de sens. Janvier n'a pas de mois précédent dans les données, donc il affiche aussi « Choisis un mois ».

### B5. La carte avec couleur verte ou rouge
1. Ajoute un visuel **Carte** avec la mesure `Évolution (affichage)`, à côté de la carte « CA ».
2. **Mise en forme** → **Valeur de légende** (ou **Valeur** selon la version) → **Couleur** → bouton **fx**.
3. **Style de mise en forme : Règles**, basé sur `Évolution vs mois précédent` :
   - si la valeur est **≥ 0** → vert `#0ca30c`
   - si la valeur est **< 0** → rouge `#d03b3b`

### ✅ Vérification (clique sur chaque mois dans le segment)
| Mois sélectionné | Affichage attendu |
|---|---|
| Janv | Choisis un mois (pas de mois précédent) |
| Mars | ▲ 25.9% (vert) |
| Avr | ▼ 28.5% (rouge) |
| Août | ▼ 13.9% (rouge) |
| Déc | ▲ 26.5% (vert) |

*(Le séparateur décimal peut être un point ou une virgule selon les paramètres de ton ordinateur.)*

**À ajouter dans la section Power BI du README :**
`- Intelligence temporelle : table de dates, DATEADD, évolution mensuelle avec mise en forme conditionnelle`

---

## Étape 14 : ajouter le dashboard au README

Colle cette section dans `README.md`, juste avant « 🛠️ Outils et compétences » :

```markdown
## 📈 Tableau de bord Power BI

Pour rendre l'analyse utilisable par un directeur de magasin, j'ai construit un tableau de bord
interactif : 4 indicateurs clés, 4 graphiques et 4 filtres (mois, rayon, paiement, fidélité).

![Dashboard Power BI](images/dashboard_powerbi.png)

- Fichier : [`powerbi/dashboard_ventes.pbix`](powerbi/dashboard_ventes.pbix) (à ouvrir avec Power BI Desktop)
- Version PDF : [`powerbi/dashboard_ventes.pdf`](powerbi/dashboard_ventes.pdf)
- Mesures DAX : CA, Nb tickets (DISTINCTCOUNT), Panier moyen, % paiement mobile, Part du CA
```

Et dans la liste des outils, ajoute :
`- **Power BI** : mesures DAX, matrice avec mise en forme conditionnelle, segments, filtre Top N`

---

## 🗣️ Ce que tu pourras dire au salon

> « J'ai nettoyé les données avec Python, puis je les ai mises dans un tableau de bord Power BI.
> Un directeur de magasin peut filtrer par mois ou par rayon et voir tout de suite son CA,
> son panier moyen et les heures de pointe. »

**Démonstration conseillée :** ouvre le dashboard sur ton ordinateur (ou montre le PDF sur ton téléphone), clique sur « Mars » ou sur « Boucherie », et montre comment les chiffres changent.
