"""SQLemon – 35 quêtes progressives, Kanto Gen 1."""

QUESTS = [

    # ══════════════════════════════════════════════════════════════════════
    # ACTE 1 — Bourg Palette  (Q1-Q3)  SELECT basique
    # ══════════════════════════════════════════════════════════════════════
    {
        "numero": 1,
        "pokemon_id": None,
        "acte": 1,
        "zone": "Bourg Palette",
        "titre": "L'inventaire du Professeur",
        "contexte": "Prof. Chen : Avant de te laisser partir, j'ai besoin d'un inventaire complet de la base de données de Kanto.",
        "description": (
            "Affiche <strong>tous</strong> les Pokémon enregistrés dans la base de données.\n"
            "Sélectionne <em>toutes</em> les colonnes de la table <code>pokemon</code>."
        ),
        "indice": "SELECT * retourne toutes les colonnes d'une table.",
        "solution": "SELECT * FROM pokemon",
        "compare": "full",
    },
    {
        "numero": 2,
        "pokemon_id": None,
        "acte": 1,
        "zone": "Bourg Palette",
        "titre": "Noms et types",
        "contexte": "Prof. Chen : Bien. Maintenant réduis le rapport — je n'ai besoin que des noms et de leurs types principaux.",
        "description": (
            "Affiche uniquement le <strong>nom</strong> et le <strong>type principal</strong> "
            "(<code>type1</code>) de chaque Pokémon.\n"
            "Résultat attendu : 151 lignes avec exactement 2 colonnes."
        ),
        "indice": "Liste les colonnes séparées par des virgules après SELECT.",
        "solution": "SELECT nom, type1 FROM pokemon",
        "compare": "full",
    },
    {
        "numero": 3,
        "pokemon_id": 'starter',
        "acte": 1,
        "zone": "Bourg Palette",
        "titre": "Ton starter",
        "contexte": "Ton starter vient d'être enregistré dans la base. Retrouve sa fiche complète.",
        "description": (
            "Retrouve <strong>toutes les informations</strong> sur <code>Salamèche</code> "
            "en filtrant par son nom.\n"
            "<small>Adapte ensuite la requête à ton propre starter si tu en as choisi un autre !</small>"
        ),
        "indice": "Utilise WHERE nom = 'Nom' pour filtrer sur une valeur exacte. Les chaînes sont entre guillemets simples.",
        "solution": "SELECT * FROM pokemon WHERE nom = 'Salamèche'",
        "compare": "names",
    },

    # ══════════════════════════════════════════════════════════════════════
    # ACTE 2 — Forêt de Jade → Argenta  (Q4-Q7)  WHERE, LIKE, AND/OR
    # ══════════════════════════════════════════════════════════════════════
    {
        "numero": 4,
        "pokemon_id": 13,
        "acte": 2,
        "zone": "Forêt de Jade",
        "titre": "L'invasion des insectes",
        "contexte": "La forêt de Jade grouille d'insectes. Le Ranger veut un recensement complet.",
        "description": (
            "Trouve tous les Pokémon dont le <strong>type principal</strong> (<code>type1</code>) "
            "est <code>'Insecte'</code>.\n"
            "Affiche toutes leurs informations."
        ),
        "indice": "Utilise WHERE type1 = 'Insecte' pour filtrer par type.",
        "solution": "SELECT * FROM pokemon WHERE type1 = 'Insecte'",
        "compare": "names",
    },
    {
        "numero": 5,
        "pokemon_id": 4,
        "acte": 2,
        "zone": "Route 3 → Argenta",
        "titre": "Alerte Feu",
        "contexte": "Un Pokémon Feu a incendié les herbes hautes près d'Argenta. Trouve tous les suspects.",
        "description": (
            "Trouve tous les Pokémon dont le <strong>type principal</strong> (<code>type1</code>) "
            "est <code>'Feu'</code>.\n"
            "Affiche toutes leurs informations."
        ),
        "indice": "Utilise WHERE type1 = 'Feu'.",
        "solution": "SELECT * FROM pokemon WHERE type1 = 'Feu'",
        "compare": "names",
    },
    {
        "numero": 6,
        "pokemon_id": 74,
        "acte": 2,
        "zone": "Arène d'Argenta",
        "titre": "La spécialité de Brice",
        "contexte": "L'Arène d'Argenta utilise des Pokémon Roche ET Sol. Giovanni veut connaître tous les adversaires potentiels.",
        "description": (
            "Trouve tous les Pokémon dont le type principal est <code>'Roche'</code> "
            "<strong>ou</strong> <code>'Sol'</code>.\n"
            "Affiche toutes leurs informations."
        ),
        "indice": "Utilise WHERE type1 = 'Roche' OR type1 = 'Sol'. Tu peux aussi écrire WHERE type1 IN ('Roche', 'Sol').",
        "solution": "SELECT * FROM pokemon WHERE type1 = 'Roche' OR type1 = 'Sol'",
        "compare": "names",
    },
    {
        "numero": 7,
        "pokemon_id": 120,
        "acte": 2,
        "zone": "Pont Zinzin",
        "titre": "Misty cherche ses Pokémon",
        "contexte": "Misty a perdu des Pokémon sur le Pont Zinzin. Elle se souvient juste que leurs noms commencent par 'T'.",
        "description": (
            "Retrouve tous les Pokémon dont le nom <strong>commence par la lettre 'T'</strong>.\n"
            "Affiche leur nom et leur <code>type1</code>."
        ),
        "indice": "LIKE 'T%' matche toutes les chaînes qui commencent par T. Le % remplace n'importe quelle suite de caractères.",
        "solution": "SELECT nom, type1 FROM pokemon WHERE nom LIKE 'T%'",
        "compare": "names",
    },

    # ══════════════════════════════════════════════════════════════════════
    # ACTE 3 — Mont Sélénite  (Q8-Q11)  ORDER BY, LIMIT, BETWEEN
    # ══════════════════════════════════════════════════════════════════════
    {
        "numero": 8,
        "pokemon_id": 101,
        "acte": 3,
        "zone": "Mont Sélénite",
        "titre": "Les fuyards de la grotte",
        "contexte": "Dans l'obscurité du Mont Sélénite, seuls les Pokémon les plus rapides échappent aux Racaillou.",
        "description": (
            "Affiche les <strong>10 Pokémon les plus rapides</strong>.\n"
            "Retourne leur nom et leur vitesse, triés du plus rapide au plus lent."
        ),
        "indice": "Combine ORDER BY vitesse DESC (tri décroissant) et LIMIT 10.",
        "solution": "SELECT nom, vitesse FROM pokemon ORDER BY vitesse DESC LIMIT 10",
        "compare": "names",
    },
    {
        "numero": 9,
        "pokemon_id": None,
        "acte": 3,
        "zone": "Mont Sélénite",
        "titre": "La tranche de résistance",
        "contexte": "Les Pokémon de la grotte ont des PV modérés. Le guide cherche ceux entre 50 et 80 PV.",
        "description": (
            "Trouve tous les Pokémon qui ont <strong>entre 50 et 80 points de vie</strong> "
            "(bornes incluses).\n"
            "Affiche toutes leurs informations."
        ),
        "indice": "Utilise WHERE pv BETWEEN 50 AND 80. BETWEEN est inclusif aux deux bornes.",
        "solution": "SELECT * FROM pokemon WHERE pv BETWEEN 50 AND 80",
        "compare": "names",
    },
    {
        "numero": 10,
        "pokemon_id": 95,
        "acte": 3,
        "zone": "Mont Sélénite",
        "titre": "Les boucliers vivants",
        "contexte": "Onix domine la grotte grâce à sa défense légendaire. Qui sont les 5 Pokémon les plus résistants ?",
        "description": (
            "Affiche les <strong>5 Pokémon avec la meilleure défense</strong>.\n"
            "Retourne leur nom et leur défense, triés du plus résistant au moins résistant."
        ),
        "indice": "ORDER BY defense DESC LIMIT 5.",
        "solution": "SELECT nom, defense FROM pokemon ORDER BY defense DESC LIMIT 5",
        "compare": "names",
    },
    {
        "numero": 11,
        "pokemon_id": 150,
        "acte": 3,
        "zone": "Mont Sélénite",
        "titre": "Rumeurs légendaires",
        "contexte": "Des témoins affirment avoir vu des silhouettes aux pouvoirs démesurés dans la montagne. Les légendaires de Kanto...",
        "description": (
            "Trouve tous les <strong>Pokémon légendaires</strong>.\n"
            "Affiche toutes leurs informations.\n"
            "La colonne <code>est_legendaire</code> vaut <code>1</code> pour les légendaires, <code>0</code> sinon."
        ),
        "indice": "Filtre avec WHERE est_legendaire = 1.",
        "solution": "SELECT * FROM pokemon WHERE est_legendaire = 1",
        "compare": "names",
    },

    # ══════════════════════════════════════════════════════════════════════
    # ACTE 4 — Céladopole  (Q12-Q15)  GROUP BY, COUNT, HAVING, AVG
    # ══════════════════════════════════════════════════════════════════════
    {
        "numero": 12,
        "pokemon_id": None,
        "acte": 4,
        "zone": "Céladopole",
        "titre": "L'inventaire du maire",
        "contexte": "Le maire de Céladopole commande une analyse. Combien de Pokémon existe-t-il par type ?",
        "description": (
            "Compte le nombre de Pokémon par <strong>type principal</strong> (<code>type1</code>).\n"
            "Affiche le type et le total (nommé <code>total</code>), triés du plus grand au plus petit."
        ),
        "indice": "Utilise GROUP BY type1 avec COUNT(*) AS total, puis ORDER BY total DESC.",
        "solution": "SELECT type1, COUNT(*) AS total FROM pokemon GROUP BY type1 ORDER BY total DESC",
        "compare": "aggregate",
    },
    {
        "numero": 13,
        "pokemon_id": None,
        "acte": 4,
        "zone": "Céladopole",
        "titre": "Les types dominants",
        "contexte": "Le maire affine sa demande : il ne veut voir que les types vraiment bien représentés — plus de 10 Pokémon.",
        "description": (
            "Compte le nombre de Pokémon par type principal.\n"
            "N'affiche que les types qui ont <strong>strictement plus de 10 Pokémon</strong>.\n"
            "Trie du plus grand au plus petit."
        ),
        "indice": "Utilise HAVING total > 10 après GROUP BY pour filtrer les groupes (pas WHERE qui filtre les lignes).",
        "solution": "SELECT type1, COUNT(*) AS total FROM pokemon GROUP BY type1 HAVING total > 10 ORDER BY total DESC",
        "compare": "aggregate",
    },
    {
        "numero": 14,
        "pokemon_id": None,
        "acte": 4,
        "zone": "Laboratoire Silph",
        "titre": "Le Pokémon moyen",
        "contexte": "Les chercheurs du labo Silph veulent connaître le profil moyen d'un Pokémon de Kanto.",
        "description": (
            "Calcule la <strong>moyenne</strong> des colonnes <code>pv</code>, <code>attaque</code>, "
            "<code>defense</code> et <code>vitesse</code> de tous les Pokémon.\n"
            "Nomme les colonnes <code>moy_pv</code>, <code>moy_att</code>, <code>moy_def</code>, <code>moy_vit</code>.\n"
            "Arrondis chaque valeur à 1 décimale avec <code>ROUND(..., 1)</code>."
        ),
        "indice": "SELECT ROUND(AVG(colonne), 1) AS alias, … FROM pokemon",
        "solution": (
            "SELECT ROUND(AVG(pv),1) AS moy_pv, ROUND(AVG(attaque),1) AS moy_att, "
            "ROUND(AVG(defense),1) AS moy_def, ROUND(AVG(vitesse),1) AS moy_vit FROM pokemon"
        ),
        "compare": "full",
    },
    {
        "numero": 15,
        "pokemon_id": None,
        "acte": 4,
        "zone": "Arène de Céladopole",
        "titre": "Les combattants d'élite",
        "contexte": "L'Arène de Céladopole cherche le type le plus offensif. Quel type a la moyenne d'attaque la plus élevée ?",
        "description": (
            "Trouve le <strong>type principal</strong> qui a la <strong>moyenne d'attaque la plus élevée</strong>.\n"
            "Affiche le <code>type1</code> et la moyenne (nommée <code>moy_att</code>), "
            "arrondie à 1 décimale.\n"
            "N'affiche que le type gagnant."
        ),
        "indice": "GROUP BY type1, puis ORDER BY moy_att DESC LIMIT 1.",
        "solution": (
            "SELECT type1, ROUND(AVG(attaque),1) AS moy_att "
            "FROM pokemon GROUP BY type1 ORDER BY moy_att DESC LIMIT 1"
        ),
        "compare": "first_col",
    },

    # ══════════════════════════════════════════════════════════════════════
    # ACTE 5 — Lavanville  (Q16-Q19)  JOIN simple
    # ══════════════════════════════════════════════════════════════════════
    {
        "numero": 16,
        "pokemon_id": 52,
        "acte": 5,
        "zone": "Lavanville",
        "titre": "Les esprits du Jackpot",
        "contexte": "Les fantômes de Lavanville utilisent une capacité mystérieuse : Jackpot. Qui la possède ?",
        "description": (
            "Trouve tous les Pokémon qui connaissent la capacité <strong>'Jackpot'</strong>.\n"
            "Affiche uniquement leur nom.\n"
            "<small>Tables : <code>pokemon</code> · <code>pokemon_capacites</code> · <code>capacites</code></small>"
        ),
        "indice": (
            "Effectue deux JOIN :\n"
            "FROM pokemon p\n"
            "JOIN pokemon_capacites pc ON p.id = pc.pokemon_id\n"
            "JOIN capacites c ON c.id = pc.capacite_id\n"
            "WHERE c.nom = 'Jackpot'"
        ),
        "solution": (
            "SELECT DISTINCT p.nom FROM pokemon p "
            "JOIN pokemon_capacites pc ON p.id = pc.pokemon_id "
            "JOIN capacites c ON c.id = pc.capacite_id "
            "WHERE c.nom = 'Jackpot'"
        ),
        "compare": "names",
    },
    {
        "numero": 17,
        "pokemon_id": 92,
        "acte": 5,
        "zone": "Lavanville",
        "titre": "L'arsenal de Fantominus",
        "contexte": "Fantominus rôde dans la Tour Pokémon. Quelles capacités peut-il utiliser contre toi ?",
        "description": (
            "Retrouve <strong>toutes les capacités</strong> que connaît <code>Fantominus</code>.\n"
            "Affiche le nom, la catégorie et la puissance de chaque capacité."
        ),
        "indice": (
            "JOIN pokemon_capacites pc ON p.id = pc.pokemon_id\n"
            "JOIN capacites c ON c.id = pc.capacite_id\n"
            "WHERE p.nom = 'Fantominus'"
        ),
        "solution": (
            "SELECT c.nom, c.categorie, c.puissance FROM pokemon p "
            "JOIN pokemon_capacites pc ON p.id = pc.pokemon_id "
            "JOIN capacites c ON c.id = pc.capacite_id "
            "WHERE p.nom = 'Fantominus'"
        ),
        "compare": "names",
    },
    {
        "numero": 18,
        "pokemon_id": 65,
        "acte": 5,
        "zone": "Lavanville",
        "titre": "Menace Psy",
        "contexte": "Un afflux de Pokémon utilisant des capacités Psy terrorise Lavanville. Qui les maîtrise ?",
        "description": (
            "Trouve tous les Pokémon qui connaissent <strong>au moins une capacité de type Psy</strong>.\n"
            "Affiche leur nom et leur <code>type1</code>.\n"
            "<small>Tables : <code>pokemon</code> · <code>pokemon_capacites</code> · "
            "<code>capacites</code> · <code>types</code></small>"
        ),
        "indice": (
            "Ajoute un troisième JOIN sur la table types :\n"
            "JOIN types t ON t.id = c.type_id\n"
            "WHERE t.nom = 'Psy'"
        ),
        "solution": (
            "SELECT DISTINCT p.nom, p.type1 FROM pokemon p "
            "JOIN pokemon_capacites pc ON p.id = pc.pokemon_id "
            "JOIN capacites c ON c.id = pc.capacite_id "
            "JOIN types t ON t.id = c.type_id "
            "WHERE t.nom = 'Psy'"
        ),
        "compare": "names",
    },
    {
        "numero": 19,
        "pokemon_id": None,
        "acte": 5,
        "zone": "Lavanville",
        "titre": "Diversité des types secondaires",
        "contexte": "Prof. Chen collecte des données pour sa recherche sur les Pokémon bi-types de Kanto.",
        "description": (
            "Compte le nombre de Pokémon par <strong>type secondaire</strong> (<code>type2</code>).\n"
            "Ignore les Pokémon sans type secondaire (<code>type2 IS NOT NULL</code>).\n"
            "Affiche le type2 et le total, triés du plus représenté au moins représenté."
        ),
        "indice": "WHERE type2 IS NOT NULL, puis GROUP BY type2 avec COUNT(*) AS total.",
        "solution": (
            "SELECT type2, COUNT(*) AS total FROM pokemon "
            "WHERE type2 IS NOT NULL GROUP BY type2 ORDER BY total DESC"
        ),
        "compare": "aggregate",
    },

    # ══════════════════════════════════════════════════════════════════════
    # ACTE 6 — Parmanie → Carmin  (Q20-Q23)  JOIN multiple, GROUP BY avancé
    # ══════════════════════════════════════════════════════════════════════
    {
        "numero": 20,
        "pokemon_id": 23,
        "acte": 6,
        "zone": "Parmanie",
        "titre": "La Rocket frappe",
        "contexte": "La Team Rocket infiltre Parmanie avec des Pokémon Poison. Dresse la liste complète de la menace.",
        "description": (
            "Trouve tous les Pokémon qui ont le type <strong>Poison</strong> "
            "en type principal (<code>type1</code>) <strong>ou</strong> "
            "en type secondaire (<code>type2</code>).\n"
            "Affiche toutes leurs informations."
        ),
        "indice": "WHERE type1 = 'Poison' OR type2 = 'Poison'",
        "solution": "SELECT * FROM pokemon WHERE type1 = 'Poison' OR type2 = 'Poison'",
        "compare": "names",
    },
    {
        "numero": 21,
        "pokemon_id": 112,
        "acte": 6,
        "zone": "Quartier Général Rocket",
        "titre": "Les soldats de Giovanni",
        "contexte": "Giovanni, chef de la Rocket, utilise des Pokémon Sol. Analyse leur puissance offensive.",
        "description": (
            "Affiche le <strong>nom</strong>, l'<strong>attaque</strong> et la "
            "<strong>vitesse</strong> de tous les Pokémon de type principal <code>'Sol'</code>.\n"
            "Trie-les par attaque décroissante."
        ),
        "indice": "WHERE type1 = 'Sol' ORDER BY attaque DESC",
        "solution": "SELECT nom, attaque, vitesse FROM pokemon WHERE type1 = 'Sol' ORDER BY attaque DESC",
        "compare": "names",
    },
    {
        "numero": 22,
        "pokemon_id": 34,
        "acte": 6,
        "zone": "Carmin-sur-Mer",
        "titre": "Séisme et Plaquage",
        "contexte": "Certains Pokémon maîtrisent à la fois Séisme et Plaquage — une combinaison dévastatrice sur le terrain.",
        "description": (
            "Trouve tous les Pokémon qui connaissent <strong>à la fois</strong> "
            "la capacité <code>'Séisme'</code> <strong>et</strong> la capacité <code>'Plaquage'</code>.\n"
            "Affiche uniquement leur nom."
        ),
        "indice": (
            "Double JOIN sur pokemon_capacites avec des alias différents :\n"
            "JOIN pokemon_capacites pc1 ON p.id = pc1.pokemon_id\n"
            "JOIN capacites c1 ON c1.id = pc1.capacite_id\n"
            "JOIN pokemon_capacites pc2 ON p.id = pc2.pokemon_id\n"
            "JOIN capacites c2 ON c2.id = pc2.capacite_id\n"
            "WHERE c1.nom = 'Séisme' AND c2.nom = 'Plaquage'"
        ),
        "solution": (
            "SELECT p.nom FROM pokemon p "
            "JOIN pokemon_capacites pc1 ON p.id = pc1.pokemon_id "
            "JOIN capacites c1 ON c1.id = pc1.capacite_id "
            "JOIN pokemon_capacites pc2 ON p.id = pc2.pokemon_id "
            "JOIN capacites c2 ON c2.id = pc2.capacite_id "
            "WHERE c1.nom = 'Séisme' AND c2.nom = 'Plaquage'"
        ),
        "compare": "names",
    },
    {
        "numero": 23,
        "pokemon_id": None,
        "acte": 6,
        "zone": "Carmin-sur-Mer",
        "titre": "L'arsenal de Kanto",
        "contexte": "Prof. Chen dresse le catalogue des capacités par type pour son encyclopédie.",
        "description": (
            "Affiche le <strong>nombre de capacités</strong> disponibles pour chaque <strong>type de capacité</strong>.\n"
            "Affiche le nom du type (depuis la table <code>types</code>) "
            "et le total (nommé <code>nb</code>).\n"
            "Trie du type le plus fourni au moins fourni."
        ),
        "indice": (
            "JOIN types t ON t.id = c.type_id\n"
            "GROUP BY t.id ORDER BY nb DESC"
        ),
        "solution": (
            "SELECT t.nom AS type_cap, COUNT(*) AS nb FROM capacites c "
            "JOIN types t ON t.id = c.type_id GROUP BY t.id ORDER BY nb DESC"
        ),
        "compare": "aggregate",
    },

    # ══════════════════════════════════════════════════════════════════════
    # ACTE 7 — Cramois'île  (Q24-Q27)  Sous-requêtes
    # ══════════════════════════════════════════════════════════════════════
    {
        "numero": 24,
        "pokemon_id": 149,
        "acte": 7,
        "zone": "Cramois'île",
        "titre": "Les attaquants de l'île",
        "contexte": "Les Pokémon de Cramois'île sont hors normes. Lesquels ont une attaque supérieure à la moyenne de Kanto ?",
        "description": (
            "Trouve tous les Pokémon dont l'<strong>attaque est supérieure à la moyenne</strong> "
            "de tous les Pokémon.\n"
            "Affiche leur nom et leur attaque, triés par attaque décroissante."
        ),
        "indice": "Utilise une sous-requête : WHERE attaque > (SELECT AVG(attaque) FROM pokemon)",
        "solution": (
            "SELECT nom, attaque FROM pokemon "
            "WHERE attaque > (SELECT AVG(attaque) FROM pokemon) ORDER BY attaque DESC"
        ),
        "compare": "names",
    },
    {
        "numero": 25,
        "pokemon_id": 25,
        "acte": 7,
        "zone": "Cramois'île",
        "titre": "Plus rapide que Pikachu",
        "contexte": "Pikachu est réputé pour sa vitesse. Mais qui, dans toute la région, peut le surpasser ?",
        "description": (
            "Trouve tous les Pokémon dont la <strong>vitesse est strictement supérieure</strong> "
            "à celle de <code>Pikachu</code>.\n"
            "Affiche leur nom et leur vitesse, triés par vitesse décroissante."
        ),
        "indice": "WHERE vitesse > (SELECT vitesse FROM pokemon WHERE nom = 'Pikachu')",
        "solution": (
            "SELECT nom, vitesse FROM pokemon "
            "WHERE vitesse > (SELECT vitesse FROM pokemon WHERE nom = 'Pikachu') "
            "ORDER BY vitesse DESC"
        ),
        "compare": "names",
    },
    {
        "numero": 26,
        "pokemon_id": 3,
        "acte": 7,
        "zone": "Cramois'île",
        "titre": "Les costauds de leur type",
        "contexte": "Parmi les Pokémon de l'île, certains ont plus de PV que la moyenne de leur propre type. Ce sont les vrais survivants.",
        "description": (
            "Trouve tous les Pokémon dont les <strong>PV sont supérieurs à la moyenne "
            "des PV de leur propre <code>type1</code></strong>.\n"
            "Affiche leur nom, leurs PV et leur type1."
        ),
        "indice": (
            "Sous-requête corrélée dans le WHERE :\n"
            "WHERE p.pv > (SELECT AVG(p2.pv) FROM pokemon p2 WHERE p2.type1 = p.type1)"
        ),
        "solution": (
            "SELECT p.nom, p.pv, p.type1 FROM pokemon p "
            "WHERE p.pv > (SELECT AVG(p2.pv) FROM pokemon p2 WHERE p2.type1 = p.type1)"
        ),
        "compare": "names",
    },
    {
        "numero": 27,
        "pokemon_id": 7,
        "acte": 7,
        "zone": "Cramois'île",
        "titre": "Résistants au Feu",
        "contexte": "Pour explorer le Volcan Cramoisie, tu as besoin de Pokémon qui ne connaissent aucune capacité de type Feu.",
        "description": (
            "Trouve tous les Pokémon qui <strong>ne connaissent aucune capacité de type Feu</strong>.\n"
            "Affiche uniquement leur nom."
        ),
        "indice": (
            "Utilise NOT IN avec une sous-requête :\n"
            "WHERE p.id NOT IN (\n"
            "  SELECT pc.pokemon_id FROM pokemon_capacites pc\n"
            "  JOIN capacites c ON c.id = pc.capacite_id\n"
            "  JOIN types t ON t.id = c.type_id WHERE t.nom = 'Feu'\n"
            ")"
        ),
        "solution": (
            "SELECT p.nom FROM pokemon p "
            "WHERE p.id NOT IN ("
            "SELECT pc.pokemon_id FROM pokemon_capacites pc "
            "JOIN capacites c ON c.id = pc.capacite_id "
            "JOIN types t ON t.id = c.type_id WHERE t.nom = 'Feu')"
        ),
        "compare": "names",
    },

    # ══════════════════════════════════════════════════════════════════════
    # ACTE 8 — Azuria → Grisaille  (Q28-Q31)  Sous-requêtes avancées, EXISTS
    # ══════════════════════════════════════════════════════════════════════
    {
        "numero": 28,
        "pokemon_id": None,
        "acte": 8,
        "zone": "Azuria",
        "titre": "Types sans gloire",
        "contexte": "Les chercheurs d'Azuria étudient les types qui n'ont jamais produit de Pokémon légendaire.",
        "description": (
            "Trouve tous les <strong>types principaux</strong> (<code>type1</code>) "
            "qui n'ont <strong>aucun Pokémon légendaire</strong>.\n"
            "Affiche la liste des types concernés, triés par ordre alphabétique."
        ),
        "indice": (
            "WHERE type1 NOT IN (\n"
            "  SELECT DISTINCT type1 FROM pokemon WHERE est_legendaire = 1\n"
            ")"
        ),
        "solution": (
            "SELECT DISTINCT type1 FROM pokemon "
            "WHERE type1 NOT IN (SELECT DISTINCT type1 FROM pokemon WHERE est_legendaire = 1) "
            "ORDER BY type1"
        ),
        "compare": "first_col",
    },
    {
        "numero": 29,
        "pokemon_id": 127,
        "acte": 8,
        "zone": "Route Safari",
        "titre": "Le top 10% offensif",
        "contexte": "La Zone Safari ne laisse entrer que l'élite. Seuls les Pokémon dans le top 10% d'attaque sont admis.",
        "description": (
            "Trouve les Pokémon dont l'attaque est dans le <strong>top 10%</strong> "
            "(les 15 meilleures valeurs d'attaque).\n"
            "Affiche leur nom et leur attaque, triés par attaque décroissante.\n"
            "<small>Astuce : 10% de 151 ≈ 15 — trouve la valeur d'attaque au rang 15.</small>"
        ),
        "indice": (
            "Sous-requête pour le seuil :\n"
            "WHERE attaque >= (SELECT attaque FROM pokemon ORDER BY attaque DESC LIMIT 1 OFFSET 14)"
        ),
        "solution": (
            "SELECT nom, attaque FROM pokemon "
            "WHERE attaque >= (SELECT attaque FROM pokemon ORDER BY attaque DESC LIMIT 1 OFFSET 14) "
            "ORDER BY attaque DESC"
        ),
        "compare": "names",
    },
    {
        "numero": 30,
        "pokemon_id": 150,
        "acte": 8,
        "zone": "Grisaille City",
        "titre": "Les colosses destructeurs",
        "contexte": "Le Cinéma de Grisaille produit un film sur les Pokémon qui maîtrisent les capacités les plus dévastatrices.",
        "description": (
            "Trouve tous les Pokémon qui connaissent <strong>au moins une capacité "
            "dont la puissance est supérieure à 100</strong>.\n"
            "Affiche leur nom et leur type1.\n"
            "<small>Utilise EXISTS pour tester l'existence d'une telle capacité.</small>"
        ),
        "indice": (
            "WHERE EXISTS (\n"
            "  SELECT 1 FROM pokemon_capacites pc\n"
            "  JOIN capacites c ON c.id = pc.capacite_id\n"
            "  WHERE pc.pokemon_id = p.id AND c.puissance > 100\n"
            ")"
        ),
        "solution": (
            "SELECT DISTINCT p.nom, p.type1 FROM pokemon p "
            "WHERE EXISTS ("
            "SELECT 1 FROM pokemon_capacites pc "
            "JOIN capacites c ON c.id = pc.capacite_id "
            "WHERE pc.pokemon_id = p.id AND c.puissance > 100)"
        ),
        "compare": "names",
    },
    {
        "numero": 31,
        "pokemon_id": 101,
        "acte": 8,
        "zone": "Grisaille City",
        "titre": "Le plus rapide de chaque type",
        "contexte": "Prof. Chen dresse le palmarès : pour chaque type, quel est le Pokémon le plus véloce ?",
        "description": (
            "Pour chaque <strong>type principal</strong>, affiche le "
            "<strong>Pokémon avec la vitesse la plus élevée</strong>.\n"
            "Affiche le type1, le nom du Pokémon et sa vitesse.\n"
            "Trie par type1 alphabétiquement."
        ),
        "indice": (
            "Sous-requête corrélée dans le WHERE :\n"
            "WHERE p.vitesse = (SELECT MAX(p2.vitesse) FROM pokemon p2 WHERE p2.type1 = p.type1)"
        ),
        "solution": (
            "SELECT p.type1, p.nom, p.vitesse FROM pokemon p "
            "WHERE p.vitesse = (SELECT MAX(p2.vitesse) FROM pokemon p2 WHERE p2.type1 = p.type1) "
            "ORDER BY p.type1"
        ),
        "compare": "names",
    },

    # ══════════════════════════════════════════════════════════════════════
    # ACTE 9 — Plateau Indigo  (Q32-Q35)  Requêtes complexes combinées
    # ══════════════════════════════════════════════════════════════════════
    {
        "numero": 32,
        "pokemon_id": 150,
        "acte": 9,
        "zone": "Plateau Indigo",
        "titre": "Le classement général",
        "contexte": "La Ligue Pokémon établit son classement. Le score total (PV + Attaque + Défense + Vitesse) détermine les finalistes.",
        "description": (
            "Calcule le <strong>score total</strong> de chaque Pokémon "
            "(<code>pv + attaque + defense + vitesse</code>).\n"
            "Affiche le nom et le score (nommé <code>score</code>).\n"
            "Trie du score le plus élevé au plus bas et affiche les <strong>20 premiers</strong>."
        ),
        "indice": "SELECT nom, (pv + attaque + defense + vitesse) AS score FROM pokemon ORDER BY score DESC LIMIT 20",
        "solution": (
            "SELECT nom, (pv + attaque + defense + vitesse) AS score "
            "FROM pokemon ORDER BY score DESC LIMIT 20"
        ),
        "compare": "names",
    },
    {
        "numero": 33,
        "pokemon_id": 149,
        "acte": 9,
        "zone": "Plateau Indigo",
        "titre": "Les bi-types d'élite",
        "contexte": "Les Pokémon bi-types ont l'avantage de la polyvalence. Mais lesquels sont vraiment au-dessus de la moyenne ?",
        "description": (
            "Trouve les Pokémon qui ont un <strong>type secondaire</strong> (<code>type2 IS NOT NULL</code>) "
            "ET dont le score total (<code>pv + attaque + defense + vitesse</code>) est "
            "<strong>supérieur à la moyenne générale</strong> de tous les Pokémon.\n"
            "Affiche leur nom, type1, type2 et score, triés par score décroissant."
        ),
        "indice": (
            "WHERE type2 IS NOT NULL\n"
            "AND (pv + attaque + defense + vitesse) > (SELECT AVG(pv + attaque + defense + vitesse) FROM pokemon)"
        ),
        "solution": (
            "SELECT nom, type1, type2, (pv + attaque + defense + vitesse) AS score "
            "FROM pokemon "
            "WHERE type2 IS NOT NULL "
            "AND (pv + attaque + defense + vitesse) > (SELECT AVG(pv + attaque + defense + vitesse) FROM pokemon) "
            "ORDER BY score DESC"
        ),
        "compare": "names",
    },
    {
        "numero": 34,
        "pokemon_id": 150,
        "acte": 9,
        "zone": "Plateau Indigo",
        "titre": "Le champion de chaque type",
        "contexte": "Avant la grande finale, chaque type élit son champion : le Pokémon avec le score total le plus élevé.",
        "description": (
            "Pour chaque <strong>type principal</strong>, trouve le Pokémon avec le "
            "<strong>score total le plus élevé</strong> (<code>pv + attaque + defense + vitesse</code>).\n"
            "Affiche le type1, le nom du champion et son score.\n"
            "Trie par score décroissant."
        ),
        "indice": (
            "Sous-requête corrélée :\n"
            "WHERE (p.pv + p.attaque + p.defense + p.vitesse) = (\n"
            "  SELECT MAX(p2.pv + p2.attaque + p2.defense + p2.vitesse)\n"
            "  FROM pokemon p2 WHERE p2.type1 = p.type1\n"
            ")"
        ),
        "solution": (
            "SELECT p.type1, p.nom, (p.pv + p.attaque + p.defense + p.vitesse) AS score "
            "FROM pokemon p "
            "WHERE (p.pv + p.attaque + p.defense + p.vitesse) = ("
            "SELECT MAX(p2.pv + p2.attaque + p2.defense + p2.vitesse) "
            "FROM pokemon p2 WHERE p2.type1 = p.type1) "
            "ORDER BY score DESC"
        ),
        "compare": "names",
    },
    {
        "numero": 35,
        "pokemon_id": 150,
        "acte": 9,
        "zone": "Plateau Indigo",
        "titre": "L'équipe parfaite",
        "contexte": "La grande finale ! Il faut le Top 5 absolu : les Pokémon avec le meilleur score total, parmi ceux qui connaissent le plus de capacités.",
        "description": (
            "Affiche le <strong>Top 5</strong> des Pokémon les plus complets :\n"
            "ceux qui ont le <strong>score total</strong> (<code>pv + attaque + defense + vitesse</code>) "
            "le plus élevé, et à score égal, le plus grand <strong>nombre de capacités</strong>.\n"
            "Affiche le nom, le score (<code>score</code>) et le nombre de capacités (<code>nb_cap</code>)."
        ),
        "indice": (
            "Combine JOIN sur pokemon_capacites, GROUP BY p.id, "
            "puis ORDER BY score DESC, nb_cap DESC LIMIT 5."
        ),
        "solution": (
            "SELECT p.nom, (p.pv + p.attaque + p.defense + p.vitesse) AS score, "
            "COUNT(pc.capacite_id) AS nb_cap "
            "FROM pokemon p JOIN pokemon_capacites pc ON p.id = pc.pokemon_id "
            "GROUP BY p.id ORDER BY score DESC, nb_cap DESC LIMIT 5"
        ),
        "compare": "names",
    },
]
