"""Définition des 9 Boss de fin d'acte – SQLemon."""

BOSS = [
    # ── Acte 1 ─ Arène de Bourg Palette ──────────────────────────────────────
    {
        "acte": 1,
        "zone": "Arène de Bourg Palette",
        "titre": "Champion Régis",
        "contexte": "Le Champion Régis te défie ! Seuls les Pokémon les plus puissants peuvent t'aider.",
        "description": (
            "Trouve tous les Pokémon dont le score total\n"
            "(pv + attaque + defense + vitesse) est supérieur à 300.\n"
            "Affiche leur nom et leur score total,\n"
            "trié par score décroissant."
        ),
        "indice": (
            "Crée un alias score_total dans le SELECT, "
            "puis réutilise le calcul dans WHERE. "
            "ORDER BY score_total DESC."
        ),
        "solution": (
            "SELECT nom, (pv + attaque + defense + vitesse) AS score_total "
            "FROM pokemon "
            "WHERE (pv + attaque + defense + vitesse) > 300 "
            "ORDER BY score_total DESC"
        ),
        "compare": "aggregate",
    },

    # ── Acte 2 ─ Arène d'Argenta ──────────────────────────────────────────────
    {
        "acte": 2,
        "zone": "Arène d'Argenta",
        "titre": "Champion Pierre",
        "contexte": "Pierre utilise des Pokémon Roche et Sol. Montre-lui que tu maîtrises les statistiques !",
        "description": (
            "Affiche pour chaque type (Roche, Sol)\n"
            "le nombre de Pokémon, leur PV moyen arrondi\n"
            "et leur attaque moyenne arrondie.\n"
            "Groupe par type."
        ),
        "indice": (
            "WHERE type1 IN ('Roche', 'Sol'). "
            "COUNT(*), ROUND(AVG(pv)), ROUND(AVG(attaque)). "
            "GROUP BY type1."
        ),
        "solution": (
            "SELECT type1, COUNT(*) AS nb, "
            "ROUND(AVG(pv)) AS pv_moyen, ROUND(AVG(attaque)) AS att_moyenne "
            "FROM pokemon "
            "WHERE type1 IN ('Roche', 'Sol') "
            "GROUP BY type1"
        ),
        "compare": "full",
    },

    # ── Acte 3 ─ Mont Sélénite ────────────────────────────────────────────────
    {
        "acte": 3,
        "zone": "Mont Sélénite",
        "titre": "Team Rocket",
        "contexte": "Les Rockets bloquent la sortie ! Prouve ta maîtrise des jointures et de l'INTERSECT.",
        "description": (
            "Trouve les Pokémon qui connaissent\n"
            "à la fois une capacité Physique\n"
            "ET une capacité Spéciale.\n"
            "Affiche leur nom et le nombre total\n"
            "de capacités qu'ils connaissent."
        ),
        "indice": (
            "Utilise INTERSECT pour trouver les IDs communs aux deux catégories. "
            "Ensuite JOIN pokemon_capacites pour compter toutes leurs capacités. "
            "GROUP BY p.id, p.nom ORDER BY p.nom."
        ),
        "solution": (
            "SELECT p.nom, COUNT(pc.capacite_id) AS nb_capacites "
            "FROM pokemon p "
            "JOIN pokemon_capacites pc ON p.id = pc.pokemon_id "
            "WHERE p.id IN ( "
            "  SELECT pokemon_id FROM pokemon_capacites pc1 "
            "  JOIN capacites c ON pc1.capacite_id = c.id WHERE c.categorie = 'Physique' "
            "  INTERSECT "
            "  SELECT pokemon_id FROM pokemon_capacites pc2 "
            "  JOIN capacites c ON pc2.capacite_id = c.id WHERE c.categorie = 'Spéciale' "
            ") "
            "GROUP BY p.id, p.nom "
            "ORDER BY p.nom"
        ),
        "compare": "aggregate",
    },

    # ── Acte 4 ─ Arène de Céladopole ─────────────────────────────────────────
    {
        "acte": 4,
        "zone": "Arène de Céladopole",
        "titre": "Championne Ondine",
        "contexte": "Ondine et ses Pokémon Eau ! Montre que tu maîtrises les sous-requêtes corrélées.",
        "description": (
            "Pour chaque type1, affiche le nom du Pokémon\n"
            "avec la vitesse la plus élevée,\n"
            "son type1 et sa vitesse.\n"
            "Utilise une sous-requête corrélée."
        ),
        "indice": (
            "WHERE p.vitesse = (SELECT MAX(p2.vitesse) FROM pokemon p2 WHERE p2.type1 = p.type1). "
            "ORDER BY p.type1."
        ),
        "solution": (
            "SELECT p.type1, p.nom, p.vitesse "
            "FROM pokemon p "
            "WHERE p.vitesse = (SELECT MAX(p2.vitesse) FROM pokemon p2 WHERE p2.type1 = p.type1) "
            "ORDER BY p.type1"
        ),
        "compare": "full",
    },

    # ── Acte 5 ─ Tour Lavanville ──────────────────────────────────────────────
    {
        "acte": 5,
        "zone": "Tour Lavanville",
        "titre": "Esprits de Lavanville",
        "contexte": "Les esprits réclament une offrande de connaissance. Qui sont les types les plus forts ?",
        "description": (
            "Trouve les 3 types (type1) qui ont\n"
            "la moyenne de stats totales\n"
            "(pv + attaque + defense + vitesse)\n"
            "la plus élevée.\n"
            "Affiche le type et la moyenne arrondie."
        ),
        "indice": (
            "AVG(pv + attaque + defense + vitesse) AS moy_total. "
            "GROUP BY type1. ORDER BY moy_total DESC. LIMIT 3."
        ),
        "solution": (
            "SELECT type1, ROUND(AVG(pv + attaque + defense + vitesse)) AS moy_total "
            "FROM pokemon "
            "GROUP BY type1 "
            "ORDER BY moy_total DESC "
            "LIMIT 3"
        ),
        "compare": "first_col",
    },

    # ── Acte 6 ─ Silph Co. ────────────────────────────────────────────────────
    {
        "acte": 6,
        "zone": "Silph Co.",
        "titre": "Giovanni",
        "contexte": "Giovanni et sa Team Rocket ! Seuls les bi-types d'élite peuvent y faire face.",
        "description": (
            "Trouve tous les Pokémon bi-types\n"
            "(type2 non null) dont l'attaque\n"
            "est supérieure à la moyenne d'attaque\n"
            "des Pokémon mono-types.\n"
            "Affiche nom, type1, type2, attaque."
        ),
        "indice": (
            "Sous-requête : SELECT AVG(attaque) FROM pokemon WHERE type2 IS NULL. "
            "Filtre WHERE type2 IS NOT NULL AND attaque > (...). "
            "ORDER BY attaque DESC."
        ),
        "solution": (
            "SELECT nom, type1, type2, attaque "
            "FROM pokemon "
            "WHERE type2 IS NOT NULL "
            "AND attaque > (SELECT AVG(attaque) FROM pokemon WHERE type2 IS NULL) "
            "ORDER BY attaque DESC"
        ),
        "compare": "names",
    },

    # ── Acte 7 ─ Arène de Cramois'île ────────────────────────────────────────
    {
        "acte": 7,
        "zone": "Arène de Cramois'île",
        "titre": "Champion Théo",
        "contexte": "Théo et ses Pokémon Feu ! Classe tous les Pokémon selon leur écart à la moyenne de leur type.",
        "description": (
            "Affiche le classement de tous les Pokémon\n"
            "par rapport à la moyenne d'attaque de leur type1 :\n"
            "nom, type1, attaque, moy_type (entière),\n"
            "écart à la moyenne.\n"
            "Trié par écart décroissant."
        ),
        "indice": (
            "JOIN pokemon p2 ON p.type1 = p2.type1. GROUP BY p.id. "
            "moy_type = SUM(p2.attaque) / COUNT(p2.id)  (division entière). "
            "ecart = p.attaque - moy_type."
        ),
        "solution": (
            "SELECT p.nom, p.type1, p.attaque, "
            "SUM(p2.attaque) / COUNT(p2.id) AS moy_type, "
            "(p.attaque - SUM(p2.attaque) / COUNT(p2.id)) AS ecart "
            "FROM pokemon p "
            "JOIN pokemon p2 ON p.type1 = p2.type1 "
            "GROUP BY p.id, p.nom, p.type1, p.attaque "
            "ORDER BY ecart DESC"
        ),
        "compare": "full",
    },

    # ── Acte 8 ─ Arène d'Azuria ───────────────────────────────────────────────
    {
        "acte": 8,
        "zone": "Arène d'Azuria",
        "titre": "Ondine — Revanche",
        "contexte": "Ondine revient plus forte ! Qui peut surpasser le meilleur Pokémon Eau ?",
        "description": (
            "Trouve les Pokémon dont le score total\n"
            "(pv + attaque + defense + vitesse)\n"
            "est strictement supérieur au maximum\n"
            "de score total de TOUS les Pokémon Eau.\n"
            "Affiche nom et score total."
        ),
        "indice": (
            "Sous-requête : SELECT MAX(pv+attaque+defense+vitesse) "
            "FROM pokemon WHERE type1 = 'Eau'. "
            "WHERE score > (...). ORDER BY score_total DESC."
        ),
        "solution": (
            "SELECT nom, (pv + attaque + defense + vitesse) AS score_total "
            "FROM pokemon "
            "WHERE (pv + attaque + defense + vitesse) > "
            "(SELECT MAX(pv + attaque + defense + vitesse) FROM pokemon WHERE type1 = 'Eau') "
            "ORDER BY score_total DESC"
        ),
        "compare": "aggregate",
    },

    # ── Acte 9 ─ Plateau Indigo ───────────────────────────────────────────────
    {
        "acte": 9,
        "zone": "Plateau Indigo",
        "titre": "La Ligue Pokémon",
        "contexte": "La Ligue complète t'attend ! Produis le rapport final de Kanto.",
        "description": (
            "Pour chaque type1, affiche :\n"
            "le nombre de Pokémon, le meilleur score total,\n"
            "le Pokémon champion (meilleur score du type),\n"
            "et si ce type a un légendaire (oui/non).\n"
            "Trié par meilleur score décroissant."
        ),
        "indice": (
            "Sous-requête corrélée pour champion : "
            "(SELECT nom FROM pokemon p2 WHERE p2.type1 = p.type1 "
            "ORDER BY pv+attaque+defense+vitesse DESC LIMIT 1). "
            "CASE WHEN MAX(est_legendaire)=1 THEN 'oui' ELSE 'non' END. "
            "GROUP BY type1."
        ),
        "solution": (
            "SELECT p.type1, COUNT(*) AS nb_pokemon, "
            "MAX(p.pv + p.attaque + p.defense + p.vitesse) AS meilleur_score, "
            "(SELECT p2.nom FROM pokemon p2 WHERE p2.type1 = p.type1 "
            " ORDER BY p2.pv + p2.attaque + p2.defense + p2.vitesse DESC LIMIT 1) AS champion, "
            "CASE WHEN MAX(p.est_legendaire) = 1 THEN 'oui' ELSE 'non' END AS legendaire "
            "FROM pokemon p "
            "GROUP BY p.type1 "
            "ORDER BY meilleur_score DESC"
        ),
        "compare": "full",
    },
]
