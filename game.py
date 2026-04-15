#!/usr/bin/env python3
"""SQLemon – Apprends le SQL à travers les 151 Pokémon de la Gen 1."""

import sqlite3
import sys
import os

# ── Encodage UTF-8 + activation ANSI sur Windows ─────────────────────────────

def _setup_terminal():
    """Configure l'encodage UTF-8 et active les séquences ANSI sur Windows."""
    # Forcer UTF-8 (surtout nécessaire sur Windows avec cp1252 par défaut)
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdin.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    # Activer le mode VT100/ANSI sur Windows (cmd, PowerShell)
    if sys.platform == "win32":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)        # STD_OUTPUT_HANDLE
            mode = ctypes.c_ulong()
            if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                # ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
                kernel32.SetConsoleMode(handle, mode.value | 0x0004)
        except Exception:
            pass

    # Retourne True si stdout est un vrai terminal interactif
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


_TTY = _setup_terminal()

DB_PATH = "sqlemon.db"

# ── Couleurs ANSI (no-op si non interactif ou redirection) ────────────────────

def _c(t, code): return f"\033[{code}m{t}\033[0m" if _TTY else str(t)
def green(t):   return _c(t, "32")
def red(t):     return _c(t, "31")
def yellow(t):  return _c(t, "33")
def cyan(t):    return _c(t, "36")
def bold(t):    return _c(t, "1")
def dim(t):     return _c(t, "2")

# ── Connexion ─────────────────────────────────────────────────────────────────

def connect():
    if not os.path.exists(DB_PATH):
        print(red(f"Erreur : base de données '{DB_PATH}' introuvable."))
        print("Lance d'abord : python setup_db.py")
        sys.exit(1)
    return sqlite3.connect(DB_PATH)

# ── Utilitaires SQL ───────────────────────────────────────────────────────────

def run_sql(conn, sql):
    """Retourne (lignes, colonnes, erreur_ou_None)."""
    try:
        cur = conn.execute(sql)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description] if cur.description else []
        return rows, cols, None
    except sqlite3.Error as e:
        return None, None, str(e)


def rows_to_set(rows):
    return frozenset(tuple(r) for r in rows)


def extract_col(rows, cols, col_name):
    """Retourne un frozenset des valeurs d'une colonne (cherche par nom, sinon col 0)."""
    idx = next((i for i, c in enumerate(cols) if c.lower() == col_name.lower()), 0)
    return frozenset(str(r[idx]).strip().lower() for r in rows)


def display_rows(rows, cols, max_rows=12):
    if not rows:
        print(dim("  (aucun résultat)"))
        return
    str_rows = [["NULL" if v is None else str(v) for v in row] for row in rows[:max_rows]]
    str_cols  = [str(c) for c in cols]
    widths    = [
        min(18, max(len(str_cols[i]), max((len(r[i]) for r in str_rows), default=0)))
        for i in range(len(str_cols))
    ]
    fmt = "  " + " │ ".join(f"{{:<{w}.{w}}}" for w in widths)
    sep = "  " + "─┼─".join("─" * w for w in widths)
    print(dim(fmt.format(*str_cols)))
    print(dim(sep))
    for row in str_rows:
        print(fmt.format(*row))
    if len(rows) > max_rows:
        print(dim(f"  … {len(rows)} lignes au total (affichage limité à {max_rows})"))


def read_input(prompt="SQL> "):
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("\nAu revoir !")
        sys.exit(0)

# ── Quêtes ────────────────────────────────────────────────────────────────────

def make_quests(conn):

    def expected(sql):
        rows, cols, _ = run_sql(conn, sql)
        return rows or [], cols or []

    # ── Fabriques de validateurs ──────────────────────────────────────────────

    def val_full(sol_sql):
        """Compare l'ensemble complet des lignes (toutes colonnes)."""
        def fn(rows, cols):
            exp, _ = expected(sol_sql)
            return rows_to_set(rows) == rows_to_set(exp)
        return fn

    def val_names(sol_sql, col="nom"):
        """Compare seulement l'ensemble des valeurs d'une colonne donnée."""
        def fn(rows, cols):
            exp, exp_cols = expected(sol_sql)
            return extract_col(rows, cols, col) == extract_col(exp, exp_cols, col)
        return fn

    # ── Liste des 10 quêtes ───────────────────────────────────────────────────

    return [
        # 1 ─────────────────────────────────────────────────────────────────
        {
            "titre": "1. Le Pokédex complet",
            "description": (
                "Affiche TOUS les Pokémon de la base de données.\n"
                "Sélectionne toutes les colonnes de la table pokemon."
            ),
            "indice":   "SELECT * retourne toutes les colonnes d'une table.",
            "solution": "SELECT * FROM pokemon;",
            "validate": val_full("SELECT * FROM pokemon"),
            "expected": lambda: expected("SELECT * FROM pokemon ORDER BY id"),
        },
        # 2 ─────────────────────────────────────────────────────────────────
        {
            "titre": "2. Noms et types",
            "description": (
                "Affiche uniquement le nom et le type principal (type1) de chaque Pokémon.\n"
                "Résultat attendu : 151 lignes avec 2 colonnes exactement."
            ),
            "indice":   "Liste les colonnes séparées par des virgules après SELECT.",
            "solution": "SELECT nom, type1 FROM pokemon;",
            "validate": val_full("SELECT nom, type1 FROM pokemon"),
            "expected": lambda: expected("SELECT nom, type1 FROM pokemon ORDER BY id"),
        },
        # 3 ─────────────────────────────────────────────────────────────────
        {
            "titre": "3. Les Pokémon de type Feu",
            "description": (
                "Trouve tous les Pokémon dont le type principal (type1) est 'Feu'.\n"
                "Affiche toutes leurs informations."
            ),
            "indice":   "Utilise WHERE type1 = 'Feu' pour filtrer les résultats.",
            "solution": "SELECT * FROM pokemon WHERE type1 = 'Feu';",
            "validate": val_names("SELECT * FROM pokemon WHERE type1 = 'Feu'"),
            "expected": lambda: expected(
                "SELECT nom, type1, pv, attaque FROM pokemon WHERE type1 = 'Feu' ORDER BY nom"
            ),
        },
        # 4 ─────────────────────────────────────────────────────────────────
        {
            "titre": "4. Les tanks",
            "description": (
                "Trouve tous les Pokémon qui ont strictement plus de 100 points de vie (pv).\n"
                "Affiche toutes leurs informations."
            ),
            "indice":   "La condition s'écrit : WHERE pv > 100",
            "solution": "SELECT * FROM pokemon WHERE pv > 100;",
            "validate": val_names("SELECT * FROM pokemon WHERE pv > 100"),
            "expected": lambda: expected(
                "SELECT nom, pv, defense FROM pokemon WHERE pv > 100 ORDER BY pv DESC"
            ),
        },
        # 5 ─────────────────────────────────────────────────────────────────
        {
            "titre": "5. Les 10 plus rapides",
            "description": (
                "Affiche les 10 Pokémon les plus rapides.\n"
                "Retourne le nom et la vitesse, triés du plus rapide au plus lent."
            ),
            "indice":   "Combine ORDER BY vitesse DESC et LIMIT 10.",
            "solution": "SELECT nom, vitesse FROM pokemon ORDER BY vitesse DESC LIMIT 10;",
            "validate": val_names(
                "SELECT nom, vitesse FROM pokemon ORDER BY vitesse DESC LIMIT 10"
            ),
            "expected": lambda: expected(
                "SELECT nom, vitesse FROM pokemon ORDER BY vitesse DESC LIMIT 10"
            ),
        },
        # 6 ─────────────────────────────────────────────────────────────────
        {
            "titre": "6. Répartition par type",
            "description": (
                "Compte le nombre de Pokémon par type principal (type1).\n"
                "Affiche le type et le total, triés du plus grand au plus petit."
            ),
            "indice":   "Utilise GROUP BY type1 avec COUNT(*) AS total, puis ORDER BY total DESC.",
            "solution": (
                "SELECT type1, COUNT(*) AS total\n"
                "FROM pokemon\n"
                "GROUP BY type1\n"
                "ORDER BY total DESC;"
            ),
            "validate": lambda rows, cols: (
                len(cols) >= 2
                and frozenset((r[0], r[1]) for r in rows)
                == frozenset(
                    (r[0], r[1])
                    for r in expected(
                        "SELECT type1, COUNT(*) FROM pokemon GROUP BY type1"
                    )[0]
                )
            ),
            "expected": lambda: expected(
                "SELECT type1, COUNT(*) AS total FROM pokemon GROUP BY type1 ORDER BY total DESC"
            ),
        },
        # 7 ─────────────────────────────────────────────────────────────────
        {
            "titre": "7. Les légendaires",
            "description": (
                "Trouve tous les Pokémon légendaires.\n"
                "Affiche toutes leurs informations.\n"
                "La colonne est_legendaire vaut 1 pour les légendaires, 0 sinon."
            ),
            "indice":   "Filtre avec WHERE est_legendaire = 1",
            "solution": "SELECT * FROM pokemon WHERE est_legendaire = 1;",
            "validate": val_names("SELECT * FROM pokemon WHERE est_legendaire = 1"),
            "expected": lambda: expected(
                "SELECT nom, type1, type2, pv FROM pokemon WHERE est_legendaire = 1"
            ),
        },
        # 8 ─────────────────────────────────────────────────────────────────
        {
            "titre": "8. Les Pokémon en S",
            "description": (
                "Trouve tous les Pokémon dont le nom commence par la lettre 'S'.\n"
                "Affiche leur nom et leur type1."
            ),
            "indice":   "LIKE 'S%' matche toutes les chaînes qui commencent par S.",
            "solution": "SELECT nom, type1 FROM pokemon WHERE nom LIKE 'S%';",
            "validate": val_names(
                "SELECT nom, type1 FROM pokemon WHERE nom LIKE 'S%'"
            ),
            "expected": lambda: expected(
                "SELECT nom, type1 FROM pokemon WHERE nom LIKE 'S%' ORDER BY nom"
            ),
        },
        # 9 ─────────────────────────────────────────────────────────────────
        {
            "titre": "9. Les maîtres du Séisme",
            "description": (
                "Trouve tous les Pokémon qui connaissent la capacité 'Séisme'.\n"
                "Affiche uniquement leur nom.\n"
                "Tables : pokemon · pokemon_capacites · capacites"
            ),
            "indice": (
                "Effectue deux JOIN :\n"
                "  FROM pokemon p\n"
                "  JOIN pokemon_capacites pc ON p.id = pc.pokemon_id\n"
                "  JOIN capacites c ON c.id = pc.capacite_id\n"
                "  WHERE c.nom = 'Séisme'"
            ),
            "solution": (
                "SELECT DISTINCT p.nom\n"
                "FROM pokemon p\n"
                "JOIN pokemon_capacites pc ON p.id = pc.pokemon_id\n"
                "JOIN capacites c ON c.id = pc.capacite_id\n"
                "WHERE c.nom = 'Séisme';"
            ),
            "validate": val_names(
                "SELECT DISTINCT p.nom FROM pokemon p "
                "JOIN pokemon_capacites pc ON p.id = pc.pokemon_id "
                "JOIN capacites c ON c.id = pc.capacite_id "
                "WHERE c.nom = 'Séisme'"
            ),
            "expected": lambda: expected(
                "SELECT DISTINCT p.nom FROM pokemon p "
                "JOIN pokemon_capacites pc ON p.id = pc.pokemon_id "
                "JOIN capacites c ON c.id = pc.capacite_id "
                "WHERE c.nom = 'Séisme' ORDER BY p.nom"
            ),
        },
        # 10 ────────────────────────────────────────────────────────────────
        {
            "titre": "10. Les attaquants d'élite",
            "description": (
                "Trouve tous les Pokémon dont l'attaque est supérieure\n"
                "à l'attaque moyenne de l'ensemble des Pokémon.\n"
                "Affiche leur nom et leur attaque."
            ),
            "indice": (
                "Utilise une sous-requête dans la condition WHERE :\n"
                "  WHERE attaque > (SELECT AVG(attaque) FROM pokemon)"
            ),
            "solution": (
                "SELECT nom, attaque FROM pokemon\n"
                "WHERE attaque > (SELECT AVG(attaque) FROM pokemon);"
            ),
            "validate": val_names(
                "SELECT nom, attaque FROM pokemon "
                "WHERE attaque > (SELECT AVG(attaque) FROM pokemon)"
            ),
            "expected": lambda: expected(
                "SELECT nom, attaque FROM pokemon "
                "WHERE attaque > (SELECT AVG(attaque) FROM pokemon) "
                "ORDER BY attaque DESC"
            ),
        },
    ]

# ── Affichage ─────────────────────────────────────────────────────────────────

BANNER = """\
╔══════════════════════════════════════════════════════╗
║    ⚡   S Q L e m o n  –  Apprends le SQL   ⚡     ║
║       151 Pokémon · 10 Quêtes · 0 dépendance         ║
╚══════════════════════════════════════════════════════╝"""

HELP = (
    f"  {yellow('indice')}    → affiche un conseil\n"
    f"  {yellow('solution')}  → révèle la réponse (quête non comptée)\n"
    f"  {yellow('passer')}    → passe à la quête suivante\n"
    f"  {yellow('quitter')}   → termine la partie"
)


def progress_bar(results, total):
    icons = {True: green("✓"), False: red("✗"), None: dim("·")}
    bar = " ".join(icons.get(r, dim("·")) for r in results)
    bar += " " + " ".join(dim("·") for _ in range(total - len(results)))
    return f"  [{bar}]"


# ── Logique d'une quête ───────────────────────────────────────────────────────

def play_quest(conn, quest, num, total, results):
    """
    Retourne :
      True  → quête réussie
      False → quête échouée / passée / solution vue
      None  → le joueur a tapé 'quitter'
    """
    LINE = "═" * 54
    print(f"\n{LINE}")
    print(bold(f"  {quest['titre']}  ({num}/{total})"))
    print(LINE)
    print(progress_bar(results, total))
    print(f"\n{quest['description']}\n")
    print(HELP)
    print()

    while True:
        user = read_input("SQL> ")
        if not user:
            continue

        cmd = user.lower()

        if cmd == "quitter":
            return None

        if cmd == "passer":
            print(yellow("  Quête passée.\n"))
            return False

        if cmd == "indice":
            print(f"\n{yellow('Indice :')} {quest['indice']}\n")
            continue

        if cmd == "solution":
            print(f"\n{cyan('Solution :')}")
            for line in quest["solution"].splitlines():
                print(f"  {line}")
            exp_rows, exp_cols = quest["expected"]()
            print(f"\n{cyan('Résultat attendu :')}")
            display_rows(exp_rows, exp_cols)
            print()
            return False

        # ── Exécution ──────────────────────────────────────────────────────
        rows, cols, err = run_sql(conn, user)
        if err:
            print(f"\n{red('Erreur SQL :')} {err}\n")
            continue

        # ── Validation ─────────────────────────────────────────────────────
        try:
            ok = quest["validate"](rows, cols)
        except Exception as e:
            print(f"\n{red('Erreur de validation :')} {e}\n")
            continue

        if ok:
            print(green(f"\n  ✓  Correct !  {len(rows)} ligne(s) retournée(s).\n"))
            return True

        # ── Réponse incorrecte ──────────────────────────────────────────────
        print(red("\n  ✗  Pas tout à fait…\n"))
        print("Ton résultat :")
        display_rows(rows, cols)
        exp_rows, exp_cols = quest["expected"]()
        print(f"\n{dim('Résultat attendu :')}")
        display_rows(exp_rows, exp_cols)
        print(
            f"\nTape {yellow('indice')} pour un conseil"
            f" ou continue d'essayer.\n"
        )


# ── Boucle principale ─────────────────────────────────────────────────────────

def main():
    print(bold(BANNER))
    print()

    conn    = connect()
    quests  = make_quests(conn)
    total   = len(quests)
    results = []   # True / False pour chaque quête jouée
    quit_early = False

    for i, quest in enumerate(quests, 1):
        result = play_quest(conn, quest, i, total, results)
        if result is None:
            quit_early = True
            break
        results.append(result)

    conn.close()

    # ── Score final ────────────────────────────────────────────────────────
    score    = sum(1 for r in results if r is True)
    played   = len(results)

    print(f"\n{'═' * 54}")
    print(bold("  Score final"))
    print(f"{'═' * 54}\n")
    print(progress_bar(results + ([None] * (total - played)), total))
    print(f"\n  {bold(str(score))}/{total} quêtes réussies", end="")
    if quit_early:
        print(f"  {dim(f'(partie interrompue après {played} quête(s))')}", end="")
    print("\n")

    if score == total:
        print(green("  Parfait ! Tu es un maître du SQL. 🏆"))
    elif score >= total * 0.7:
        print(yellow("  Très bien joué ! Encore un effort pour le score parfait."))
    elif score >= total * 0.4:
        print(cyan("  Bon début ! Relis les indices et réessaie les quêtes ratées."))
    else:
        print(dim("  Continue à pratiquer, tu vas y arriver !"))
    print()


if __name__ == "__main__":
    main()
