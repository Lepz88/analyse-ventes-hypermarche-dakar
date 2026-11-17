# 🎤 Préparation entretien : projet Teranga Pay

> ⚠️ Fichier PERSONNEL : il est exclu de GitHub via `.gitignore`.
> Méthode : lis la question, réponds **à voix haute sans regarder**, puis compare avec la réponse.
> Les réponses ci-dessous sont des modèles : **reformule-les avec tes mots**.

---

## 🧩 Le projet en 90 secondes (« Parlez-moi de votre projet »)
_À rédiger toi-même à la fin du projet, avec la structure Problème → Ce que j'ai fait → Résultat chiffré → Recommandation._

---

## Questions sur les données

**Q1. Pourquoi des données simulées ?**
> Les vraies données Mobile Money sont confidentielles. J'ai construit un simulateur qui reproduit la structure d'un réseau sénégalais : 14 régions, milieu urbain et rural, saisonnalité locale, ruptures de liquidité. Je le présente toujours clairement comme des données simulées.

**Q2. Pourquoi les colonnes `cache_` ne sont-elles pas exportées ?**
> Mon générateur crée des variables cachées qui décident quels agents vont partir. Je ne les exporte pas : mon analyse doit retrouver, à partir des seules données disponibles, quels agents sont actifs, à risque ou partis, et surtout pourquoi ils partent. C'est comme dans une vraie entreprise : personne ne te donne une colonne « cet agent va partir ».

**Q3. Pourquoi une graine fixe (`seed = 42`) et une date de référence fixe ?**
> Pour la reproductibilité : n'importe qui obtient exactement les mêmes chiffres, à n'importe quelle date. Avec `CURRENT_DATE`, les résultats changeraient chaque jour.

## Questions techniques

**Q4. Pourquoi un schéma `staging` et un schéma `analytics` ?**
> Le staging reçoit les données brutes sans contrainte, pour pouvoir y repérer les erreurs. L'analytics contient les données propres en modèle en étoile, avec clés primaires et étrangères, prêt pour l'analyse et Power BI.

**Q5. C'est quoi un modèle en étoile ?**
> Une table de faits au centre (les transactions : ce qui se passe, avec les montants) reliée à des tables de dimensions (agent, client, région, date : qui, où, quand). C'est le format standard pour Power BI.

**Q6. Quelles anomalies as-tu nettoyées ?**
> Des doublons (2 890), des montants manquants (1 435) et négatifs (720), des types de transaction en majuscules et 22 régions mal écrites (« THIES », « St Louis »). Les lignes écartées sont tracées dans une table de rejets, avec le motif.

**Q7. Raconte une difficulté que tu as résolue.**
> En comparant mes résultats entre deux machines, j'ai remarqué un petit écart. J'ai découvert que 16 transactions en double avaient des copies contradictoires : une avec un montant valide, l'autre sans. Mon dédoublonnage gardait une copie au hasard. J'ai écrit une règle déterministe qui garde la version valide, et ajouté un contrôle qualité.

**Q8. Comment fonctionne `LEFT JOIN … WHERE … IS NULL` ?**
> Le LEFT JOIN garde tous les agents, même ceux sans transaction correspondante. Pour ceux-là, les colonnes de la table transactions sont vides (NULL). Le filtre `IS NULL` isole donc les agents sans aucune transaction sur la période : les inactifs.

## Questions business

**Q9. Quel est le mois le plus actif, et pourquoi ?**
> Mai, à cause de la Tabaski. Je l'ai prouvé en comparant les moyennes par jour : 49,2 M FCFA par jour pendant la fête, contre 29,6 M FCFA le reste de l'année (×1,7). La part des transferts passe de 23,9 % à 36,5 %, et le montant moyen augmente aussi.

**Q10. Pourquoi diviser par le nombre de jours dans la comparaison Tabaski ?**
> La période de la Tabaski dure environ 13 jours, le reste de l'année plus de 350. Comparer des totaux n'aurait aucun sens : il faut comparer à base égale.

**Q11. Qu'est-ce que l'entreprise doit faire de cet insight ?**
> Renforcer la liquidité des agents avant la fête. Sinon, ils tombent en rupture de cash au moment où la demande est la plus forte, et les clients vont voir la concurrence.

## Questions sur l'analyse du churn (Sprint 2)

**Q12. Pourquoi séparer « Jamais activé » et « Churn » ?**
> Ce ne sont pas les mêmes problèmes. Un agent jamais activé révèle un problème de recrutement ou de démarrage, et il peut encore être activé. Un agent en churn révèle un problème de fidélisation : il générait du volume qu'on a perdu. Les actions sont différentes, et les mélanger fausserait le taux de churn (30 % au lieu de 26 %).

**Q13. Peut-on comparer le taux de churn de Kédougou à celui de Dakar ?**
> Pas directement. Kédougou n'a que 8 agents actives : un seul départ de plus ferait varier son taux de 12,5 points. Dakar en a 234. Je présente toujours le taux avec l'effectif, et je regroupe les petites régions (par zone d'éloignement) ou je filtre avec HAVING avant de conclure.

**Q14. Quel est le principal facteur de churn que tu as trouvé ?**
> Les ruptures de liquidité. Les agents qui en subissent 2 ou plus par mois partent 4,1 fois plus que les autres. Et ces ruptures sont 6,2 fois plus fréquentes dans les zones rurales éloignées. J'ai testé mon hypothèse en deux maillons, en comparant à base égale (ruptures par mois d'activité). Je reste prudent : c'est une forte association, et avec de vraies données, je la confirmerais par un test terrain.

**Q15. Quelle est la différence entre WHERE et HAVING ?**
> WHERE filtre les lignes avant le regroupement (ex : retirer les agents jamais activés). HAVING filtre les groupes après le regroupement (ex : garder les régions d'au moins 30 agents).

**Q16. Pourquoi « plus d'agents » n'explique-t-il pas un taux de churn plus faible ?**
> Le nombre d'agents mesure la taille d'un groupe, pas sa santé. Avec deux chiffres, on ne peut pas établir de règle, et un contre-exemple la casse : Diourbel (81 agents) et Ziguinchor (39 agents) ont le même taux, environ 31 %. Corrélation n'est pas causalité.

**Q17. Comment calcules-tu une variation en pourcentage ? Et un « combien de fois plus » ?**
> Pour une variation, je divise l'écart par la valeur de départ : (nouvelle − ancienne) ÷ ancienne. Par exemple, un agent qui passe de 34 à 13 transactions perd 62 %. Pour un « combien de fois plus », je divise le groupe comparé par le groupe de référence : 54,5 % ÷ 13,3 % = 4,1 fois plus. Le réflexe, c'est de toujours se demander quelle est la référence : c'est elle qu'on met en bas.

**Q18. Quelle différence entre NULL et 0 ?**
> NULL veut dire « pas d'information », 0 veut dire « zéro mesuré ». Par exemple, LAG renvoie NULL pour octobre 2025 parce que mes données commencent ce mois-là, pas parce que l'agent n'avait fait aucune transaction en septembre.

**Q19. Comment sais-tu dans quel ordre une requête trie ses résultats ? (cas de la liste d'agents à appeler)**
> Je lis le ORDER BY. Dans ma liste, le tri se fait d'abord par priorité, puis par nombre de ruptures sur 90 jours en ordre décroissant (DESC), puis par activité. L'agent TP-AG-00640 de Kolda est en tête parce qu'il a 16 ruptures de cash en 90 jours, pas à cause de son milieu ou de son type de point. Réflexe : pour l'ordre, je lis le ORDER BY ; pour savoir pourquoi une ligne est présente, je lis le WHERE.

**Q20. Quelle action recommandes-tu pour un agent en forte baisse d'activité ?**
> Une action qui répond à la cause visible dans les données : donnée → cause → action. Pour TP-AG-00640 (Kolda, rural, 16 ruptures en 90 jours, activité à 49 % de l'habitude), le problème est la liquidité. Je propose de l'appeler cette semaine, d'organiser un réapprovisionnement rapide, puis un fonds de roulement plus élevé ou un rattachement à un point de recharge proche, avec l'objectif de passer sous 1 rupture par mois. Changer son type de point ne serait ni réaliste ni lié aux données.

**Q21. Ton signal de détection est-il fiable ?**
> Testé sur le passé (backtest au 30/06/2026), les agents en forte baisse sont partis à 80 % contre 6,3 % pour les stables (×12,7). Mais ce groupe ne compte que 10 agents : je retiens l'ordre de grandeur, pas le chiffre exact. La baisse modérée donne ×2,8 sur 56 agents. Et le signal ne repère qu'environ 1 départ sur 3 : c'est un outil utile, pas magique.

**Q22. Les agents recrutés récemment partent-ils plus ?**
> Par cohorte trimestrielle, aucune tendance claire : les taux varient entre 20 et 39 % avec de petits groupes, et la dernière cohorte (0 %) n'a pas eu le temps de partir, c'est un biais de censure. À exposition égale, sur les 6 premiers mois, les nouveaux partent 1,6 fois plus, mais sur 58 agents seulement : c'est une tendance, bien plus faible que l'effet de la liquidité (×4,1). Une hypothèse non confirmée est aussi un résultat utile.

**Q23. Combien le churn coûte-t-il au réseau ?**
> Les 208 agents partis faisaient passer 164 M FCFA par mois, soit environ 20 % du volume actuel du réseau. J'ai calculé le volume mensuel de chaque agent sur sa période d'activité, pour comparer à base égale. 60 % de cette perte vient d'agents qui avaient au moins une rupture de cash par mois. Et 78 M FCFA par mois sont encore en jeu chez les 73 agents qui ralentissent.

**Q24. Les agents qui partent sont-ils des gros ou des petits agents ?**
> Des petits : 0,79 M FCFA par mois en moyenne, deux fois moins que les agents actifs (1,58 M). Ils gagnent donc moins de commissions et ont moins de raisons de rester face aux difficultés. Attention à ne pas confondre le nombre d'agents (combien ils sont) et le volume par agent (la taille de chacun).

**Q25. Si tu ne pouvais financer qu'une seule action, laquelle ?**
> La liquidité : réapprovisionner plus vite les agents qui ont au moins une rupture par mois. Ce groupe représente 60 % du volume perdu (98 M FCFA par mois), et on connaît la cause, donc on sait quoi faire. Pour les autres agents partis, la cause reste inconnue : c'est une piste à creuser.

**Q26. Ta phrase d'impact (CV / LinkedIn)**
> « Analyse du churn d'un réseau Mobile Money simulé de 800 agents (SQL, PostgreSQL) : identification des ruptures de liquidité comme premier facteur de départ (×4,1), chiffrage de la perte à 164 M FCFA par mois (20 % du volume), et création d'un signal d'alerte précoce ciblant 73 agents à risque représentant 78 M FCFA par mois. »

**Q27. Tu as déjà fait des graphiques avec Python : pourquoi Power BI en plus ?**
> Python m'a servi à analyser et à illustrer mes découvertes dans le rapport : ce sont des images fixes. Power BI sert à livrer un outil interactif que le directeur peut utiliser lui-même chaque semaine, filtrer par région ou par mois, pour suivre le churn et savoir quels agents appeler, sans écrire de code.

**Q28. Pourquoi n'as-tu pas analysé le churn des clients ?**
> J'ai volontairement concentré l'analyse sur les agents, parce qu'un agent qui part fait perdre tous ses clients d'un coup : c'est le levier le plus important. L'analyse du churn des clients est ma prochaine étape, les données sont déjà prêtes dans ma base (12 000 clients).

**Q29. Ton dashboard affiche 27,1 % de churn, ton rapport 26 %. Lequel est juste ?**
> Les deux, mais ils ne répondent pas à la même question. 26 % = 208 agents partis sur les 800 recrutés : c'est la répartition des statuts. 27,1 % = 208 sur les 768 agents qui ont été actifs : c'est le vrai taux de churn, puisqu'un agent qui n'a jamais démarré ne peut pas partir. La différence vient de la référence, pas d'un arrondi.

**Q30. Pourquoi avoir fait certains calculs en SQL plutôt qu'en DAX ?**
> Les calculs complexes par agent (volume mensuel, ruptures par mois, signal faible) étaient déjà écrits et vérifiés en SQL au Sprint 2. Je les ai rassemblés dans une vue PostgreSQL, et Power BI ne fait qu'afficher. C'est plus simple, plus fiable, et les mêmes chiffres servent partout (SQL, Python, Power BI). En DAX, je n'ai gardé que des mesures simples : compter, filtrer, diviser.

**Q31. Comment as-tu conçu le design de ton dashboard ?**
> J'ai suivi quelques règles simples : peu de couleurs (bleu pour l'information, orange pour le problème), un fond gris clair avec des cases blanches, tout aligné avec les mêmes espaces, les chiffres clés en haut et des titres qui donnent la conclusion. J'ai aussi créé un thème de couleurs commun à mes graphiques Python et à Power BI, pour que tout le projet soit cohérent.

**Q32. Présente-moi ton dashboard Power BI.**
> Il a deux pages. La page « Vue d'ensemble » est pour le directeur : quatre chiffres clés en haut (27,1 % de churn, 164 M FCFA perdus par mois, 9 agents à appeler, 548 agents actifs), trois graphiques dont les titres donnent la conclusion (le churn monte avec les ruptures de cash, il est plus élevé loin de Dakar, et 2,3 fois plus élevé en rural), et des filtres par région, milieu et type de point. La page « Agents à appeler » est pour l'équipe terrain : la liste des 73 agents qui ralentissent, avec les 9 prioritaires en haut.

**Q33. Comment as-tu vérifié que ton dashboard est juste ?**
> J'ai comparé ses chiffres avec mes requêtes SQL : 27,1 % de churn, 45 % à Kolda avec le filtre, 17,1 % en urbain, et les 9 mêmes agents à appeler que dans mon SQL. SQL, Python et Power BI donnent les mêmes résultats, parce que les calculs complexes sont faits une seule fois, dans une vue PostgreSQL.

**Q34. Pourquoi des info-bulles avec le nombre d'agents ?**
> Pour que le lecteur puisse juger la fiabilité d'un taux sans surcharger le graphique. Par exemple, Kédougou n'a que 8 agents : en survolant la barre, on voit tout de suite que son taux est moins fiable que celui de Dakar, qui en a 234.

**Q35. Comment colores-tu automatiquement les régions les plus touchées ?**
> Avec la mise en forme conditionnelle : une règle qui met en orange les barres dont le taux de churn est supérieur ou égal à 40 %. Si les données changent, les couleurs suivent toutes seules. Attention : le taux est stocké entre 0 et 1, donc la règle s'écrit 0,4 et non 40.

**Q36. Comment as-tu publié ton projet ? Tu connais Git ?**
> Oui. J'ai créé un dépôt sur GitHub, puis j'ai utilisé git init, git add, git commit et git push depuis le terminal de VS Code. Avant d'envoyer, je vérifie avec git status que mes fichiers privés et les gros CSV sont bien exclus grâce au .gitignore. Pour les mises à jour, je fais git pull, puis add, commit et push, avec un message qui dit ce qui a changé.

**Q37. Raconte un problème technique que tu as résolu seul.**
> Après la publication, mon README s'affichait en un seul paragraphe sur GitHub. Avec la commande git ls-files --eol, j'ai vu que Git ne le reconnaissait pas comme du texte : il était enregistré dans un mauvais encodage. Je l'ai remplacé par une version en UTF-8, vérifié l'encodage dans VS Code, puis renvoyé. Depuis, je modifie toujours mes fichiers dans VS Code et je vérifie le rendu avant de publier.

**Q38. « Présentez-moi un de vos projets » : le pitch du projet (60 secondes)**
> *Brouillon rédigé le 31/10, à reformuler avec mes mots et à répéter à voix haute.*
>
> J'ai réalisé un projet sur le churn des agents Mobile Money au Sénégal. Un agent, c'est une boutique ou un kiosque qui permet aux clients de déposer et de retirer de l'argent. Quand il arrête, toute une zone perd son point d'accès, surtout en milieu rural.
>
> Comme les vraies données sont confidentielles, j'ai simulé un réseau fictif : 800 agents et 576 000 transactions sur 12 mois. J'ai construit toute la chaîne : une base PostgreSQL, l'analyse en SQL, des graphiques en Python et un dashboard Power BI.
>
> Le résultat principal : les agents qui manquent souvent de cash partent 4 fois plus que les autres. Au total, le churn fait perdre environ 164 millions de FCFA par mois, soit 20 % du volume du réseau. J'ai aussi créé un signal d'alerte qui repère à l'avance les agents qui ralentissent : 9 agents à appeler en priorité.
>
> Ma recommandation : réapprovisionner en cash les agents dès leur première rupture du mois, en priorité en zone rurale.
>
> Ce projet m'a appris que derrière chaque requête, il y a une décision à prendre.

**Conseils pour le dire :** parler lentement ; retenir les 4 chiffres clés (800 agents, ×4, 164 M FCFA / 20 %, 9 agents) plutôt que le texte mot à mot ; finir en regardant le recruteur ; si on me demande des détails, j'ai Q14 (facteur principal), Q23 (coût), Q21 (signal), Q33 (vérification).

**Q39. Sur ton CV : « signal d'alerte précoce… 73 agents… 78 M FCFA ». Ça veut dire quoi ?**
> Un agent qui va partir ralentit d'abord. Je compare ses 30 derniers jours à son habitude. J'ai testé l'idée sur le passé : les agents en forte baisse sont partis 12 fois plus. Aujourd'hui, ça donne 9 agents à appeler en priorité et 64 à surveiller.

**À retenir par cœur :** l'idée (il ralentit avant de partir) ; la preuve (testé sur le passé, ×12,7) ; l'action (9 à appeler, 64 à surveiller = 73).

**S'il demande « Et les 78 millions ? »**
> C'est le volume mensuel de ces 73 agents. On risque de le perdre s'ils partent, mais ils ne partiront pas tous.

**S'il demande « Quelles sont les limites ? »**
> Le test repose sur peu d'agents, et le signal repère environ 1 départ sur 3. C'est un complément, pas une solution complète.

*Pour les détails (seulement si on me les demande) :* seuils < 50 % = appeler, 50–80 % = surveiller ; backtest au 30/06/2026 : forte baisse 8 partis sur 10 (80 %), stables 32 sur 509 (6,3 %) ; 78,1 M = 9,0 M (les 9 prioritaires) + 69,1 M (les 64 à surveiller). Voir aussi Q21.

---
_Nouvelles questions ajoutées à chaque sprint._"""
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
