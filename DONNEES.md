# Données : ventes d'un hypermarché fictif à Dakar (2025)

> ⚠️ **Données simulées.** Produits, prix (approximatifs, en FCFA), clients et tickets sont inventés
> avec le script `generer_donnees.py`. Elles ne représentent aucune enseigne réelle.

- **Période :** 1er janvier au 31 décembre 2025
- **Taille :** environ 17 600 lignes de vente (une ligne = un produit dans un ticket de caisse), environ 5 400 tickets
- **Fichier :** `ventes.csv` (UTF-8, séparateur virgule)

## Dictionnaire des colonnes

| Colonne | Description |
|---|---|
| `id_ticket` | Numéro du ticket de caisse (plusieurs lignes par ticket) |
| `date` | Date de l'achat |
| `heure` | Heure de l'achat (HH:MM) |
| `id_produit` | Code produit |
| `produit` | Nom du produit |
| `categorie` | Rayon (Épicerie, Boissons, Boucherie…) |
| `quantite` | Nombre d'unités achetées |
| `prix_unitaire_fcfa` | Prix d'une unité en FCFA |
| `montant_fcfa` | quantite × prix_unitaire_fcfa |
| `mode_paiement` | Espèces, Wave, Orange Money, Carte bancaire |
| `id_client` | Numéro de carte de fidélité (vide si le client n'a pas de carte) |
| `caisse` | Numéro de la caisse (1 à 8) |

## Particularités intégrées à la simulation

- Plus d'affluence le vendredi et le samedi, et en fin et début de mois.
- Périodes spéciales : Ramadan et Korité (mars), Tabaski (fin mai et début juin), rentrée scolaire (fin septembre et octobre), fêtes de fin d'année.
- Saison des mangues (avril à juillet) et hausse des boissons pendant les mois chauds.

## Nettoyage

Le fichier contient volontairement des erreurs, comme un vrai export de caisse :
doublons, valeurs manquantes, catégories mal orthographiées, formats de date différents,
quantités aberrantes et espaces parasites. À toi de les trouver et de les corriger.
