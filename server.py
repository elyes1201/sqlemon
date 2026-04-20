"""SQLemon – serveur web local (Flask)."""

from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os
import uuid
import webbrowser
import threading
from quetes import QUESTS
from arcade import generer_question

# Stockage en mémoire des questions arcade (clé = UUID)
_arcade_store: dict = {}

# Statistiques arcade par joueur (clé = joueur_id)
_arcade_stats: dict = {}

app = Flask(__name__, static_folder='static', static_url_path='/static')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "sqlemon.db")

# ── Helpers ───────────────────────────────────────────────────────────────────

def open_db():
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def open_db_rw():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def normalise(rows, cols, mode):
    if mode == "names":
        idx = next((i for i, c in enumerate(cols) if c.lower() == "nom"), 0)
        return frozenset(str(r[idx]).strip().lower() for r in rows)
    if mode == "aggregate":
        return frozenset((str(r[0]), int(r[1])) for r in rows) if len(cols) >= 2 else frozenset()
    if mode == "first_col":
        return frozenset(str(r[0]).strip().lower() for r in rows)
    # "full"
    return frozenset(tuple("" if v is None else str(v) for v in r) for r in rows)


def rows_to_dict(rows, cols, limit=50):
    return {
        "colonnes": list(cols),
        "lignes": [[v if v is not None else None for v in r] for r in rows[:limit]],
        "total": len(rows),
    }

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def root():
    return send_from_directory(BASE_DIR, "index.html")



@app.route("/quete/<int:numero>")
def get_quete(numero):
    if not 1 <= numero <= len(QUESTS):
        return jsonify({"erreur": "Quête introuvable"}), 404
    q = QUESTS[numero - 1]
    return jsonify({
        "numero":      q["numero"],
        "acte":        q["acte"],
        "zone":        q["zone"],
        "titre":       q["titre"],
        "contexte":    q["contexte"],
        "description": q["description"],
        "indice":      q["indice"],
        "pokemon_id":  q.get("pokemon_id"),
        "total":       len(QUESTS),
    })


@app.route("/pokemon_info/<int:pokemon_id>")
def get_pokemon_info(pokemon_id):
    conn = open_db()
    row = conn.execute(
        "SELECT id, nom, type1, type2 FROM pokemon WHERE id = ?", (pokemon_id,)
    ).fetchone()
    conn.close()
    if not row:
        return jsonify({"erreur": "Pokémon introuvable"}), 404
    return jsonify(dict(row))


@app.route("/starters")
def get_starters():
    STARTER_IDS = [1, 4, 7]
    conn = open_db()
    starters = []
    for sid in STARTER_IDS:
        row = conn.execute(
            "SELECT id, nom, type1, type2, pv, attaque, defense, vitesse FROM pokemon WHERE id = ?",
            (sid,)
        ).fetchone()
        if row:
            starters.append(dict(row))
    conn.close()
    return jsonify(starters)


@app.route("/nouvelle_partie", methods=["POST"])
def nouvelle_partie():
    data       = request.get_json(silent=True) or {}
    pseudo     = (data.get("pseudo") or "").strip()
    starter_id = data.get("starter_id")

    if not pseudo:
        return jsonify({"erreur": "Pseudo manquant"}), 400
    if starter_id not in (1, 4, 7):
        return jsonify({"erreur": "Starter invalide (1, 4 ou 7)"}), 400

    conn = open_db_rw()
    cur  = conn.execute(
        "INSERT INTO joueur (pseudo, starter_id) VALUES (?, ?)",
        (pseudo, starter_id),
    )
    joueur_id = cur.lastrowid
    conn.commit()
    conn.close()
    return jsonify({"succes": True, "joueur_id": joueur_id, "pseudo": pseudo, "starter_id": starter_id})


@app.route("/valider", methods=["POST"])
def valider():
    data    = request.get_json(silent=True) or {}
    numero  = data.get("numero")
    requete = (data.get("requete") or "").strip()

    if not isinstance(numero, int) or not 1 <= numero <= len(QUESTS):
        return jsonify({"erreur": "Numéro de quête invalide"}), 400
    if not requete:
        return jsonify({"erreur": "Requête vide"}), 400

    quest = QUESTS[numero - 1]

    try:
        conn = open_db()

        # Requête du joueur
        try:
            cur         = conn.execute(requete)
            player_rows = cur.fetchmany(500)
            player_cols = [d[0] for d in cur.description] if cur.description else []
        except sqlite3.Error as e:
            conn.close()
            return jsonify({"succes": False, "erreur_sql": str(e),
                            "message": f"Erreur SQL : {e}"})

        # Solution de référence (jamais exposée)
        cur2         = conn.execute(quest["solution"])
        sol_rows     = cur2.fetchall()
        sol_cols     = [d[0] for d in cur2.description] if cur2.description else []
        conn.close()

        succes = normalise(player_rows, player_cols, quest["compare"]) \
              == normalise(sol_rows,    sol_cols,    quest["compare"])

        message = (
            f"Correct ! {len(player_rows)} ligne(s) retournée(s)."
            if succes else
            f"Pas tout à fait… {len(player_rows)} ligne(s) obtenue(s), "
            f"{len(sol_rows)} attendue(s)."
        )

        return jsonify({
            "succes":   succes,
            "message":  message,
            "resultat": rows_to_dict(player_rows, player_cols, limit=50 if succes else 10),
            "attendu":  None if succes else rows_to_dict(sol_rows, sol_cols, limit=5),
        })

    except Exception as e:
        return jsonify({"succes": False, "message": f"Erreur serveur : {e}"}), 500


@app.route("/arcade/question")
def arcade_question():
    niveau = request.args.get("niveau", 0, type=int)
    q    = generer_question(niveau)
    qid  = str(uuid.uuid4())
    _arcade_store[qid] = {
        "solution": q["solution"],
        "compare":  q["compare"],
    }
    return jsonify({
        "id":          qid,
        "niveau":      q["niveau"],
        "categorie":   q["categorie"],
        "titre":       q["titre"],
        "description": q["description"],
        "indice":      q["indice"],
        "solution":    q["solution"],   # exposé à des fins éducatives
        "pokemon_id":  q.get("pokemon_id"),
    })


@app.route("/arcade/valider", methods=["POST"])
def arcade_valider():
    data      = request.get_json(silent=True) or {}
    qid       = data.get("question_id", "")
    requete   = (data.get("requete") or "").strip()
    joueur_id = data.get("joueur_id")

    if not qid or qid not in _arcade_store:
        return jsonify({"erreur": "Question introuvable ou expirée"}), 400
    if not requete:
        return jsonify({"erreur": "Requête vide"}), 400

    stored = _arcade_store[qid]

    try:
        conn = open_db()

        try:
            cur         = conn.execute(requete)
            player_rows = cur.fetchmany(500)
            player_cols = [d[0] for d in cur.description] if cur.description else []
        except sqlite3.Error as e:
            conn.close()
            return jsonify({"succes": False, "erreur_sql": str(e),
                            "message": f"Erreur SQL : {e}"})

        cur2     = conn.execute(stored["solution"])
        sol_rows = cur2.fetchall()
        sol_cols = [d[0] for d in cur2.description] if cur2.description else []
        conn.close()

        succes = normalise(player_rows, player_cols, stored["compare"]) \
              == normalise(sol_rows,    sol_cols,    stored["compare"])

        message = (
            f"Correct ! {len(player_rows)} ligne(s) retournée(s)."
            if succes else
            f"Pas tout à fait… {len(player_rows)} ligne(s) obtenue(s), "
            f"{len(sol_rows)} attendue(s)."
        )

        # Mettre à jour les stats serveur du joueur
        if joueur_id is not None:
            st = _arcade_stats.setdefault(joueur_id, {
                "tentees": 0, "reussies": 0,
                "streak": 0, "best_streak": 0,
            })
            st["tentees"] += 1
            if succes:
                st["reussies"] += 1
                st["streak"]   += 1
                st["best_streak"] = max(st["best_streak"], st["streak"])
            else:
                st["streak"] = 0

        if succes:
            _arcade_store.pop(qid, None)

        return jsonify({
            "succes":   succes,
            "message":  message,
            "resultat": rows_to_dict(player_rows, player_cols, limit=50 if succes else 10),
            "attendu":  None if succes else rows_to_dict(sol_rows, sol_cols, limit=5),
        })

    except Exception as e:
        return jsonify({"succes": False, "message": f"Erreur serveur : {e}"}), 500


@app.route("/arcade/stats")
def arcade_stats():
    joueur_id = request.args.get("joueur_id", type=int)
    if joueur_id is None:
        return jsonify({"erreur": "joueur_id requis"}), 400
    st = _arcade_stats.get(joueur_id, {
        "tentees": 0, "reussies": 0, "streak": 0, "best_streak": 0,
    })
    return jsonify(st)


@app.route("/sauvegarder", methods=["POST"])
def sauvegarder():
    import json as _json
    data      = request.get_json(silent=True) or {}
    joueur_id = data.get("joueur_id")
    quete     = data.get("quete")
    scores    = data.get("scores")
    if not joueur_id or not quete or scores is None:
        return jsonify({"erreur": "Données manquantes"}), 400
    progression = _json.dumps({"quete": quete, "scores": scores})
    conn = open_db_rw()
    conn.execute(
        "UPDATE joueur SET quete_actuelle = ?, progression = ? WHERE id = ?",
        (quete, progression, joueur_id),
    )
    conn.commit()
    conn.close()
    return jsonify({"succes": True})


@app.route("/charger/<int:joueur_id>")
def charger(joueur_id):
    import json as _json
    conn = open_db()
    row  = conn.execute(
        "SELECT id, pseudo, starter_id, quete_actuelle, progression FROM joueur WHERE id = ?",
        (joueur_id,),
    ).fetchone()
    conn.close()
    if not row:
        return jsonify({"erreur": "Joueur introuvable"}), 404
    d = dict(row)
    if d["progression"]:
        d["progression"] = _json.loads(d["progression"])
    return jsonify(d)


@app.route("/sauvegarde/<pseudo>")
def sauvegarde_pseudo(pseudo):
    import json as _json
    conn = open_db()
    row  = conn.execute(
        """SELECT id, pseudo, starter_id, quete_actuelle, progression
           FROM joueur WHERE pseudo = ? AND progression IS NOT NULL
           ORDER BY id DESC LIMIT 1""",
        (pseudo,),
    ).fetchone()
    conn.close()
    if not row:
        return jsonify({"trouve": False})
    d = dict(row)
    if d["progression"]:
        d["progression"] = _json.loads(d["progression"])
    d["trouve"] = True
    return jsonify(d)


@app.route("/executer", methods=["POST"])
def executer():
    data    = request.get_json(silent=True) or {}
    requete = (data.get("requete") or "").strip()
    if not requete:
        return jsonify({"erreur": "Requête vide"}), 400
    try:
        conn = open_db()
        try:
            cur  = conn.execute(requete)
            rows = cur.fetchmany(200)
            cols = [d[0] for d in cur.description] if cur.description else []
        except sqlite3.Error as e:
            conn.close()
            return jsonify({"succes": False, "erreur_sql": str(e), "message": str(e)})
        conn.close()
        return jsonify({"succes": True, "resultat": rows_to_dict(rows, cols, limit=200)})
    except Exception as e:
        return jsonify({"succes": False, "message": f"Erreur serveur : {e}"}), 500


if __name__ == "__main__":
    print("SQLemon – http://localhost:5000")
    if os.environ.get("RENDER") is None:
        threading.Timer(1.0, lambda: webbrowser.open("http://localhost:5000")).start()
    app.run(host="0.0.0.0", port=5000)
