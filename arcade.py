"""arcade.py – 60 templates SQL pour le mode Arcade de SQLemon (4 niveaux)."""

import random
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sqlemon.db")

# ── Cache données DB ──────────────────────────────────────────────────────────

_cache = None

def _data():
    global _cache
    if _cache:
        return _cache
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    _cache = {
        "types1":    [r[0] for r in conn.execute("SELECT DISTINCT type1 FROM pokemon ORDER BY type1")],
        "types2":    [r[0] for r in conn.execute("SELECT DISTINCT type2 FROM pokemon WHERE type2 IS NOT NULL ORDER BY type2")],
        "pokemon":   [r[0] for r in conn.execute("SELECT nom FROM pokemon ORDER BY id")],
        "capacites": [r[0] for r in conn.execute("SELECT nom FROM capacites ORDER BY id")],
        "categories":[r[0] for r in conn.execute("SELECT DISTINCT categorie FROM capacites WHERE categorie IS NOT NULL")],
    }
    conn.close()
    return _cache

# ── Helpers ────────────────────────────────────────────────────────────────────

def _rc(lst):        return random.choice(lst)
def _t1():           return _rc(_data()["types1"])
def _t2():           return _rc(_data()["types2"])
def _pok():          return _rc(_data()["pokemon"])
def _cap():          return _rc(_data()["capacites"])
def _cat():          return _rc(_data()["categories"])
def _s():            return _rc(["pv", "attaque", "defense", "vitesse"])
def _sl(s):          return {"pv":"PV","attaque":"ATTAQUE","defense":"DÉFENSE","vitesse":"VITESSE"}[s]
def _n(lo=3, hi=15): return random.randint(lo, hi)
def _esc(s):         return s.replace("'", "''")

SEUILS = {
    "pv":      [40, 50, 60, 80, 100, 120],
    "attaque": [40, 50, 60, 70, 80, 90],
    "defense": [40, 50, 60, 70, 80, 90],
    "vitesse": [40, 50, 60, 70, 80, 90],
}
BETWEEN_RANGES = {
    "pv":      [(40, 80), (60, 100), (70, 120), (50, 90)],
    "attaque": [(40, 70), (50, 80), (60, 90), (70, 100)],
    "defense": [(40, 70), (50, 80), (60, 90), (70, 100)],
    "vitesse": [(40, 70), (50, 80), (60, 90), (70, 100)],
}
def _sv(stat): return _rc(SEUILS[stat])
def _bv(stat): return _rc(BETWEEN_RANGES[stat])

# ── NIVEAU 1 — SELECT / WHERE basiques (15) ───────────────────────────────────

def n1_01():
    t = _t1()
    return {
        "niveau": 1, "categorie": "SELECT *",
        "titre": f"TOUT AFFICHER — TYPE {t.upper()}",
        "description": (
            f"Affiche <strong>toutes les colonnes</strong> des Pokémon\n"
            f"dont le <code>type1</code> est <strong>'{t}'</strong>."
        ),
        "indice": f"SELECT * FROM pokemon WHERE type1 = ...",
        "solution": f"SELECT * FROM pokemon WHERE type1 = '{t}'",
        "compare": "names", "pokemon_id": None,
    }

def n1_02():
    t = _t1()
    return {
        "niveau": 1, "categorie": "SELECT colonnes",
        "titre": f"NOM ET STATS — TYPE {t.upper()}",
        "description": (
            f"Sélectionne <code>nom</code>, <code>pv</code>, <code>attaque</code>,\n"
            f"<code>defense</code>, <code>vitesse</code>\n"
            f"des Pokémon dont le <code>type1</code> est <strong>'{t}'</strong>."
        ),
        "indice": "SELECT nom, pv, attaque, defense, vitesse FROM pokemon WHERE type1 = ...",
        "solution": f"SELECT nom, pv, attaque, defense, vitesse FROM pokemon WHERE type1 = '{t}'",
        "compare": "names", "pokemon_id": None,
    }

def n1_03():
    t = _t1()
    return {
        "niveau": 1, "categorie": "SELECT colonnes",
        "titre": f"NOM ET TYPES — TYPE {t.upper()}",
        "description": (
            f"Sélectionne <code>nom</code>, <code>type1</code> et <code>type2</code>\n"
            f"des Pokémon dont le <code>type1</code> est <strong>'{t}'</strong>."
        ),
        "indice": "SELECT nom, type1, type2 FROM pokemon WHERE type1 = ...",
        "solution": f"SELECT nom, type1, type2 FROM pokemon WHERE type1 = '{t}'",
        "compare": "names", "pokemon_id": None,
    }

def n1_04():
    stat = _s(); label = _sl(stat); seuil = _sv(stat)
    return {
        "niveau": 1, "categorie": "WHERE stat",
        "titre": f"{label} > {seuil}",
        "description": (
            f"Sélectionne le <code>nom</code> de tous les Pokémon\n"
            f"dont <code>{stat}</code> est <strong>strictement supérieur</strong> à {seuil}."
        ),
        "indice": f"SELECT nom FROM pokemon WHERE {stat} > ...",
        "solution": f"SELECT nom FROM pokemon WHERE {stat} > {seuil}",
        "compare": "names", "pokemon_id": None,
    }

def n1_05():
    stat = _s(); label = _sl(stat); seuil = _sv(stat)
    return {
        "niveau": 1, "categorie": "WHERE stat",
        "titre": f"{label} <= {seuil}",
        "description": (
            f"Sélectionne le <code>nom</code> de tous les Pokémon\n"
            f"dont <code>{stat}</code> est <strong>inférieur ou égal</strong> à {seuil}."
        ),
        "indice": f"SELECT nom FROM pokemon WHERE {stat} <= ...",
        "solution": f"SELECT nom FROM pokemon WHERE {stat} <= {seuil}",
        "compare": "names", "pokemon_id": None,
    }

def n1_06():
    letter = _rc(list("ABCDEFGHKLMNOPRST"))
    return {
        "niveau": 1, "categorie": "LIKE",
        "titre": f"NOMS COMMENÇANT PAR '{letter}'",
        "description": (
            f"Sélectionne le <code>nom</code> des Pokémon\n"
            f"dont le nom <strong>commence</strong> par la lettre <strong>'{letter}'</strong>.\n"
            f"<small>Utilise LIKE avec le joker % en fin.</small>"
        ),
        "indice": f"SELECT nom FROM pokemon WHERE nom LIKE '{letter}%'",
        "solution": f"SELECT nom FROM pokemon WHERE nom LIKE '{letter}%'",
        "compare": "names", "pokemon_id": None,
    }

def n1_07():
    letter = _rc(list("ABCDEFGHKLMNOPRST"))
    return {
        "niveau": 1, "categorie": "LIKE",
        "titre": f"NOMS CONTENANT '{letter}'",
        "description": (
            f"Sélectionne le <code>nom</code> des Pokémon\n"
            f"dont le nom <strong>contient</strong> la lettre <strong>'{letter}'</strong>.\n"
            f"<small>Utilise LIKE avec % avant et après.</small>"
        ),
        "indice": f"SELECT nom FROM pokemon WHERE nom LIKE '%{letter}%'",
        "solution": f"SELECT nom FROM pokemon WHERE nom LIKE '%{letter}%'",
        "compare": "names", "pokemon_id": None,
    }

def n1_08():
    letter = _rc(list("ABCDEFGHKLMNOPRST"))
    return {
        "niveau": 1, "categorie": "LIKE",
        "titre": f"NOMS FINISSANT PAR '{letter}'",
        "description": (
            f"Sélectionne le <code>nom</code> des Pokémon\n"
            f"dont le nom <strong>se termine</strong> par la lettre <strong>'{letter}'</strong>.\n"
            f"<small>Utilise LIKE avec % au début.</small>"
        ),
        "indice": f"SELECT nom FROM pokemon WHERE nom LIKE '%{letter}'",
        "solution": f"SELECT nom FROM pokemon WHERE nom LIKE '%{letter}'",
        "compare": "names", "pokemon_id": None,
    }

def n1_09():
    return {
        "niveau": 1, "categorie": "WHERE booléen",
        "titre": "POKÉMON LÉGENDAIRES",
        "description": (
            "Sélectionne le <code>nom</code> de tous les Pokémon\n"
            "marqués comme légendaires\n"
            "(<code>est_legendaire = 1</code>)."
        ),
        "indice": "SELECT nom FROM pokemon WHERE est_legendaire = 1",
        "solution": "SELECT nom FROM pokemon WHERE est_legendaire = 1",
        "compare": "names", "pokemon_id": 150,
    }

def n1_10():
    return {
        "niveau": 1, "categorie": "WHERE NULL",
        "titre": "POKÉMON MONO-TYPE",
        "description": (
            "Sélectionne le <code>nom</code> des Pokémon\n"
            "qui n'ont <strong>pas</strong> de type secondaire\n"
            "(<code>type2</code> est NULL)."
        ),
        "indice": "SELECT nom FROM pokemon WHERE type2 IS NULL",
        "solution": "SELECT nom FROM pokemon WHERE type2 IS NULL",
        "compare": "names", "pokemon_id": None,
    }

def n1_11():
    return {
        "niveau": 1, "categorie": "WHERE NULL",
        "titre": "POKÉMON BI-TYPE",
        "description": (
            "Sélectionne le <code>nom</code> des Pokémon\n"
            "qui possèdent <strong>un type secondaire</strong>\n"
            "(<code>type2</code> n'est PAS NULL)."
        ),
        "indice": "SELECT nom FROM pokemon WHERE type2 IS NOT NULL",
        "solution": "SELECT nom FROM pokemon WHERE type2 IS NOT NULL",
        "compare": "names", "pokemon_id": None,
    }

def n1_12():
    t2 = _t2()
    return {
        "niveau": 1, "categorie": "WHERE type2",
        "titre": f"TYPE SECONDAIRE : {t2.upper()}",
        "description": (
            f"Sélectionne <code>nom</code>, <code>type1</code> et <code>type2</code>\n"
            f"des Pokémon dont le <code>type2</code> est <strong>'{t2}'</strong>."
        ),
        "indice": f"SELECT nom, type1, type2 FROM pokemon WHERE type2 = '{t2}'",
        "solution": f"SELECT nom, type1, type2 FROM pokemon WHERE type2 = '{t2}'",
        "compare": "names", "pokemon_id": None,
    }

def n1_13():
    cat = _cat()
    return {
        "niveau": 1, "categorie": "SELECT capacites",
        "titre": f"CAPACITÉS DE CATÉGORIE {cat.upper()}",
        "description": (
            f"Sélectionne le <code>nom</code> de toutes les capacités\n"
            f"dont la <code>categorie</code> est <strong>'{cat}'</strong>."
        ),
        "indice": f"SELECT nom FROM capacites WHERE categorie = '{cat}'",
        "solution": f"SELECT nom FROM capacites WHERE categorie = '{cat}'",
        "compare": "first_col", "pokemon_id": None,
    }

def n1_14():
    seuil = _rc([50, 60, 70, 80])
    return {
        "niveau": 1, "categorie": "WHERE puissance",
        "titre": f"CAPACITÉS PUISSANTES (> {seuil})",
        "description": (
            f"Sélectionne le <code>nom</code> des capacités\n"
            f"dont la <code>puissance</code> est supérieure à <strong>{seuil}</strong>.\n"
            f"<small>Attention : certaines capacités ont puissance NULL.</small>"
        ),
        "indice": f"SELECT nom FROM capacites WHERE puissance > {seuil}",
        "solution": f"SELECT nom FROM capacites WHERE puissance > {seuil}",
        "compare": "first_col", "pokemon_id": None,
    }

def n1_15():
    t = _t1()
    return {
        "niveau": 1, "categorie": "WHERE combiné",
        "titre": f"NON-LÉGENDAIRES DE TYPE {t.upper()}",
        "description": (
            f"Sélectionne le <code>nom</code> des Pokémon\n"
            f"de <code>type1</code> <strong>'{t}'</strong>\n"
            f"qui <strong>ne sont pas</strong> légendaires (<code>est_legendaire = 0</code>)."
        ),
        "indice": f"SELECT nom FROM pokemon WHERE type1 = '{t}' AND est_legendaire = 0",
        "solution": f"SELECT nom FROM pokemon WHERE type1 = '{t}' AND est_legendaire = 0",
        "compare": "names", "pokemon_id": None,
    }

# ── NIVEAU 2 — ORDER BY, BETWEEN, AND/OR, agrégats, GROUP BY (20) ─────────────

def n2_01():
    stat = _s(); label = _sl(stat); n = _n(3, 10)
    return {
        "niveau": 2, "categorie": "ORDER BY + LIMIT",
        "titre": f"TOP {n} EN {label}",
        "description": (
            f"Sélectionne le <code>nom</code> des <strong>{n}</strong> Pokémon\n"
            f"avec les valeurs de <code>{stat}</code> les plus <strong>élevées</strong>.\n"
            f"<small>Utilise ORDER BY … DESC LIMIT {n}.</small>"
        ),
        "indice": f"SELECT nom FROM pokemon ORDER BY {stat} DESC LIMIT {n}",
        "solution": f"SELECT nom FROM pokemon ORDER BY {stat} DESC LIMIT {n}",
        "compare": "names", "pokemon_id": None,
    }

def n2_02():
    stat = _s(); label = _sl(stat); n = _n(3, 10)
    return {
        "niveau": 2, "categorie": "ORDER BY + LIMIT",
        "titre": f"LES {n} PLUS FAIBLES EN {label}",
        "description": (
            f"Sélectionne le <code>nom</code> des <strong>{n}</strong> Pokémon\n"
            f"avec les valeurs de <code>{stat}</code> les plus <strong>faibles</strong>.\n"
            f"<small>Utilise ORDER BY … ASC LIMIT {n}.</small>"
        ),
        "indice": f"SELECT nom FROM pokemon ORDER BY {stat} ASC LIMIT {n}",
        "solution": f"SELECT nom FROM pokemon ORDER BY {stat} ASC LIMIT {n}",
        "compare": "names", "pokemon_id": None,
    }

def n2_03():
    stat = _s(); label = _sl(stat); lo, hi = _bv(stat)
    return {
        "niveau": 2, "categorie": "BETWEEN",
        "titre": f"{label} ENTRE {lo} ET {hi}",
        "description": (
            f"Sélectionne le <code>nom</code> des Pokémon\n"
            f"dont <code>{stat}</code> est compris entre\n"
            f"<strong>{lo}</strong> et <strong>{hi}</strong> (bornes incluses).\n"
            f"<small>Utilise BETWEEN … AND …</small>"
        ),
        "indice": f"SELECT nom FROM pokemon WHERE {stat} BETWEEN {lo} AND {hi}",
        "solution": f"SELECT nom FROM pokemon WHERE {stat} BETWEEN {lo} AND {hi}",
        "compare": "names", "pokemon_id": None,
    }

def n2_04():
    t = _t1(); stat = _s(); label = _sl(stat); seuil = _sv(stat)
    return {
        "niveau": 2, "categorie": "AND",
        "titre": f"TYPE {t.upper()} ET {label} > {seuil}",
        "description": (
            f"Sélectionne le <code>nom</code> des Pokémon\n"
            f"de <code>type1</code> <strong>'{t}'</strong>\n"
            f"<strong>ET</strong> dont <code>{stat}</code> > {seuil}."
        ),
        "indice": f"SELECT nom FROM pokemon WHERE type1 = '{t}' AND {stat} > {seuil}",
        "solution": f"SELECT nom FROM pokemon WHERE type1 = '{t}' AND {stat} > {seuil}",
        "compare": "names", "pokemon_id": None,
    }

def n2_05():
    d = _data(); t1 = _rc(d["types1"]); t2 = _rc([x for x in d["types1"] if x != t1])
    return {
        "niveau": 2, "categorie": "OR",
        "titre": f"TYPE {t1.upper()} OU {t2.upper()}",
        "description": (
            f"Sélectionne le <code>nom</code> des Pokémon\n"
            f"dont le <code>type1</code> est <strong>'{t1}'</strong>\n"
            f"<strong>OU</strong> <strong>'{t2}'</strong>."
        ),
        "indice": f"SELECT nom FROM pokemon WHERE type1 = '{t1}' OR type1 = '{t2}'",
        "solution": f"SELECT nom FROM pokemon WHERE type1 = '{t1}' OR type1 = '{t2}'",
        "compare": "names", "pokemon_id": None,
    }

def n2_06():
    t = _rc(["Eau","Feu","Plante","Psy","Poison","Vol","Normal","Roche"])
    return {
        "niveau": 2, "categorie": "OR sur types",
        "titre": f"PORTEURS DU TYPE {t.upper()}",
        "description": (
            f"Sélectionne le <code>nom</code> des Pokémon\n"
            f"dont <code>type1</code> = <strong>'{t}'</strong>\n"
            f"<strong>OU</strong> <code>type2</code> = <strong>'{t}'</strong>."
        ),
        "indice": f"SELECT nom FROM pokemon WHERE type1 = '{t}' OR type2 = '{t}'",
        "solution": f"SELECT nom FROM pokemon WHERE type1 = '{t}' OR type2 = '{t}'",
        "compare": "names", "pokemon_id": None,
    }

def n2_07():
    stat = _s(); label = _sl(stat)
    lo, hi = _bv(stat)
    seuil = (lo + hi) // 2
    return {
        "niveau": 2, "categorie": "AND combiné",
        "titre": f"{lo} < {label} < {hi}",
        "description": (
            f"Sélectionne le <code>nom</code> des Pokémon\n"
            f"dont <code>{stat}</code> est <strong>strictement</strong>\n"
            f"supérieur à {lo} <strong>ET</strong> inférieur à {hi}.\n"
            f"<small>Sans BETWEEN — utilise deux conditions AND.</small>"
        ),
        "indice": f"SELECT nom FROM pokemon WHERE {stat} > {lo} AND {stat} < {hi}",
        "solution": f"SELECT nom FROM pokemon WHERE {stat} > {lo} AND {stat} < {hi}",
        "compare": "names", "pokemon_id": None,
    }

def n2_08():
    t = _t1()
    return {
        "niveau": 2, "categorie": "COUNT",
        "titre": f"COMBIEN DE {t.upper()} ?",
        "description": (
            f"Compte le nombre total de Pokémon\n"
            f"dont le <code>type1</code> est <strong>'{t}'</strong>.\n"
            f"<small>Retourne une seule valeur avec COUNT(*).</small>"
        ),
        "indice": f"SELECT COUNT(*) FROM pokemon WHERE type1 = '{t}'",
        "solution": f"SELECT COUNT(*) FROM pokemon WHERE type1 = '{t}'",
        "compare": "full", "pokemon_id": None,
    }

def n2_09():
    stat = _s(); label = _sl(stat)
    return {
        "niveau": 2, "categorie": "AVG",
        "titre": f"MOYENNE DE {label}",
        "description": (
            f"Calcule la <strong>moyenne</strong> de <code>{stat}</code>\n"
            f"pour tous les Pokémon.\n"
            f"<small>Retourne ROUND(AVG({stat}), 1) pour 1 décimale.</small>"
        ),
        "indice": f"SELECT ROUND(AVG({stat}), 1) FROM pokemon",
        "solution": f"SELECT ROUND(AVG({stat}), 1) FROM pokemon",
        "compare": "full", "pokemon_id": None,
    }

def n2_10():
    stat = _s(); label = _sl(stat)
    return {
        "niveau": 2, "categorie": "MAX / MIN",
        "titre": f"MAX ET MIN DE {label}",
        "description": (
            f"Retourne le <strong>maximum</strong> puis le <strong>minimum</strong>\n"
            f"de <code>{stat}</code> pour tous les Pokémon.\n"
            f"<small>Sélectionne MAX({stat}), MIN({stat}) dans cet ordre.</small>"
        ),
        "indice": f"SELECT MAX({stat}), MIN({stat}) FROM pokemon",
        "solution": f"SELECT MAX({stat}), MIN({stat}) FROM pokemon",
        "compare": "full", "pokemon_id": None,
    }

def n2_11():
    t = _t1(); stat = _s(); label = _sl(stat)
    return {
        "niveau": 2, "categorie": "AVG + WHERE",
        "titre": f"MOYENNE {label} — TYPE {t.upper()}",
        "description": (
            f"Calcule la <strong>moyenne</strong> de <code>{stat}</code>\n"
            f"uniquement pour les Pokémon de type1 <strong>'{t}'</strong>.\n"
            f"<small>Retourne ROUND(AVG({stat}), 1).</small>"
        ),
        "indice": f"SELECT ROUND(AVG({stat}), 1) FROM pokemon WHERE type1 = '{t}'",
        "solution": f"SELECT ROUND(AVG({stat}), 1) FROM pokemon WHERE type1 = '{t}'",
        "compare": "full", "pokemon_id": None,
    }

def n2_12():
    t = _t1(); stat = _s(); label = _sl(stat)
    return {
        "niveau": 2, "categorie": "SUM",
        "titre": f"SOMME {label} — TYPE {t.upper()}",
        "description": (
            f"Calcule la <strong>somme totale</strong> de <code>{stat}</code>\n"
            f"pour tous les Pokémon de <code>type1</code> <strong>'{t}'</strong>."
        ),
        "indice": f"SELECT SUM({stat}) FROM pokemon WHERE type1 = '{t}'",
        "solution": f"SELECT SUM({stat}) FROM pokemon WHERE type1 = '{t}'",
        "compare": "full", "pokemon_id": None,
    }

def n2_13():
    stat = _s(); label = _sl(stat)
    return {
        "niveau": 2, "categorie": "MAX + WHERE",
        "titre": f"MAX {label} DES LÉGENDAIRES",
        "description": (
            f"Trouve le <strong>maximum</strong> de <code>{stat}</code>\n"
            f"parmi les Pokémon légendaires (<code>est_legendaire = 1</code>)."
        ),
        "indice": f"SELECT MAX({stat}) FROM pokemon WHERE est_legendaire = 1",
        "solution": f"SELECT MAX({stat}) FROM pokemon WHERE est_legendaire = 1",
        "compare": "full", "pokemon_id": 150,
    }

def n2_14():
    return {
        "niveau": 2, "categorie": "GROUP BY",
        "titre": "POKÉMON PAR TYPE — COMPTAGE",
        "description": (
            "Retourne le <code>type1</code> et le nombre de Pokémon\n"
            "(<code>COUNT(*)</code>) pour chaque type,\n"
            "trié par <code>type1</code> alphabétiquement."
        ),
        "indice": "SELECT type1, COUNT(*) FROM pokemon GROUP BY type1 ORDER BY type1",
        "solution": "SELECT type1, COUNT(*) FROM pokemon GROUP BY type1 ORDER BY type1",
        "compare": "aggregate", "pokemon_id": None,
    }

def n2_15():
    stat = _s(); label = _sl(stat)
    return {
        "niveau": 2, "categorie": "GROUP BY + MAX",
        "titre": f"MAX {label} PAR TYPE",
        "description": (
            f"Retourne le <code>type1</code> et le <code>MAX({stat})</code>\n"
            f"pour chaque type, trié par <code>type1</code>."
        ),
        "indice": f"SELECT type1, MAX({stat}) FROM pokemon GROUP BY type1 ORDER BY type1",
        "solution": f"SELECT type1, MAX({stat}) FROM pokemon GROUP BY type1 ORDER BY type1",
        "compare": "aggregate", "pokemon_id": None,
    }

def n2_16():
    stat = _s(); label = _sl(stat)
    return {
        "niveau": 2, "categorie": "GROUP BY + MIN",
        "titre": f"MIN {label} PAR TYPE",
        "description": (
            f"Retourne le <code>type1</code> et le <code>MIN({stat})</code>\n"
            f"pour chaque type, trié par <code>type1</code>."
        ),
        "indice": f"SELECT type1, MIN({stat}) FROM pokemon GROUP BY type1 ORDER BY type1",
        "solution": f"SELECT type1, MIN({stat}) FROM pokemon GROUP BY type1 ORDER BY type1",
        "compare": "aggregate", "pokemon_id": None,
    }

def n2_17():
    n = _n(3, 8)
    return {
        "niveau": 2, "categorie": "GROUP BY + ORDER",
        "titre": f"TOP {n} TYPES LES PLUS PEUPLÉS",
        "description": (
            f"Retourne le <code>type1</code> et le nombre de Pokémon\n"
            f"par type, ordonné du <strong>plus peuplé au moins peuplé</strong>,\n"
            f"et limité aux <strong>{n} premiers</strong>."
        ),
        "indice": f"SELECT type1, COUNT(*) FROM pokemon GROUP BY type1 ORDER BY COUNT(*) DESC LIMIT {n}",
        "solution": f"SELECT type1, COUNT(*) FROM pokemon GROUP BY type1 ORDER BY COUNT(*) DESC LIMIT {n}",
        "compare": "aggregate", "pokemon_id": None,
    }

def n2_18():
    letter = _rc(list("ABCDEFGHKLMNOPRST")); t = _t1()
    return {
        "niveau": 2, "categorie": "LIKE + AND",
        "titre": f"TYPE {t.upper()} AVEC '{letter}' DANS LE NOM",
        "description": (
            f"Sélectionne le <code>nom</code> des Pokémon\n"
            f"de <code>type1</code> <strong>'{t}'</strong>\n"
            f"<strong>ET</strong> dont le nom contient <strong>'{letter}'</strong>."
        ),
        "indice": f"SELECT nom FROM pokemon WHERE type1 = '{t}' AND nom LIKE '%{letter}%'",
        "solution": f"SELECT nom FROM pokemon WHERE type1 = '{t}' AND nom LIKE '%{letter}%'",
        "compare": "names", "pokemon_id": None,
    }

def n2_19():
    stat = _s(); label = _sl(stat); t = _t1(); lo, hi = _bv(stat)
    return {
        "niveau": 2, "categorie": "BETWEEN + AND",
        "titre": f"TYPE {t.upper()} — {label} ENTRE {lo} ET {hi}",
        "description": (
            f"Sélectionne le <code>nom</code> des Pokémon\n"
            f"de type1 <strong>'{t}'</strong>\n"
            f"dont <code>{stat}</code> est entre <strong>{lo}</strong> et <strong>{hi}</strong>."
        ),
        "indice": f"SELECT nom FROM pokemon WHERE type1 = '{t}' AND {stat} BETWEEN {lo} AND {hi}",
        "solution": f"SELECT nom FROM pokemon WHERE type1 = '{t}' AND {stat} BETWEEN {lo} AND {hi}",
        "compare": "names", "pokemon_id": None,
    }

def n2_20():
    stat = _s(); label = _sl(stat); seuil = _sv(stat)
    return {
        "niveau": 2, "categorie": "ORDER BY filtré",
        "titre": f"{label} > {seuil} — TRIÉ",
        "description": (
            f"Sélectionne le <code>nom</code> des Pokémon\n"
            f"dont <code>{stat}</code> > {seuil},\n"
            f"triés par <code>{stat}</code> <strong>décroissant</strong>."
        ),
        "indice": f"SELECT nom FROM pokemon WHERE {stat} > {seuil} ORDER BY {stat} DESC",
        "solution": f"SELECT nom FROM pokemon WHERE {stat} > {seuil} ORDER BY {stat} DESC",
        "compare": "names", "pokemon_id": None,
    }

# ── NIVEAU 3 — HAVING, JOINs (15) ────────────────────────────────────────────

def n3_01():
    n = _n(5, 12)
    return {
        "niveau": 3, "categorie": "GROUP BY + HAVING",
        "titre": f"TYPES AVEC PLUS DE {n} POKÉMON",
        "description": (
            f"Sélectionne le <code>type1</code> des types\n"
            f"qui comptent <strong>strictement plus de {n}</strong> Pokémon.\n"
            f"<small>GROUP BY … HAVING COUNT(*) > {n}</small>"
        ),
        "indice": f"SELECT type1 FROM pokemon GROUP BY type1 HAVING COUNT(*) > {n}",
        "solution": f"SELECT type1 FROM pokemon GROUP BY type1 HAVING COUNT(*) > {n}",
        "compare": "first_col", "pokemon_id": None,
    }

def n3_02():
    stat = _s(); label = _sl(stat)
    seuil = _rc([50, 55, 60, 65, 70])
    return {
        "niveau": 3, "categorie": "GROUP BY + HAVING AVG",
        "titre": f"TYPES OÙ LA MOYENNE {label} > {seuil}",
        "description": (
            f"Sélectionne le <code>type1</code> des types\n"
            f"dont la <strong>moyenne de {label.lower()}</strong>\n"
            f"est strictement supérieure à <strong>{seuil}</strong>.\n"
            f"<small>GROUP BY … HAVING AVG({stat}) > {seuil}</small>"
        ),
        "indice": f"SELECT type1 FROM pokemon GROUP BY type1 HAVING AVG({stat}) > {seuil}",
        "solution": f"SELECT type1 FROM pokemon GROUP BY type1 HAVING AVG({stat}) > {seuil}",
        "compare": "first_col", "pokemon_id": None,
    }

def n3_03():
    stat = _s(); label = _sl(stat)
    seuil = _rc([90, 100, 110, 120])
    return {
        "niveau": 3, "categorie": "GROUP BY + HAVING MAX",
        "titre": f"TYPES AVEC MAX {label} >= {seuil}",
        "description": (
            f"Sélectionne le <code>type1</code> des types\n"
            f"dont le <strong>maximum de {label.lower()}</strong>\n"
            f"est supérieur ou égal à <strong>{seuil}</strong>."
        ),
        "indice": f"SELECT type1 FROM pokemon GROUP BY type1 HAVING MAX({stat}) >= {seuil}",
        "solution": f"SELECT type1 FROM pokemon GROUP BY type1 HAVING MAX({stat}) >= {seuil}",
        "compare": "first_col", "pokemon_id": None,
    }

def n3_04():
    cap = _cap(); cap_sql = _esc(cap)
    return {
        "niveau": 3, "categorie": "JOIN simple",
        "titre": f"POKÉMON CONNAISSANT {cap.upper()}",
        "description": (
            f"Sélectionne le <code>nom</code> distinct des Pokémon\n"
            f"qui connaissent la capacité <strong>'{cap}'</strong>.\n"
            f"<small>JOIN pokemon → pokemon_capacites → capacites</small>"
        ),
        "indice": (
            f"SELECT DISTINCT p.nom FROM pokemon p\n"
            f"JOIN pokemon_capacites pc ON p.id = pc.pokemon_id\n"
            f"JOIN capacites c ON pc.capacite_id = c.id\n"
            f"WHERE c.nom = '{cap_sql}'"
        ),
        "solution": (
            f"SELECT DISTINCT p.nom FROM pokemon p "
            f"JOIN pokemon_capacites pc ON p.id = pc.pokemon_id "
            f"JOIN capacites c ON pc.capacite_id = c.id "
            f"WHERE c.nom = '{cap_sql}'"
        ),
        "compare": "names", "pokemon_id": None,
    }

def n3_05():
    seuil = _rc([70, 80, 90, 100])
    return {
        "niveau": 3, "categorie": "JOIN + WHERE",
        "titre": f"POKÉMON AVEC CAPACITÉ PUISSANCE > {seuil}",
        "description": (
            f"Sélectionne le <code>nom</code> distinct des Pokémon\n"
            f"qui connaissent au moins une capacité\n"
            f"de <code>puissance</code> > <strong>{seuil}</strong>."
        ),
        "indice": (
            f"SELECT DISTINCT p.nom FROM pokemon p\n"
            f"JOIN pokemon_capacites pc ON p.id = pc.pokemon_id\n"
            f"JOIN capacites c ON pc.capacite_id = c.id\n"
            f"WHERE c.puissance > {seuil}"
        ),
        "solution": (
            f"SELECT DISTINCT p.nom FROM pokemon p "
            f"JOIN pokemon_capacites pc ON p.id = pc.pokemon_id "
            f"JOIN capacites c ON pc.capacite_id = c.id "
            f"WHERE c.puissance > {seuil}"
        ),
        "compare": "names", "pokemon_id": None,
    }

def n3_06():
    t = _t1()
    return {
        "niveau": 3, "categorie": "JOIN 4 tables",
        "titre": f"POKÉMON AVEC CAPACITÉ DE TYPE {t.upper()}",
        "description": (
            f"Sélectionne le <code>nom</code> distinct des Pokémon\n"
            f"qui connaissent au moins une capacité de type <strong>'{t}'</strong>.\n"
            f"<small>JOIN : pokemon → pokemon_capacites → capacites → types</small>"
        ),
        "indice": (
            f"SELECT DISTINCT p.nom FROM pokemon p\n"
            f"JOIN pokemon_capacites pc ON p.id = pc.pokemon_id\n"
            f"JOIN capacites c ON pc.capacite_id = c.id\n"
            f"JOIN types t ON c.type_id = t.id\n"
            f"WHERE t.nom = '{t}'"
        ),
        "solution": (
            f"SELECT DISTINCT p.nom FROM pokemon p "
            f"JOIN pokemon_capacites pc ON p.id = pc.pokemon_id "
            f"JOIN capacites c ON pc.capacite_id = c.id "
            f"JOIN types t ON c.type_id = t.id "
            f"WHERE t.nom = '{t}'"
        ),
        "compare": "names", "pokemon_id": None,
    }

def n3_07():
    pok = _pok(); pok_sql = _esc(pok)
    return {
        "niveau": 3, "categorie": "JOIN + WHERE pokémon",
        "titre": f"CAPACITÉS DE {pok.upper()}",
        "description": (
            f"Sélectionne le <code>nom</code> de toutes les capacités\n"
            f"que connaît le Pokémon <strong>'{pok}'</strong>.\n"
            f"<small>Résultat : noms de capacités, pas de pokemon.</small>"
        ),
        "indice": (
            f"SELECT c.nom FROM capacites c\n"
            f"JOIN pokemon_capacites pc ON c.id = pc.capacite_id\n"
            f"JOIN pokemon p ON pc.pokemon_id = p.id\n"
            f"WHERE p.nom = '{pok_sql}'"
        ),
        "solution": (
            f"SELECT c.nom FROM capacites c "
            f"JOIN pokemon_capacites pc ON c.id = pc.capacite_id "
            f"JOIN pokemon p ON pc.pokemon_id = p.id "
            f"WHERE p.nom = '{pok_sql}'"
        ),
        "compare": "first_col", "pokemon_id": None,
    }

def n3_08():
    cat = _cat()
    return {
        "niveau": 3, "categorie": "JOIN + catégorie",
        "titre": f"POKÉMON AVEC CAPACITÉ {cat.upper()}",
        "description": (
            f"Sélectionne le <code>nom</code> distinct des Pokémon\n"
            f"qui connaissent au moins une capacité\n"
            f"de catégorie <strong>'{cat}'</strong>."
        ),
        "indice": (
            f"SELECT DISTINCT p.nom FROM pokemon p\n"
            f"JOIN pokemon_capacites pc ON p.id = pc.pokemon_id\n"
            f"JOIN capacites c ON pc.capacite_id = c.id\n"
            f"WHERE c.categorie = '{cat}'"
        ),
        "solution": (
            f"SELECT DISTINCT p.nom FROM pokemon p "
            f"JOIN pokemon_capacites pc ON p.id = pc.pokemon_id "
            f"JOIN capacites c ON pc.capacite_id = c.id "
            f"WHERE c.categorie = '{cat}'"
        ),
        "compare": "names", "pokemon_id": None,
    }

def n3_09():
    t = _t1(); seuil = _rc([60, 70, 80])
    return {
        "niveau": 3, "categorie": "JOIN + AND",
        "titre": f"TYPE {t.upper()} + CAPACITÉ PUISSANTE (>= {seuil})",
        "description": (
            f"Sélectionne le <code>nom</code> distinct des Pokémon\n"
            f"de <code>type1</code> <strong>'{t}'</strong>\n"
            f"qui connaissent une capacité de <code>puissance</code> >= <strong>{seuil}</strong>."
        ),
        "indice": (
            f"SELECT DISTINCT p.nom FROM pokemon p\n"
            f"JOIN pokemon_capacites pc ON p.id = pc.pokemon_id\n"
            f"JOIN capacites c ON pc.capacite_id = c.id\n"
            f"WHERE p.type1 = '{t}' AND c.puissance >= {seuil}"
        ),
        "solution": (
            f"SELECT DISTINCT p.nom FROM pokemon p "
            f"JOIN pokemon_capacites pc ON p.id = pc.pokemon_id "
            f"JOIN capacites c ON pc.capacite_id = c.id "
            f"WHERE p.type1 = '{t}' AND c.puissance >= {seuil}"
        ),
        "compare": "names", "pokemon_id": None,
    }

def n3_10():
    n = _n(3, 8)
    return {
        "niveau": 3, "categorie": "JOIN + GROUP BY",
        "titre": f"TOP {n} CAPACITÉS LES PLUS APPRISES",
        "description": (
            f"Sélectionne le <code>nom</code> des <strong>{n}</strong> capacités\n"
            f"connues par le plus grand nombre de Pokémon.\n"
            f"<small>Résultat : noms de capacités uniquement.</small>"
        ),
        "indice": (
            f"SELECT c.nom FROM capacites c\n"
            f"JOIN pokemon_capacites pc ON c.id = pc.capacite_id\n"
            f"GROUP BY c.id ORDER BY COUNT(*) DESC LIMIT {n}"
        ),
        "solution": (
            f"SELECT c.nom FROM capacites c "
            f"JOIN pokemon_capacites pc ON c.id = pc.capacite_id "
            f"GROUP BY c.id ORDER BY COUNT(*) DESC LIMIT {n}"
        ),
        "compare": "first_col", "pokemon_id": None,
    }

def n3_11():
    t = _t1()
    return {
        "niveau": 3, "categorie": "JOIN + GROUP BY",
        "titre": f"TYPES DES CAPACITÉS CONNUES PAR TYPE {t.upper()}",
        "description": (
            f"Sélectionne les <code>type1</code> distincts des Pokémon\n"
            f"qui connaissent au moins une capacité de type <strong>'{t}'</strong>.\n"
            f"<small>Résultat : liste de types de pokemon, pas de noms.</small>"
        ),
        "indice": (
            f"SELECT DISTINCT p.type1 FROM pokemon p\n"
            f"JOIN pokemon_capacites pc ON p.id = pc.pokemon_id\n"
            f"JOIN capacites c ON pc.capacite_id = c.id\n"
            f"JOIN types t ON c.type_id = t.id\n"
            f"WHERE t.nom = '{t}'"
        ),
        "solution": (
            f"SELECT DISTINCT p.type1 FROM pokemon p "
            f"JOIN pokemon_capacites pc ON p.id = pc.pokemon_id "
            f"JOIN capacites c ON pc.capacite_id = c.id "
            f"JOIN types t ON c.type_id = t.id "
            f"WHERE t.nom = '{t}'"
        ),
        "compare": "first_col", "pokemon_id": None,
    }

def n3_12():
    cat = _cat()
    return {
        "niveau": 3, "categorie": "JOIN + HAVING",
        "titre": f"POKÉMON AVEC 3+ CAPACITÉS {cat.upper()}",
        "description": (
            f"Sélectionne le <code>nom</code> des Pokémon\n"
            f"qui connaissent <strong>au moins 2</strong> capacités\n"
            f"de catégorie <strong>'{cat}'</strong>.\n"
            f"<small>GROUP BY p.id HAVING COUNT(*) >= 2</small>"
        ),
        "indice": (
            f"SELECT p.nom FROM pokemon p\n"
            f"JOIN pokemon_capacites pc ON p.id = pc.pokemon_id\n"
            f"JOIN capacites c ON pc.capacite_id = c.id\n"
            f"WHERE c.categorie = '{cat}'\n"
            f"GROUP BY p.id HAVING COUNT(*) >= 2"
        ),
        "solution": (
            f"SELECT p.nom FROM pokemon p "
            f"JOIN pokemon_capacites pc ON p.id = pc.pokemon_id "
            f"JOIN capacites c ON pc.capacite_id = c.id "
            f"WHERE c.categorie = '{cat}' "
            f"GROUP BY p.id HAVING COUNT(*) >= 2"
        ),
        "compare": "names", "pokemon_id": None,
    }

def n3_13():
    seuil = _rc([60, 70, 80])
    return {
        "niveau": 3, "categorie": "JOIN + HAVING",
        "titre": f"POKÉMON AVEC 2+ CAPACITÉS PUISSANTES (> {seuil})",
        "description": (
            f"Sélectionne le <code>nom</code> des Pokémon\n"
            f"connaissant <strong>au moins 2</strong> capacités\n"
            f"de <code>puissance</code> > <strong>{seuil}</strong>."
        ),
        "indice": (
            f"SELECT p.nom FROM pokemon p\n"
            f"JOIN pokemon_capacites pc ON p.id = pc.pokemon_id\n"
            f"JOIN capacites c ON pc.capacite_id = c.id\n"
            f"WHERE c.puissance > {seuil}\n"
            f"GROUP BY p.id HAVING COUNT(*) >= 2"
        ),
        "solution": (
            f"SELECT p.nom FROM pokemon p "
            f"JOIN pokemon_capacites pc ON p.id = pc.pokemon_id "
            f"JOIN capacites c ON pc.capacite_id = c.id "
            f"WHERE c.puissance > {seuil} "
            f"GROUP BY p.id HAVING COUNT(*) >= 2"
        ),
        "compare": "names", "pokemon_id": None,
    }

def n3_14():
    t = _t1()
    return {
        "niveau": 3, "categorie": "JOIN + GROUP BY + ORDER",
        "titre": f"CAPACITÉS DU TYPE {t.upper()} ET LEUR NOMBRE",
        "description": (
            f"Pour chaque capacité de type <strong>'{t}'</strong>,\n"
            f"retourne son <code>nom</code> et le nombre de Pokémon\n"
            f"(<code>COUNT</code>) qui la connaissent, trié par nom."
        ),
        "indice": (
            f"SELECT c.nom, COUNT(pc.pokemon_id) FROM capacites c\n"
            f"JOIN pokemon_capacites pc ON c.id = pc.capacite_id\n"
            f"JOIN types t ON c.type_id = t.id\n"
            f"WHERE t.nom = '{t}' GROUP BY c.id ORDER BY c.nom"
        ),
        "solution": (
            f"SELECT c.nom, COUNT(pc.pokemon_id) FROM capacites c "
            f"JOIN pokemon_capacites pc ON c.id = pc.capacite_id "
            f"JOIN types t ON c.type_id = t.id "
            f"WHERE t.nom = '{t}' GROUP BY c.id ORDER BY c.nom"
        ),
        "compare": "aggregate", "pokemon_id": None,
    }

def n3_15():
    t = _t1()
    return {
        "niveau": 3, "categorie": "JOIN + WHERE type1",
        "titre": f"CAPACITÉS CONNUES PAR LES {t.upper()}",
        "description": (
            f"Sélectionne le <code>nom</code> distinct de toutes les capacités\n"
            f"connues par au moins un Pokémon de <code>type1</code> <strong>'{t}'</strong>."
        ),
        "indice": (
            f"SELECT DISTINCT c.nom FROM capacites c\n"
            f"JOIN pokemon_capacites pc ON c.id = pc.capacite_id\n"
            f"JOIN pokemon p ON pc.pokemon_id = p.id\n"
            f"WHERE p.type1 = '{t}'"
        ),
        "solution": (
            f"SELECT DISTINCT c.nom FROM capacites c "
            f"JOIN pokemon_capacites pc ON c.id = pc.capacite_id "
            f"JOIN pokemon p ON pc.pokemon_id = p.id "
            f"WHERE p.type1 = '{t}'"
        ),
        "compare": "first_col", "pokemon_id": None,
    }

# ── NIVEAU 4 — Sous-requêtes, EXISTS (10) ─────────────────────────────────────

def n4_01():
    stat = _s(); label = _sl(stat)
    return {
        "niveau": 4, "categorie": "Sous-requête AVG",
        "titre": f"AU-DESSUS DE LA MOYENNE — {label}",
        "description": (
            f"Sélectionne le <code>nom</code> des Pokémon\n"
            f"dont <code>{stat}</code> est supérieur\n"
            f"à la <strong>moyenne générale</strong> de <code>{stat}</code>.\n"
            f"<small>Utilise une sous-requête : WHERE {stat} > (SELECT AVG...)</small>"
        ),
        "indice": f"SELECT nom FROM pokemon WHERE {stat} > (SELECT AVG({stat}) FROM pokemon)",
        "solution": f"SELECT nom FROM pokemon WHERE {stat} > (SELECT AVG({stat}) FROM pokemon)",
        "compare": "names", "pokemon_id": None,
    }

def n4_02():
    stat = _s(); label = _sl(stat)
    return {
        "niveau": 4, "categorie": "Sous-requête MAX",
        "titre": f"LE MEILLEUR EN {label}",
        "description": (
            f"Sélectionne le <code>nom</code> du (ou des) Pokémon\n"
            f"dont <code>{stat}</code> est égal au\n"
            f"<strong>maximum absolu</strong> de cette stat.\n"
            f"<small>WHERE {stat} = (SELECT MAX({stat}) FROM ...)</small>"
        ),
        "indice": f"SELECT nom FROM pokemon WHERE {stat} = (SELECT MAX({stat}) FROM pokemon)",
        "solution": f"SELECT nom FROM pokemon WHERE {stat} = (SELECT MAX({stat}) FROM pokemon)",
        "compare": "names", "pokemon_id": None,
    }

def n4_03():
    t = _t1(); stat = _s(); label = _sl(stat)
    return {
        "niveau": 4, "categorie": "Sous-requête MAX par type",
        "titre": f"MEILLEUR {label} DU TYPE {t.upper()}",
        "description": (
            f"Sélectionne le <code>nom</code> du Pokémon de type1 <strong>'{t}'</strong>\n"
            f"dont <code>{stat}</code> est le maximum de son type.\n"
            f"<small>WHERE type1 = '{t}' AND {stat} = (SELECT MAX...)</small>"
        ),
        "indice": (
            f"SELECT nom FROM pokemon\n"
            f"WHERE type1 = '{t}'\n"
            f"AND {stat} = (SELECT MAX({stat}) FROM pokemon WHERE type1 = '{t}')"
        ),
        "solution": (
            f"SELECT nom FROM pokemon "
            f"WHERE type1 = '{t}' "
            f"AND {stat} = (SELECT MAX({stat}) FROM pokemon WHERE type1 = '{t}')"
        ),
        "compare": "names", "pokemon_id": None,
    }

def n4_04():
    # Pick low-stat pokemon so result is always non-empty
    ref = _rc([("Magicarpe", "pv", 20), ("Fantominus", "pv", 30),
               ("Magicarpe", "attaque", 10), ("Abra", "defense", 15),
               ("Ronflex", "vitesse", 30), ("Amonistar", "vitesse", 35)])
    pok_name, stat, _ = ref; label = _sl(stat); pok_sql = _esc(pok_name)
    return {
        "niveau": 4, "categorie": "Sous-requête",
        "titre": f"PLUS DE {label} QUE {pok_name.upper()}",
        "description": (
            f"Sélectionne le <code>nom</code> des Pokémon\n"
            f"dont <code>{stat}</code> est strictement supérieur\n"
            f"à celui de <strong>{pok_name}</strong>.\n"
            f"<small>WHERE {stat} > (SELECT {stat} FROM pokemon WHERE nom = '{pok_sql}')</small>"
        ),
        "indice": (
            f"SELECT nom FROM pokemon\n"
            f"WHERE {stat} > (SELECT {stat} FROM pokemon WHERE nom = '{pok_sql}')"
        ),
        "solution": (
            f"SELECT nom FROM pokemon "
            f"WHERE {stat} > (SELECT {stat} FROM pokemon WHERE nom = '{pok_sql}')"
        ),
        "compare": "names", "pokemon_id": None,
    }

def n4_05():
    n = _n(5, 14)
    stat = _s(); label = _sl(stat)
    return {
        "niveau": 4, "categorie": "Sous-requête OFFSET",
        "titre": f"TOP {n} EN {label} — SOUS-REQUÊTE",
        "description": (
            f"Sélectionne le <code>nom</code> des Pokémon\n"
            f"appartenant au <strong>top {n}</strong> en <code>{stat}</code>,\n"
            f"sans utiliser LIMIT directement.\n"
            f"<small>WHERE {stat} >= (SELECT {stat} FROM pokemon ORDER BY {stat} DESC LIMIT 1 OFFSET {n-1})</small>"
        ),
        "indice": (
            f"SELECT nom FROM pokemon\n"
            f"WHERE {stat} >= (\n"
            f"  SELECT {stat} FROM pokemon ORDER BY {stat} DESC LIMIT 1 OFFSET {n-1}\n"
            f")"
        ),
        "solution": (
            f"SELECT nom FROM pokemon "
            f"WHERE {stat} >= (SELECT {stat} FROM pokemon ORDER BY {stat} DESC LIMIT 1 OFFSET {n-1})"
        ),
        "compare": "names", "pokemon_id": None,
    }

def n4_06():
    n = _n(3, 10)
    return {
        "niveau": 4, "categorie": "Sous-requête IN",
        "titre": f"POKÉMON DES TYPES LES PLUS PEUPLÉS (> {n})",
        "description": (
            f"Sélectionne le <code>nom</code> des Pokémon\n"
            f"dont le <code>type1</code> compte <strong>plus de {n}</strong> Pokémon.\n"
            f"<small>WHERE type1 IN (SELECT type1 ... HAVING COUNT > {n})</small>"
        ),
        "indice": (
            f"SELECT nom FROM pokemon\n"
            f"WHERE type1 IN (\n"
            f"  SELECT type1 FROM pokemon GROUP BY type1 HAVING COUNT(*) > {n}\n"
            f")"
        ),
        "solution": (
            f"SELECT nom FROM pokemon "
            f"WHERE type1 IN (SELECT type1 FROM pokemon GROUP BY type1 HAVING COUNT(*) > {n})"
        ),
        "compare": "names", "pokemon_id": None,
    }

def n4_07():
    seuil = _rc([70, 80, 90])
    return {
        "niveau": 4, "categorie": "EXISTS",
        "titre": f"POKÉMON AVEC AU MOINS UNE CAPACITÉ >= {seuil}",
        "description": (
            f"Sélectionne le <code>nom</code> des Pokémon\n"
            f"pour lesquels il <strong>existe</strong> au moins une capacité\n"
            f"de <code>puissance</code> >= <strong>{seuil}</strong>.\n"
            f"<small>WHERE EXISTS (SELECT 1 FROM ...)</small>"
        ),
        "indice": (
            f"SELECT nom FROM pokemon p\n"
            f"WHERE EXISTS (\n"
            f"  SELECT 1 FROM pokemon_capacites pc\n"
            f"  JOIN capacites c ON pc.capacite_id = c.id\n"
            f"  WHERE pc.pokemon_id = p.id AND c.puissance >= {seuil}\n"
            f")"
        ),
        "solution": (
            f"SELECT nom FROM pokemon p "
            f"WHERE EXISTS (SELECT 1 FROM pokemon_capacites pc "
            f"JOIN capacites c ON pc.capacite_id = c.id "
            f"WHERE pc.pokemon_id = p.id AND c.puissance >= {seuil})"
        ),
        "compare": "names", "pokemon_id": None,
    }

def n4_08():
    seuil = _rc([90, 100, 110])
    return {
        "niveau": 4, "categorie": "NOT EXISTS",
        "titre": f"POKÉMON SANS CAPACITÉ >= {seuil}",
        "description": (
            f"Sélectionne le <code>nom</code> des Pokémon\n"
            f"pour lesquels il n'existe <strong>aucune</strong> capacité\n"
            f"de <code>puissance</code> >= <strong>{seuil}</strong>.\n"
            f"<small>WHERE NOT EXISTS (...)</small>"
        ),
        "indice": (
            f"SELECT nom FROM pokemon p\n"
            f"WHERE NOT EXISTS (\n"
            f"  SELECT 1 FROM pokemon_capacites pc\n"
            f"  JOIN capacites c ON pc.capacite_id = c.id\n"
            f"  WHERE pc.pokemon_id = p.id AND c.puissance >= {seuil}\n"
            f")"
        ),
        "solution": (
            f"SELECT nom FROM pokemon p "
            f"WHERE NOT EXISTS (SELECT 1 FROM pokemon_capacites pc "
            f"JOIN capacites c ON pc.capacite_id = c.id "
            f"WHERE pc.pokemon_id = p.id AND c.puissance >= {seuil})"
        ),
        "compare": "names", "pokemon_id": None,
    }

def n4_09():
    stat = _s(); label = _sl(stat)
    return {
        "niveau": 4, "categorie": "Sous-requête corrélée",
        "titre": f"AU-DESSUS DE LA MOYENNE DE SON TYPE ({label})",
        "description": (
            f"Sélectionne le <code>nom</code> des Pokémon\n"
            f"dont <code>{stat}</code> est supérieur à la\n"
            f"<strong>moyenne de {label.lower()} de leur propre type</strong>.\n"
            f"<small>Sous-requête corrélée : AVG({stat}) WHERE type1 = p.type1</small>"
        ),
        "indice": (
            f"SELECT nom FROM pokemon p\n"
            f"WHERE {stat} > (\n"
            f"  SELECT AVG({stat}) FROM pokemon WHERE type1 = p.type1\n"
            f")"
        ),
        "solution": (
            f"SELECT nom FROM pokemon p "
            f"WHERE {stat} > (SELECT AVG({stat}) FROM pokemon WHERE type1 = p.type1)"
        ),
        "compare": "names", "pokemon_id": None,
    }

def n4_10():
    return {
        "niveau": 4, "categorie": "Sous-requête double",
        "titre": "POKÉMON DU TYPE LE PLUS PEUPLÉ",
        "description": (
            "Sélectionne le <code>nom</code> de tous les Pokémon\n"
            "appartenant au <strong>type1 le plus représenté</strong>.\n"
            "<small>Sous-requête imbriquée pour trouver le type dominant.</small>"
        ),
        "indice": (
            "SELECT nom FROM pokemon\n"
            "WHERE type1 = (\n"
            "  SELECT type1 FROM pokemon\n"
            "  GROUP BY type1 ORDER BY COUNT(*) DESC LIMIT 1\n"
            ")"
        ),
        "solution": (
            "SELECT nom FROM pokemon "
            "WHERE type1 = (SELECT type1 FROM pokemon GROUP BY type1 ORDER BY COUNT(*) DESC LIMIT 1)"
        ),
        "compare": "names", "pokemon_id": None,
    }

# ── Registres ─────────────────────────────────────────────────────────────────

TEMPLATES = {
    1: [n1_01,n1_02,n1_03,n1_04,n1_05,n1_06,n1_07,n1_08,n1_09,n1_10,
        n1_11,n1_12,n1_13,n1_14,n1_15],
    2: [n2_01,n2_02,n2_03,n2_04,n2_05,n2_06,n2_07,n2_08,n2_09,n2_10,
        n2_11,n2_12,n2_13,n2_14,n2_15,n2_16,n2_17,n2_18,n2_19,n2_20],
    3: [n3_01,n3_02,n3_03,n3_04,n3_05,n3_06,n3_07,n3_08,n3_09,n3_10,
        n3_11,n3_12,n3_13,n3_14,n3_15],
    4: [n4_01,n4_02,n4_03,n4_04,n4_05,n4_06,n4_07,n4_08,n4_09,n4_10],
}

# Pondération niveaux pour le mode "aléatoire" : 30% N1, 35% N2, 25% N3, 10% N4
_POOL = (TEMPLATES[1] * 6 + TEMPLATES[2] * 7 + TEMPLATES[3] * 5 + TEMPLATES[4] * 2)


def generer_question(niveau: int = 0) -> dict:
    """Génère une question aléatoire. niveau=0 → pondéré, 1-4 → niveau fixe."""
    if niveau in (1, 2, 3, 4):
        fn = random.choice(TEMPLATES[niveau])
    else:
        fn = random.choice(_POOL)
    return fn()
