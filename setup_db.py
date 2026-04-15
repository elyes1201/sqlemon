import sqlite3
import csv
import os

DB_PATH = "sqlemon.db"
DATA_DIR = "data"

TYPES = [
    (1, "Normal"), (2, "Feu"), (3, "Eau"), (4, "Plante"), (5, "Electrik"),
    (6, "Glace"), (7, "Combat"), (8, "Poison"), (9, "Sol"), (10, "Vol"),
    (11, "Psy"), (12, "Insecte"), (13, "Roche"), (14, "Spectre"), (15, "Dragon"),
]


def create_tables(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS types (
            id INTEGER PRIMARY KEY,
            nom TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS pokemon (
            id INTEGER PRIMARY KEY,
            nom TEXT NOT NULL,
            type1 TEXT NOT NULL,
            type2 TEXT,
            pv INTEGER,
            attaque INTEGER,
            defense INTEGER,
            vitesse INTEGER,
            est_legendaire INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS capacites (
            id INTEGER PRIMARY KEY,
            nom TEXT NOT NULL,
            type_id INTEGER REFERENCES types(id),
            puissance INTEGER,
            precision INTEGER,
            categorie TEXT
        );
        CREATE TABLE IF NOT EXISTS pokemon_capacites (
            pokemon_id INTEGER REFERENCES pokemon(id),
            capacite_id INTEGER REFERENCES capacites(id),
            PRIMARY KEY (pokemon_id, capacite_id)
        );
        CREATE TABLE IF NOT EXISTS joueur (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            pseudo      TEXT    NOT NULL,
            starter_id  INTEGER REFERENCES pokemon(id),
            quete_actuelle INTEGER DEFAULT 1,
            date_debut  TEXT    DEFAULT (datetime('now'))
        );
    """)


def load_csv(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    conn.executemany("INSERT INTO types VALUES (?, ?)", TYPES)

    rows = load_csv("pokemon.csv")
    conn.executemany(
        "INSERT INTO pokemon VALUES (?,?,?,?,?,?,?,?,?)",
        [(r["id"], r["nom"], r["type1"], r["type2"] or None,
          r["pv"], r["attaque"], r["defense"], r["vitesse"], r["est_legendaire"])
         for r in rows],
    )

    rows = load_csv("capacites.csv")
    conn.executemany(
        "INSERT INTO capacites VALUES (?,?,?,?,?,?)",
        [(r["id"], r["nom"], r["type_id"], r["puissance"], r["precision"], r["categorie"])
         for r in rows],
    )

    rows = load_csv("pokemon_capacites.csv")
    conn.executemany(
        "INSERT INTO pokemon_capacites VALUES (?,?)",
        [(r["pokemon_id"], r["capacite_id"]) for r in rows],
    )

    conn.commit()

    cur = conn.cursor()
    nb_pokemon   = cur.execute("SELECT COUNT(*) FROM pokemon").fetchone()[0]
    nb_capacites = cur.execute("SELECT COUNT(*) FROM capacites").fetchone()[0]
    nb_relations = cur.execute("SELECT COUNT(*) FROM pokemon_capacites").fetchone()[0]

    print(f"Base de données créée : {DB_PATH}")
    print(f"  Pokémon insérés     : {nb_pokemon}")
    print(f"  Capacités insérées  : {nb_capacites}")
    print(f"  Relations pok-cap   : {nb_relations}")
    print(f"  Table joueur        : prête (0 joueurs)")

    conn.close()


if __name__ == "__main__":
    main()
