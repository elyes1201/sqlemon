// ── Constantes ────────────────────────────────────────────────────────────────
const TOTAL = 35;
const SPRITE_BASE = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/';

// Définition des 9 actes (premier/dernier quest, label court, message de transition)
const ACTES = [
  { num:1, label:"BOURG",    first:1,  last:3,  zone:"Bourg Palette",  color:"#306230",
    msg:"Bourg Palette est derrière toi. La Forêt de Jade s'étend devant toi, grouillante de Pokémon Insecte..." },
  { num:2, label:"JADE",     first:4,  last:7,  zone:"Forêt → Argenta",color:"#0f380f",
    msg:"L'Arène d'Argenta est vaincue ! La Team Rocket rôde. Cap sur le sinistre Mont Sélénite..." },
  { num:3, label:"SÉLÉNI.",  first:8,  last:11, zone:"Mont Sélénite",   color:"#6b6b6b",
    msg:"Tu émerges de la grotte obscure. Les lumières de Céladopole brillent au loin..." },
  { num:4, label:"CÉLADO.",  first:12, last:15, zone:"Céladopole",      color:"#4a90d9",
    msg:"Le labo Silph a livré ses secrets. Une brise froide vient du nord... direction Lavanville." },
  { num:5, label:"LAVANDE",  first:16, last:19, zone:"Lavanville",      color:"#4a0a4a",
    msg:"Les esprits de Lavanville sont en paix. La Route Nationale s'étire vers Parmanie et Carmin..." },
  { num:6, label:"PARMA.",   first:20, last:23, zone:"Parmanie → Carmin",color:"#8b2020",
    msg:"La Team Rocket est repoussée ! Giovanni bat en retraite. Un bateau t'attend vers Cramois'île..." },
  { num:7, label:"CRAMO.",   first:24, last:27, zone:"Cramois'île",     color:"#d96a00",
    msg:"L'île est sauvée. Tu prends la route des sommets vers Azuria et Grisaille City..." },
  { num:8, label:"AZURIA",   first:28, last:31, zone:"Azuria → Grisaille",color:"#00a8d9",
    msg:"Tu es prêt. Le Plateau Indigo se profile à l'horizon. La Ligue Pokémon t'attend..." },
  { num:9, label:"INDIGO",   first:32, last:35, zone:"Plateau Indigo",  color:"#d9a800",
    msg:null },
];

// ── Backgrounds par acte ───────────────────────────────────────────────────────
const BACKGROUNDS = [
  null,
  '/static/backgrounds/bourg_palette.png',
  '/static/backgrounds/foret_jade.png',
  '/static/backgrounds/mont_selenite.png',
  '/static/backgrounds/celadopole.png',
  '/static/backgrounds/lavanville.png',
  '/static/backgrounds/carmin_sur_mer.png',
  "/static/backgrounds/cramois'ile.png",
  '/static/backgrounds/azuria.png',
  '/static/backgrounds/plateau_indigo.png',
];
let _currentBgLayer = 'a';

function changeBg(acteNum) {
  if (!acteNum) return;
  document.body.className = 'acte-' + acteNum;
}

// ── AudioManager — musique de fond ────────────────────────────────────────────
const AudioManager = {
  BASE: 'https://play.pokemonshowdown.com/audio/bgm/',
  TRACKS: {
    0: 'title.mp3',         // écran titre
    1: 'pallet.mp3',
    2: 'viridianforest.mp3',
    3: 'mtmoon.mp3',
    4: 'cerulean.mp3',
    5: 'lavender.mp3',
    6: 'vermilion.mp3',
    7: 'cinnabar.mp3',
    8: 'cerulean.mp3',
    9: 'indigo.mp3',
  },
  VOLUME:  0.3,
  FADE_MS: 1000,

  _current:    null,
  _currentKey: null,

  init() {
    if (localStorage.getItem('sqlemon_sound') === 'off') {
      soundEnabled = false;
    }
    _updateSoundBtn();
  },

  play(key) {
    if (this._currentKey === key) return;
    this._currentKey = key;

    const next = new Audio(this.BASE + (this.TRACKS[key] || ''));
    next.loop   = true;
    next.volume = 0;
    next.play().catch(() => {});  // silencieux si autoplay bloqué

    const prev = this._current;
    this._current = next;

    if (soundEnabled) {
      this._fade(next, 0, this.VOLUME, this.FADE_MS);
      if (prev) this._fade(prev, prev.volume, 0, this.FADE_MS,
        () => { prev.pause(); prev.src = ''; });
    } else {
      if (prev) { prev.pause(); prev.src = ''; }
    }
  },

  syncVolume() {
    localStorage.setItem('sqlemon_sound', soundEnabled ? 'on' : 'off');
    if (!this._current) return;
    if (soundEnabled) {
      this._fade(this._current, this._current.volume, this.VOLUME, 500);
    } else {
      this._fade(this._current, this._current.volume, 0, 500);
    }
  },

  _fade(audio, from, to, ms, onDone) {
    if (audio._fadeTimer) clearInterval(audio._fadeTimer);
    const STEPS = 20;
    const step_ms = ms / STEPS;
    const delta   = (to - from) / STEPS;
    let   step    = 0;
    audio.volume  = Math.max(0, Math.min(1, from));
    audio._fadeTimer = setInterval(() => {
      step++;
      audio.volume = Math.max(0, Math.min(1, from + delta * step));
      if (step >= STEPS) {
        clearInterval(audio._fadeTimer);
        audio._fadeTimer = null;
        audio.volume = Math.max(0, Math.min(1, to));
        if (onDone) onDone();
      }
    }, step_ms);
  },
};

function _updateSoundBtn() {
  const btn = document.getElementById('sound-btn');
  if (btn) btn.textContent = soundEnabled ? '🔊' : '🔇';
}

// ── État ─────────────────────────────────────────────────────────────────────
let quete    = 1;
let scores   = new Array(TOTAL).fill(null); // null / true / false
let joueurPseudo      = '';
let joueurStarterId   = null;
let joueurStarterNom  = '';
let selectedStarterId = null;
let startTime         = null;
let transitionNextQ   = null; // quête à charger après transition
let currentPokemonId  = null; // sprite en cours

// Mode de jeu
let gameMode = 'histoire'; // 'histoire' | 'arcade'

// État arcade
let defiCount       = 0;   // questions chargées (tentées)
let defiOk          = 0;   // questions réussies
let defiStreak      = 0;   // streak actuel
let defiChallengeId = null; // question_id en cours
let arcadeNiveau    = 0;   // 0=aléatoire, 1-4=niveau fixe

// ID joueur (pour /arcade/stats)
let joueurId = null;

// ── Démarrage ─────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  AudioManager.init();
  lancerIntro();
});

document.addEventListener('DOMContentLoaded', () => {
  const reqEl = document.getElementById('requete');
  if (reqEl) reqEl.addEventListener('keydown', e => {
    if (e.ctrlKey && e.key === 'Enter') { e.preventDefault(); valider(); }
  });
  const docReqEl = document.getElementById('doc-requete');
  if (docReqEl) docReqEl.addEventListener('keydown', e => {
    if (e.ctrlKey && e.key === 'Enter') { e.preventDefault(); executerDocSQL(); }
  });
});

// ── INTRO ─────────────────────────────────────────────────────────────────────
const TEXTE_INTRO = "Le Professeur Chen a besoin de ton aide. Des Pokémon ont disparu dans toute la région de Kanto. Seul un dresseur maîtrisant l'art des requêtes SQL pourra les retrouver dans la base de données de Kanto. Quel est ton nom, dresseur ?";

function lancerIntro() {
  changeBg(1);
  AudioManager.play(0); // title.mp3
  typewriterEffect(document.getElementById('prof-text'), TEXTE_INTRO, 28, () => {
    document.getElementById('pseudo-wrap').style.display = 'flex';
    document.getElementById('btn-commencer').style.display = 'block';
    document.getElementById('pseudo-input').focus();
  });
}

function typewriterEffect(el, text, speed, onDone) {
  let i = 0;
  el.innerHTML = '<span class="cursor-blink"></span>';
  const cursor = el.querySelector('.cursor-blink');
  const interval = setInterval(() => {
    if (i < text.length) {
      cursor.insertAdjacentText('beforebegin', text[i]);
      i++;
    } else {
      clearInterval(interval);
      cursor.remove();
      if (onDone) onDone();
    }
  }, speed);
}

document.addEventListener('DOMContentLoaded', () => {
  const pseudoInput = document.getElementById('pseudo-input');
  if (pseudoInput) pseudoInput.addEventListener('keydown', e => {
    if (e.key === 'Enter') allerEtapeMode();
  });
});

function allerEtapeMode() {
  const pseudo = document.getElementById('pseudo-input').value.trim();
  if (!pseudo) {
    document.getElementById('pseudo-input').focus();
    return;
  }
  joueurPseudo = pseudo;
  document.getElementById('step-a').style.display = 'none';
  document.getElementById('step-mode').style.display = 'flex';
}

async function allerEtapeB(mode) {
  gameMode = mode;
  document.getElementById('step-mode').style.display = 'none';
  document.getElementById('step-b').style.display = 'flex';

  const grid = document.getElementById('starters-grid');
  grid.innerHTML = '<div style="font-size:7px;color:var(--gb-dark);grid-column:1/-1">CHARGEMENT…</div>';

  try {
    const r = await fetch('/starters');
    const starters = await r.json();
    afficherStarters(starters);
  } catch {
    grid.innerHTML = '<div style="font-size:7px;color:var(--gb-dark);grid-column:1/-1">ERREUR CHARGEMENT</div>';
  }
}

function afficherStarters(starters) {
  const MAX_STAT = 130;
  const STATS = [
    { key: 'pv',       label: 'PV' },
    { key: 'attaque',  label: 'ATT' },
    { key: 'defense',  label: 'DEF' },
    { key: 'vitesse',  label: 'VIT' },
  ];

  const grid = document.getElementById('starters-grid');
  grid.innerHTML = '';

  starters.forEach(s => {
    const card = document.createElement('div');
    card.className = 'starter-card';
    card.dataset.type = s.type1;
    card.dataset.id = s.id;

    const statRows = STATS.map(st => {
      const pct = Math.round((s[st.key] / MAX_STAT) * 100);
      return `<div class="s-stat-row">
        <div class="s-stat-name">${st.label}</div>
        <div class="s-stat-bar-bg"><div class="s-stat-bar" style="width:${pct}%"></div></div>
        <div class="s-stat-val">${s[st.key]}</div>
      </div>`;
    }).join('');

    card.innerHTML = `
      <div class="starter-sprite-wrap">
        <img class="starter-sprite" src="${SPRITE_BASE}${s.id}.png" alt="${s.nom}" onerror="this.parentElement.style.display='none'">
      </div>
      <div class="s-nom">${s.nom.toUpperCase()}</div>
      <div class="s-type">${s.type1}${s.type2 ? ' / ' + s.type2 : ''}</div>
      <div class="s-stats">${statRows}</div>
    `;

    card.addEventListener('click', () => {
      document.querySelectorAll('.starter-card').forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
      selectedStarterId = s.id;
      document.getElementById('btn-confirmer').disabled = false;
    });

    grid.appendChild(card);
  });
}

async function commencerAventure() {
  if (!selectedStarterId) return;

  const btn = document.getElementById('btn-confirmer');
  btn.disabled = true;
  btn.textContent = '…';

  try {
    const resp = await fetch('/nouvelle_partie', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pseudo: joueurPseudo, starter_id: selectedStarterId }),
    });
    const data = await resp.json();
    if (data.succes) {
      joueurStarterId = selectedStarterId;
      joueurId = data.joueur_id || null;
      if (gameMode === 'arcade') {
        demarrerArcade();
      } else {
        demarrerJeu();
      }
    } else {
      btn.disabled = false;
      btn.textContent = '▶ COMMENCER L\'AVENTURE';
      alert('Erreur: ' + (data.erreur || 'inconnue'));
    }
  } catch {
    btn.disabled = false;
    btn.textContent = '▶ COMMENCER L\'AVENTURE';
  }
}

function demarrerJeu() {
  const overlay = document.getElementById('ecran-intro');
  overlay.classList.add('fade-out');
  startTime = Date.now();
  setTimeout(async () => {
    overlay.style.display = 'none';
    const gc = document.getElementById('game-content');
    gc.style.display = 'flex';

    // Récupérer le nom du starter choisi
    try {
      const r = await fetch('/starters');
      const starters = await r.json();
      const s = starters.find(x => x.id === joueurStarterId);
      if (s) joueurStarterNom = s.nom;
    } catch { joueurStarterNom = '?'; }

    // Badge dresseur
    document.getElementById('db-pseudo').textContent  = joueurPseudo.toUpperCase();
    document.getElementById('db-starter').textContent = joueurStarterNom.toUpperCase();
    document.getElementById('dresseur-badge').style.display = 'block';

    // Écran de fin - préremplir
    document.getElementById('fin-pseudo').textContent  = joueurPseudo.toUpperCase();
    document.getElementById('fin-starter').textContent = joueurStarterNom.toUpperCase();

    buildActBar();
    buildPips();
    chargerQuete(1);
  }, 700);
}

async function demarrerArcade() {
  const overlay = document.getElementById('ecran-intro');
  overlay.classList.add('fade-out');
  startTime = Date.now();
  defiCount = 0; defiOk = 0; defiStreak = 0;

  setTimeout(async () => {
    overlay.style.display = 'none';
    const gc = document.getElementById('game-content');
    gc.style.display = 'flex';

    try {
      const r = await fetch('/starters');
      const starters = await r.json();
      const s = starters.find(x => x.id === joueurStarterId);
      if (s) joueurStarterNom = s.nom;
    } catch { joueurStarterNom = '?'; }

    document.getElementById('db-pseudo').textContent  = joueurPseudo.toUpperCase();
    document.getElementById('db-starter').textContent = joueurStarterNom.toUpperCase();
    document.getElementById('dresseur-badge').style.display = 'block';

    // Interface arcade
    document.getElementById('act-bar').style.display      = 'none';
    document.getElementById('arcade-bar').classList.add('visible');
    document.getElementById('prog-pips').style.display    = 'none';
    document.getElementById('score-histoire').style.display = 'none';
    document.getElementById('score-arcade').style.display   = '';
    document.getElementById('lcd-header-histoire').style.display = 'none';
    document.getElementById('lcd-header-arcade').style.display   = '';
    document.getElementById('btn-passer').classList.add('visible');

    chargerDefiArcade();
  }, 700);
}

// ── Mode Arcade ───────────────────────────────────────────────────────────────

async function chargerDefiArcade() {
  defiCount++;
  defiChallengeId = null;

  setFeedback('', '');
  document.getElementById('results-zone').innerHTML = '';
  document.getElementById('q-indice').classList.remove('visible');
  cacherBoutonSuivant();
  document.getElementById('requete').value = '';

  document.getElementById('q-num-arc').textContent = String(defiCount).padStart(2, '0');
  document.getElementById('ss-defi').textContent   = String(defiCount).padStart(2, '0');
  document.getElementById('q-titre').textContent   = 'CHARGEMENT…';
  document.getElementById('q-desc').innerHTML      = '';

  try {
    const r = await fetch(`/arcade/question?niveau=${arcadeNiveau}`);
    const d = await r.json();
    defiChallengeId = d.id;

    document.getElementById('q-titre').textContent  = d.titre.toUpperCase();
    document.getElementById('q-desc').innerHTML     = d.description.replace(/\n/g, '<br>');
    document.getElementById('q-indice').textContent = d.indice;

    const niveauLabel = d.niveau ? `NIV.${d.niveau}` : 'ARCADE';
    document.getElementById('q-zone').textContent =
      `▶ ARCADE · ${niveauLabel} · ${(d.categorie || '').toUpperCase()}`;

    // Pas de contexte narratif en arcade
    document.getElementById('q-contexte').classList.remove('visible');

    chargerSprite(d.pokemon_id || null);

  } catch {
    document.getElementById('q-titre').textContent = 'ERREUR CONNEXION';
  }
}

async function validerArcade() {
  const req = document.getElementById('requete').value.trim();
  if (!req) { setFeedback('> SAISIR UNE REQUETE SQL', 'bad'); return; }
  if (!defiChallengeId) { setFeedback('> AUCUN DÉFI CHARGÉ', 'bad'); return; }

  setFeedback('> ANALYSE EN COURS…', 'ok loader');
  document.getElementById('results-zone').innerHTML = '';
  document.getElementById('btn-val').disabled = true;

  try {
    const resp = await fetch('/arcade/valider', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question_id: defiChallengeId, requete: req, joueur_id: joueurId }),
    });
    const data = await resp.json();
    document.getElementById('btn-val').disabled = false;
    afficherReponseArcade(data);
  } catch {
    document.getElementById('btn-val').disabled = false;
    setFeedback('> ERREUR: SERVEUR INJOIGNABLE', 'bad');
  }
}

function afficherReponseArcade(data) {
  if (data.erreur_sql) { afficherErreurSQL(data.message); return; }
  if (data.erreur)     { setFeedback('> ERR: ' + data.erreur, 'bad'); return; }

  if (data.succes) {
    soundSucces();
    defiOk++;
    defiStreak++;
    majArcadeUI();
    if (data.resultat) buildTable(data.resultat, 'RÉSULTAT', 'r-ok');
    setFeedback('> ' + data.message, 'ok');
    revelerSprite();
    const btn = document.getElementById('btn-next-quest');
    btn.textContent = 'DÉFI SUIVANT ▶';
    btn.classList.add('visible');
  } else {
    soundErreur();
    defiStreak = 0;
    majArcadeUI();
    setFeedback('> ' + data.message, 'bad');
    if (data.resultat) buildTable(data.resultat, 'CE QUE TA REQUÊTE RETOURNE', 'r-bad');
    if (data.attendu)  buildTable(data.attendu,  'CE QUI ÉTAIT ATTENDU',       '');
  }
}

function afficherErreurSQL(message) {
  setFeedback('', '');
  const zone = document.getElementById('results-zone');
  zone.innerHTML = '';
  const div = document.createElement('div');
  div.className = 'sql-error-msg';
  div.innerHTML = '<div class="sql-error-label">ERREUR SQL</div>'
    + '<div class="sql-error-detail">' + message + '</div>';
  zone.appendChild(div);
}

function majArcadeUI() {
  document.getElementById('sc-arc-ok').textContent  = defiOk;
  document.getElementById('sc-streak').textContent  = defiStreak;
  document.getElementById('arc-ok-bar').textContent     = defiOk;
  document.getElementById('arc-tried-bar').textContent  = defiCount;
  document.getElementById('arc-streak-bar').textContent = defiStreak;
  const pct = defiCount > 0 ? Math.round((defiOk / defiCount) * 100) + '%' : '–';
  document.getElementById('arc-pct-bar').textContent = pct;
}

function setNiveau(n) {
  arcadeNiveau = n;
  document.querySelectorAll('.diff-btn').forEach(b => {
    b.classList.toggle('active', parseInt(b.dataset.niveau) === n);
  });
}

function passerQuestion() {
  chargerDefiArcade();
}

// ── Barre d'actes ────────────────────────────────────────────────────────────
function buildActBar() {
  const bar = document.getElementById('act-bar');
  bar.innerHTML = '';
  ACTES.forEach(a => {
    const seg = document.createElement('div');
    seg.className = 'act-seg as-locked';
    seg.id = `act-seg-${a.num}`;
    seg.title = a.zone;
    seg.style.setProperty('--act-color', a.color);
    seg.innerHTML = `
      <div class="act-seg-badge">${a.num}</div>
      <div class="act-seg-label">${a.label}</div>`;
    seg.addEventListener('click', () => chargerQuete(a.first));
    bar.appendChild(seg);
  });
  majActBar();
}

function majActBar() {
  const acteActuel = getActe(quete).num;
  document.body.dataset.acte = acteActuel;
  changeBg(acteActuel);
  AudioManager.play(acteActuel); // fondu enchaîné vers la musique de l'acte
  ACTES.forEach(a => {
    const seg = document.getElementById(`act-seg-${a.num}`);
    if (!seg) return;
    const acteDone = scores.slice(a.first - 1, a.last).every(s => s === true);
    const badgeEl = seg.querySelector('.act-seg-badge');
    seg.className = 'act-seg';
    if (acteDone) {
      seg.classList.add('as-done');
      if (badgeEl) badgeEl.textContent = '✓';
    } else if (a.num === acteActuel) {
      seg.classList.add('as-current');
      if (badgeEl) badgeEl.textContent = a.num;
    } else if (a.num < acteActuel) {
      seg.classList.add('as-done');
      if (badgeEl) badgeEl.textContent = '✓';
    } else {
      seg.classList.add('as-locked');
      if (badgeEl) badgeEl.textContent = a.num;
    }
  });
}

function getActe(numQuete) {
  return ACTES.find(a => numQuete >= a.first && numQuete <= a.last) || ACTES[0];
}

// ── Pips de progression ───────────────────────────────────────────────────────
function buildPips() {
  const wrap = document.getElementById('prog-pips');
  for (let i = 1; i <= TOTAL; i++) {
    const d = document.createElement('div');
    d.className = 'pip';
    d.id = `pip-${i}`;
    d.title = `Quête ${i}`;
    d.style.cssText = 'width:7px;height:7px;';
    d.addEventListener('click', () => chargerQuete(i));
    wrap.appendChild(d);
  }
}

function majPips() {
  let ok = 0, fail = 0;
  for (let i = 1; i <= TOTAL; i++) {
    const cl = ['pip'];
    if (i === quete)           cl.push('p-active');
    if (scores[i-1] === true)  { cl.push('p-ok');   ok++; }
    if (scores[i-1] === false) { cl.push('p-fail');  fail++; }
    document.getElementById(`pip-${i}`).className = cl.join(' ');
  }
  document.getElementById('ss-num').textContent  = String(quete).padStart(2,'0');
  document.getElementById('sc-ok').textContent   = ok;
  document.getElementById('sc-fail').textContent = fail;
  document.getElementById('btn-prev').disabled = (quete === 1);
  document.getElementById('btn-next').disabled = (quete === TOTAL);
  majActBar();
}

// ── Chargement d'une quête ────────────────────────────────────────────────────
async function chargerQuete(n) {
  quete = n;
  majPips();

  setFeedback('', '');
  document.getElementById('results-zone').innerHTML = '';
  document.getElementById('q-indice').classList.remove('visible');
  cacherBoutonSuivant();

  document.getElementById('q-num').textContent   = String(n).padStart(2,'0');
  document.getElementById('q-titre').textContent = '…';
  document.getElementById('q-desc').innerHTML    = '';

  try {
    const r = await fetch(`/quete/${n}`);
    const d = await r.json();

    document.getElementById('q-num').textContent     = String(d.numero).padStart(2,'0');
    document.getElementById('q-acte').textContent    = d.acte;
    document.getElementById('q-zone').textContent    = '▶ ' + (d.zone || '');
    document.getElementById('q-titre').textContent   = d.titre.toUpperCase();
    document.getElementById('q-desc').innerHTML      = d.description.replace(/\n/g,'<br>');
    document.getElementById('q-indice').textContent  = d.indice;

    const contexteEl = document.getElementById('q-contexte');
    if (d.contexte) {
      contexteEl.textContent = '> ' + d.contexte;
      contexteEl.classList.add('visible');
    } else {
      contexteEl.classList.remove('visible');
    }

    let pid = d.pokemon_id;
    if (pid === 'starter') pid = joueurStarterId;
    chargerSprite(pid);

  } catch {
    document.getElementById('q-titre').textContent = 'ERREUR CONNEXION';
  }
}

function naviguer(delta) { chargerQuete(quete + delta); }

// ── Sprite ────────────────────────────────────────────────────────────────────
function chargerSprite(pokemonId) {
  currentPokemonId = pokemonId;
  const frame  = document.getElementById('sprite-frame');
  const img    = document.getElementById('sprite-img');
  const qmark  = document.getElementById('sprite-qmark');
  const nomEl  = document.getElementById('sprite-nom');
  const typeEl = document.getElementById('sprite-type');

  if (!pokemonId) {
    frame.classList.remove('visible');
    img.src = '';
    return;
  }

  frame.classList.add('visible');
  img.className = 'sprite-img silhouette';
  img.src = SPRITE_BASE + pokemonId + '.png';
  img.onerror = () => { frame.classList.remove('visible'); };
  qmark.className = 'sprite-q-mark';
  nomEl.textContent  = '??????';
  nomEl.className    = 'sprite-nom';
  typeEl.textContent = '';
  typeEl.className   = 'sprite-type';
}

async function revelerSprite() {
  if (!currentPokemonId) return;
  const frame  = document.getElementById('sprite-frame');
  const img    = document.getElementById('sprite-img');
  const qmark  = document.getElementById('sprite-qmark');
  const nomEl  = document.getElementById('sprite-nom');
  const typeEl = document.getElementById('sprite-type');
  const screen = document.getElementById('sprite-screen');

  img.className = 'sprite-img revealed';
  qmark.className = 'sprite-q-mark hidden';
  screen.classList.add('flash');
  setTimeout(() => screen.classList.remove('flash'), 900);

  try {
    const r = await fetch(`/pokemon_info/${currentPokemonId}`);
    if (r.ok) {
      const p = await r.json();
      nomEl.textContent = p.nom.toUpperCase();
      typeEl.textContent = p.type1 + (p.type2 ? ' / ' + p.type2 : '');
    } else {
      nomEl.textContent = '#' + currentPokemonId;
    }
  } catch {
    nomEl.textContent = '#' + currentPokemonId;
  }
  nomEl.className = 'sprite-nom revealed';
  typeEl.className = 'sprite-type revealed';
}

// ── Indice ────────────────────────────────────────────────────────────────────
function toggleIndice() {
  document.getElementById('q-indice').classList.toggle('visible');
}

// ── Reset ─────────────────────────────────────────────────────────────────────
function effacer() {
  document.getElementById('requete').value = '';
  document.getElementById('requete').focus();
  setFeedback('', '');
  document.getElementById('results-zone').innerHTML = '';
}

// ── Valider ───────────────────────────────────────────────────────────────────
async function valider() {
  if (gameMode === 'arcade') { validerArcade(); return; }
  const req = document.getElementById('requete').value.trim();
  if (!req) { setFeedback('> SAISIR UNE REQUETE SQL', 'bad'); return; }

  setFeedback('> ANALYSE EN COURS…', 'ok loader');
  document.getElementById('results-zone').innerHTML = '';
  document.getElementById('btn-val').disabled = true;

  try {
    const resp = await fetch('/valider', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ numero: quete, requete: req }),
    });
    const data = await resp.json();
    document.getElementById('btn-val').disabled = false;
    afficherReponse(data);
  } catch {
    document.getElementById('btn-val').disabled = false;
    setFeedback('> ERREUR: SERVEUR INJOIGNABLE', 'bad');
  }
}

function afficherReponse(data) {
  if (data.erreur_sql) { afficherErreurSQL(data.message); return; }
  if (data.erreur)     { setFeedback('> ERR: ' + data.erreur, 'bad'); return; }

  if (data.succes) {
    soundSucces();
    scores[quete - 1] = true;
    majPips();
    if (data.resultat) buildTable(data.resultat, 'RÉSULTAT', 'r-ok');
    setFeedback('> ' + data.message, 'ok');
    revelerSprite();
    afficherBoutonSuivant();
  } else {
    soundErreur();
    if (scores[quete - 1] !== true) scores[quete - 1] = false;
    majPips();
    setFeedback('> ' + data.message, 'bad');
    if (data.resultat) buildTable(data.resultat, 'CE QUE TA REQUÊTE RETOURNE', 'r-bad');
    if (data.attendu)  buildTable(data.attendu,  'CE QUI ÉTAIT ATTENDU', '');
  }
}

// ── Bouton quête suivante ────────────────────────────────────────────────────
function afficherBoutonSuivant() {
  const btn = document.getElementById('btn-next-quest');
  if (quete === TOTAL) {
    btn.textContent = 'VOIR LE RESULTAT FINAL ▶';
  } else {
    const next = getActe(quete + 1);
    const acteCourant = getActe(quete);
    if (quete === acteCourant.last) {
      btn.textContent = 'ACTE ' + (acteCourant.num + 1) + ' : ' + next.zone.toUpperCase() + ' ▶';
    } else {
      btn.textContent = 'QUÊTE ' + (quete + 1) + ' ▶';
    }
  }
  btn.classList.add('visible');
}

function cacherBoutonSuivant() {
  document.getElementById('btn-next-quest').classList.remove('visible');
}

function nextQuest() {
  cacherBoutonSuivant();
  if (gameMode === 'arcade') { chargerDefiArcade(); return; }
  const acteData = getActe(quete);
  const estDernierDActe = (quete === acteData.last);

  if (quete === TOTAL) {
    afficherFin();
  } else if (estDernierDActe) {
    afficherTransition(acteData, quete + 1);
  } else {
    chargerQuete(quete + 1);
  }
}

// ── Transition entre actes ───────────────────────────────────────────────────
function afficherTransition(acteTermine, prochaineQuete) {
  soundChangementActe();
  transitionNextQ = prochaineQuete;
  const ok = scores.filter(s => s === true).length;
  document.getElementById('tr-badge').textContent = `ACTE ${acteTermine.num} TERMINÉ`;
  document.getElementById('tr-titre').textContent = `${acteTermine.zone.toUpperCase()}\nCOMPLÉTÉ !`;
  document.getElementById('tr-titre').style.whiteSpace = 'pre-line';
  document.getElementById('tr-text').textContent = acteTermine.msg || '';
  document.getElementById('tr-score-val').textContent = ok;
  document.getElementById('transition-popup').classList.remove('hidden');
}

function fermerTransition() {
  document.getElementById('transition-popup').classList.add('hidden');
  if (transitionNextQ) chargerQuete(transitionNextQ);
  transitionNextQ = null;
}

// ── Écran de fin ────────────────────────────────────────────────────────────
function afficherFin() {
  const ok = scores.filter(s => s === true).length;
  const elapsed = startTime ? Math.floor((Date.now() - startTime) / 1000) : 0;
  const h = Math.floor(elapsed / 3600);
  const m = Math.floor((elapsed % 3600) / 60);
  const s = elapsed % 60;
  const tempsStr = h > 0
    ? `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`
    : `${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;

  document.getElementById('fin-ok').textContent    = ok;
  document.getElementById('fin-temps').textContent = tempsStr;
  document.getElementById('ecran-fin').classList.remove('hidden');

  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      document.getElementById('fin-bar').style.width = `${Math.round((ok / TOTAL) * 100)}%`;
    });
  });
}

function rejouer() {
  document.getElementById('ecran-fin').classList.add('hidden');
  document.getElementById('ecran-doc').classList.add('hidden');
  scores = new Array(TOTAL).fill(null);
  quete  = 1;
  startTime = null;
  joueurPseudo = '';
  joueurStarterId = null;
  joueurStarterNom = '';
  selectedStarterId = null;
  gameMode = 'histoire';
  defiCount = 0; defiOk = 0; defiStreak = 0; defiChallengeId = null;
  arcadeNiveau = 0; joueurId = null;
  document.getElementById('arcade-bar').classList.remove('visible');
  document.getElementById('btn-passer').classList.remove('visible');
  document.querySelectorAll('.diff-btn').forEach(b =>
    b.classList.toggle('active', parseInt(b.dataset.niveau) === 0));

  document.getElementById('game-content').style.display = 'none';
  document.getElementById('ecran-intro').style.display  = 'flex';
  document.getElementById('ecran-intro').classList.remove('fade-out');
  document.getElementById('ecran-intro').style.opacity  = '1';
  document.getElementById('step-a').style.display    = 'flex';
  document.getElementById('step-mode').style.display = 'none';
  document.getElementById('step-b').style.display    = 'none';
  document.getElementById('pseudo-input').value = '';
  document.getElementById('prof-text').innerHTML = '';
  document.getElementById('prog-pips').innerHTML = '';
  document.getElementById('prog-pips').style.display = '';
  document.getElementById('act-bar').innerHTML   = '';
  document.getElementById('act-bar').style.display = '';
  document.getElementById('score-histoire').style.display = '';
  document.getElementById('score-arcade').style.display   = 'none';
  document.getElementById('lcd-header-histoire').style.display = '';
  document.getElementById('lcd-header-arcade').style.display   = 'none';
  setFeedback('', '');
  cacherBoutonSuivant();
  document.getElementById('results-zone').innerHTML = '';
  document.getElementById('sprite-frame').classList.remove('visible');
  currentPokemonId = null;
  lancerIntro();
}

// ── Construction d'un tableau LCD ─────────────────────────────────────────────
function buildTable(payload, titre, labelCls) {
  const zone  = document.getElementById('results-zone');
  const block = document.createElement('div');
  block.className = 'r-block';

  const lbl = document.createElement('div');
  lbl.className = `r-label ${labelCls}`;
  lbl.innerHTML = titre + ` <span class="r-count">(${payload.total})</span>`;
  block.appendChild(lbl);

  if (!payload.lignes.length) {
    const p = document.createElement('div');
    p.style.cssText = 'font-size:6px;color:var(--gb-dark);padding:4px 0';
    p.textContent = '> AUCUN RESULTAT';
    block.appendChild(p);
    zone.appendChild(block);
    return;
  }

  const wrap  = document.createElement('div');
  wrap.className = 'table-lcd-wrap';
  const table = document.createElement('table');
  table.className = 'table-lcd';

  const thead = table.createTHead();
  const hrow  = thead.insertRow();
  payload.colonnes.forEach(c => {
    const th = document.createElement('th');
    th.textContent = c.toUpperCase();
    hrow.appendChild(th);
  });

  const tbody = table.createTBody();
  payload.lignes.forEach(row => {
    const tr = tbody.insertRow();
    row.forEach(val => {
      const td = tr.insertCell();
      if (val === null) { td.textContent = 'NULL'; td.className = 'null-v'; }
      else td.textContent = val;
    });
  });

  wrap.appendChild(table);

  if (payload.total > payload.lignes.length) {
    const note = document.createElement('div');
    note.className = 'table-trunc';
    note.textContent = `… ${payload.total} LIGNES (LIMITE: ${payload.lignes.length})`;
    wrap.appendChild(note);
  }

  block.appendChild(wrap);
  zone.appendChild(block);
}

// ── Feedback ──────────────────────────────────────────────────────────────────
function setFeedback(text, type) {
  const el = document.getElementById('feedback');
  if (!text) { el.className = 'feedback'; return; }
  el.textContent = text;
  el.className = `feedback vis ${type}`;
}

// ══════════════════════════════════════════════════════════════════════════════
// MODE DOCUMENTATION
// ══════════════════════════════════════════════════════════════════════════════

const DOC_TOPICS = [
  { id: 'select-all', titre: 'SELECT *', cat: 'BASES',
    desc: 'Sélectionne toutes les colonnes d\'une table. Pratique pour explorer, mais à éviter en production (coûteux).',
    syntaxe: 'SELECT * FROM table;',
    exemple: 'SELECT * FROM pokemon LIMIT 5;' },
  { id: 'select-cols', titre: 'SELECT colonnes', cat: 'BASES',
    desc: 'Sélectionne uniquement les colonnes dont tu as besoin. Séparées par des virgules.',
    syntaxe: 'SELECT col1, col2 FROM table;',
    exemple: 'SELECT nom, type1, pv FROM pokemon LIMIT 5;' },
  { id: 'alias', titre: 'AS (alias)', cat: 'BASES',
    desc: 'Renomme une colonne dans le résultat avec AS. Très utile avec les fonctions d\'agrégation.',
    syntaxe: 'SELECT col AS nouveau_nom\nFROM table;',
    exemple: 'SELECT nom, pv AS points_de_vie,\n       attaque AS att\nFROM pokemon LIMIT 5;' },
  { id: 'where-eq', titre: 'WHERE =', cat: 'FILTRAGE',
    desc: 'Filtre les lignes selon une valeur exacte. Les chaînes de texte s\'écrivent entre guillemets simples.',
    syntaxe: 'SELECT * FROM table\nWHERE colonne = \'valeur\';',
    exemple: 'SELECT nom, type1 FROM pokemon\nWHERE type1 = \'Feu\';' },
  { id: 'where-comp', titre: 'WHERE <, >, <=, >=', cat: 'FILTRAGE',
    desc: 'Compare des valeurs numériques.',
    syntaxe: 'SELECT * FROM table\nWHERE colonne > valeur;',
    exemple: 'SELECT nom, pv FROM pokemon\nWHERE pv >= 100\nORDER BY pv DESC;' },
  { id: 'and-or', titre: 'AND / OR', cat: 'FILTRAGE',
    desc: 'AND : toutes les conditions doivent être vraies. OR : au moins une condition suffit.',
    syntaxe: 'WHERE cond1 AND cond2\nWHERE cond1 OR cond2',
    exemple: 'SELECT nom FROM pokemon\nWHERE type1 = \'Eau\' AND pv > 80;' },
  { id: 'like', titre: 'LIKE', cat: 'FILTRAGE',
    desc: '% remplace n\'importe quelle suite de caractères. _ remplace exactement 1 caractère.',
    syntaxe: 'WHERE col LIKE \'début%\'\nWHERE col LIKE \'%fin\'\nWHERE col LIKE \'%milieu%\'',
    exemple: 'SELECT nom FROM pokemon\nWHERE nom LIKE \'R%\';' },
  { id: 'between', titre: 'BETWEEN', cat: 'FILTRAGE',
    desc: 'Filtre un intervalle. Les deux bornes sont incluses.',
    syntaxe: 'WHERE colonne BETWEEN valeur1 AND valeur2',
    exemple: 'SELECT nom, pv FROM pokemon\nWHERE pv BETWEEN 80 AND 100;' },
  { id: 'null', titre: 'IS NULL / NOT NULL', cat: 'FILTRAGE',
    desc: 'NULL = valeur absente. Ne jamais utiliser = NULL : toujours IS NULL ou IS NOT NULL.',
    syntaxe: 'WHERE colonne IS NULL\nWHERE colonne IS NOT NULL',
    exemple: 'SELECT nom, type2 FROM pokemon\nWHERE type2 IS NOT NULL\nLIMIT 5;' },
  { id: 'in', titre: 'IN', cat: 'FILTRAGE',
    desc: 'Vérifie si une valeur appartient à une liste.',
    syntaxe: 'WHERE colonne IN (val1, val2, val3)',
    exemple: 'SELECT nom FROM pokemon\nWHERE type1 IN (\'Feu\', \'Eau\', \'Plante\');' },
  { id: 'order', titre: 'ORDER BY', cat: 'TRI',
    desc: 'Trie les résultats. ASC = croissant (défaut). DESC = décroissant.',
    syntaxe: 'SELECT ... ORDER BY col DESC;\nSELECT ... ORDER BY col1 ASC, col2 DESC;',
    exemple: 'SELECT nom, vitesse\nFROM pokemon\nORDER BY vitesse DESC\nLIMIT 10;' },
  { id: 'limit', titre: 'LIMIT / OFFSET', cat: 'TRI',
    desc: 'LIMIT n : au maximum n lignes. OFFSET k : saute les k premières lignes.',
    syntaxe: 'SELECT ... LIMIT n;\nSELECT ... LIMIT n OFFSET k;',
    exemple: '-- Pokémon 11 à 15\nSELECT nom FROM pokemon\nORDER BY id\nLIMIT 5 OFFSET 10;' },
  { id: 'count', titre: 'COUNT', cat: 'AGRÉGATS',
    desc: 'Compte les lignes. COUNT(*) compte tout. COUNT(col) ignore les NULL.',
    syntaxe: 'SELECT COUNT(*) FROM table;\nSELECT COUNT(col) FROM table;',
    exemple: 'SELECT COUNT(*) FROM pokemon\nWHERE type1 = \'Eau\';' },
  { id: 'agg', titre: 'SUM / AVG / MAX / MIN', cat: 'AGRÉGATS',
    desc: 'Fonctions d\'agrégation sur une colonne numérique.',
    syntaxe: 'SELECT SUM(col), AVG(col),\n       MAX(col), MIN(col)\nFROM table;',
    exemple: 'SELECT ROUND(AVG(pv), 1) AS moy_pv,\n       MAX(attaque) AS max_att\nFROM pokemon;' },
  { id: 'group', titre: 'GROUP BY', cat: 'AGRÉGATS',
    desc: 'Regroupe les lignes partageant la même valeur, puis applique des fonctions d\'agrégation.',
    syntaxe: 'SELECT col, COUNT(*) AS n\nFROM table\nGROUP BY col\nORDER BY n DESC;',
    exemple: 'SELECT type1, COUNT(*) AS total\nFROM pokemon\nGROUP BY type1\nORDER BY total DESC;' },
  { id: 'having', titre: 'HAVING', cat: 'AGRÉGATS',
    desc: 'Filtre les groupes créés par GROUP BY. WHERE filtre avant groupage, HAVING filtre après.',
    syntaxe: 'SELECT col, COUNT(*) AS n\nFROM table\nGROUP BY col\nHAVING n > valeur;',
    exemple: 'SELECT type1, COUNT(*) AS total\nFROM pokemon\nGROUP BY type1\nHAVING total > 10;' },
  { id: 'join', titre: 'JOIN (INNER)', cat: 'JOIN',
    desc: 'Joint deux tables sur une clé commune. Retourne uniquement les lignes avec correspondance.',
    syntaxe: 'SELECT a.col, b.col\nFROM tableA a\nJOIN tableB b ON a.id = b.a_id;',
    exemple: 'SELECT p.nom, c.nom AS capacite\nFROM pokemon p\nJOIN pokemon_capacites pc\n  ON p.id = pc.pokemon_id\nJOIN capacites c\n  ON pc.capacite_id = c.id\nWHERE p.nom = \'Pikachu\';' },
  { id: 'multi-join', titre: 'Chaîner les JOIN', cat: 'JOIN',
    desc: 'Plusieurs JOIN s\'enchaînent pour traverser plusieurs tables.',
    syntaxe: 'FROM A a\nJOIN B b ON a.id = b.a_id\nJOIN C c ON b.id = c.b_id;',
    exemple: 'SELECT DISTINCT p.nom, t.nom AS type_cap\nFROM pokemon p\nJOIN pokemon_capacites pc ON p.id = pc.pokemon_id\nJOIN capacites c ON pc.capacite_id = c.id\nJOIN types t ON c.type_id = t.id\nWHERE p.type1 = \'Eau\'\nLIMIT 10;' },
  { id: 'distinct', titre: 'DISTINCT', cat: 'JOIN',
    desc: 'Élimine les doublons dans les résultats.',
    syntaxe: 'SELECT DISTINCT col FROM table;',
    exemple: 'SELECT DISTINCT type1\nFROM pokemon\nORDER BY type1;' },
  { id: 'subquery', titre: 'Sous-requête', cat: 'AVANCÉ',
    desc: 'Requête imbriquée dans WHERE, FROM ou SELECT.',
    syntaxe: 'SELECT ...\nWHERE col > (SELECT AVG(col) FROM table);',
    exemple: 'SELECT nom, attaque\nFROM pokemon\nWHERE attaque > (\n  SELECT AVG(attaque) FROM pokemon\n)\nORDER BY attaque DESC;' },
  { id: 'correlated', titre: 'Sous-requête corrélée', cat: 'AVANCÉ',
    desc: 'Sous-requête qui référence la requête externe via un alias.',
    syntaxe: 'SELECT ... FROM tableA a\nWHERE val > (\n  SELECT AVG(val) FROM tableA b\n  WHERE b.groupe = a.groupe\n);',
    exemple: 'SELECT nom, pv, type1\nFROM pokemon p\nWHERE pv > (\n  SELECT AVG(pv) FROM pokemon p2\n  WHERE p2.type1 = p.type1\n);' },
  { id: 'exists', titre: 'EXISTS / NOT EXISTS', cat: 'AVANCÉ',
    desc: 'EXISTS retourne vrai si la sous-requête produit au moins une ligne.',
    syntaxe: 'SELECT ...\nWHERE EXISTS\n  (SELECT 1 FROM ... WHERE ...)',
    exemple: 'SELECT p.nom\nFROM pokemon p\nWHERE EXISTS (\n  SELECT 1 FROM pokemon_capacites pc\n  JOIN capacites c ON c.id = pc.capacite_id\n  WHERE pc.pokemon_id = p.id\n    AND c.puissance > 100\n);' },
  { id: 'not-in', titre: 'NOT IN', cat: 'AVANCÉ',
    desc: 'Exclut les valeurs présentes dans une liste ou sous-requête.',
    syntaxe: 'WHERE col NOT IN (SELECT col FROM ...)',
    exemple: 'SELECT nom FROM pokemon\nWHERE type1 NOT IN (\n  SELECT DISTINCT type1\n  FROM pokemon\n  WHERE est_legendaire = 1\n)\nORDER BY type1;' },
];

const SCHEMA_TABLES = [
  { nom: 'pokemon', color: '#A8A8A8',
    cols: [
      { nom: 'id',             type: 'INTEGER', badge: 'PK' },
      { nom: 'nom',            type: 'TEXT' },
      { nom: 'type1',          type: 'TEXT' },
      { nom: 'type2',          type: 'TEXT',    badge: 'NULL' },
      { nom: 'pv',             type: 'INTEGER' },
      { nom: 'attaque',        type: 'INTEGER' },
      { nom: 'defense',        type: 'INTEGER' },
      { nom: 'vitesse',        type: 'INTEGER' },
      { nom: 'est_legendaire', type: 'INTEGER' },
    ],
    rels: [],
  },
  { nom: 'types', color: '#A8A8A8',
    cols: [
      { nom: 'id',  type: 'INTEGER', badge: 'PK' },
      { nom: 'nom', type: 'TEXT' },
    ],
    rels: [],
  },
  { nom: 'capacites', color: '#A8A8A8',
    cols: [
      { nom: 'id',        type: 'INTEGER', badge: 'PK' },
      { nom: 'nom',       type: 'TEXT' },
      { nom: 'type_id',   type: 'INTEGER', badge: 'FK', fkRef: 'types.id' },
      { nom: 'puissance', type: 'INTEGER', badge: 'NULL' },
      { nom: 'precision', type: 'INTEGER', badge: 'NULL' },
      { nom: 'categorie', type: 'TEXT',    badge: 'NULL' },
    ],
    rels: ['type_id → types.id'],
  },
  { nom: 'pokemon_capacites', color: '#A8A8A8',
    cols: [
      { nom: 'pokemon_id',  type: 'INTEGER', badge: 'FK', fkRef: 'pokemon.id' },
      { nom: 'capacite_id', type: 'INTEGER', badge: 'FK', fkRef: 'capacites.id' },
    ],
    rels: ['pokemon_id → pokemon.id', 'capacite_id → capacites.id'],
  },
];

function allerDocumentation() {
  document.getElementById('step-mode').style.display = 'none';
  const overlay = document.getElementById('ecran-intro');
  overlay.classList.add('fade-out');
  setTimeout(() => {
    overlay.style.display = 'none';
    document.getElementById('ecran-doc').classList.remove('hidden');
    buildDocReference();
    buildDocSchema();
  }, 700);
}

function retourMenuDepuisDoc() {
  document.getElementById('ecran-doc').classList.add('hidden');
  document.getElementById('doc-requete').value = '';
  docFeedback('', '');
  document.getElementById('doc-results').innerHTML = '';
  const overlay = document.getElementById('ecran-intro');
  overlay.style.display = 'flex';
  overlay.style.opacity = '1';
  overlay.classList.remove('fade-out');
  document.getElementById('step-a').style.display = 'none';
  document.getElementById('step-b').style.display = 'none';
  document.getElementById('step-mode').style.display = 'flex';
}

function switchDocTab(tab) {
  document.querySelectorAll('.doc-tab').forEach(t => t.classList.remove('active'));
  document.getElementById('tab-' + tab).classList.add('active');
  document.getElementById('doc-section-ref').classList.toggle('hidden', tab !== 'ref');
  document.getElementById('doc-section-schema').classList.toggle('hidden', tab !== 'schema');
}

function buildDocReference() {
  const grid = document.getElementById('doc-ref-grid');
  if (grid.children.length > 0) return;
  DOC_TOPICS.forEach(topic => {
    const card = document.createElement('div');
    card.className = 'topic-card';
    card.id = 'topic-' + topic.id;

    const header = document.createElement('div');
    header.className = 'topic-header';
    const cat = document.createElement('span');
    cat.className = 'topic-cat';
    cat.dataset.cat = topic.cat;
    cat.textContent = topic.cat;
    const nom = document.createElement('span');
    nom.className = 'topic-nom';
    nom.textContent = topic.titre;
    const arrow = document.createElement('span');
    arrow.className = 'topic-arrow';
    arrow.textContent = '›';
    header.append(cat, nom, arrow);
    header.addEventListener('click', () => card.classList.toggle('expanded'));

    const body = document.createElement('div');
    body.className = 'topic-body';

    const desc = document.createElement('div');
    desc.className = 'topic-desc';
    desc.textContent = topic.desc;

    const lSyntaxe = document.createElement('div');
    lSyntaxe.className = 'topic-code-label';
    lSyntaxe.textContent = 'SYNTAXE';
    const syntaxe = document.createElement('div');
    syntaxe.className = 'topic-code';
    syntaxe.textContent = topic.syntaxe;

    const lExemple = document.createElement('div');
    lExemple.className = 'topic-code-label';
    lExemple.textContent = 'EXEMPLE KANTO (cliquer pour essayer)';
    const exemple = document.createElement('div');
    exemple.className = 'topic-code exemple';
    exemple.textContent = topic.exemple;
    exemple.addEventListener('click', () => essayerExemple(topic.exemple));

    const btnEss = document.createElement('button');
    btnEss.className = 'btn-essayer';
    btnEss.textContent = '▶ ESSAYER';
    btnEss.addEventListener('click', () => essayerExemple(topic.exemple));

    body.append(desc, lSyntaxe, syntaxe, lExemple, exemple, btnEss);
    card.append(header, body);
    grid.appendChild(card);
  });
}

function buildDocSchema() {
  const grid = document.getElementById('schema-grid');
  if (grid.children.length > 0) return;
  SCHEMA_TABLES.forEach(tbl => {
    const card = document.createElement('div');
    card.className = 'schema-table-card';
    card.style.borderColor = tbl.color + '44';

    const hdr = document.createElement('div');
    hdr.className = 'schema-table-header';
    hdr.style.cssText = `background:${tbl.color}18;color:${tbl.color};border-bottom:1px solid ${tbl.color}44`;
    hdr.textContent = tbl.nom.toUpperCase();
    card.appendChild(hdr);

    const colsWrap = document.createElement('div');
    colsWrap.className = 'schema-table-cols';
    tbl.cols.forEach(c => {
      const row = document.createElement('div');
      row.className = 'schema-col-row';
      const cName = document.createElement('span');
      cName.className = 'schema-col-name' + (c.badge === 'PK' ? ' pk' : '');
      cName.textContent = c.nom;
      const cType = document.createElement('span');
      cType.className = 'schema-col-type';
      cType.textContent = c.type;
      row.append(cName, cType);
      if (c.badge) {
        const badge = document.createElement('span');
        badge.className = 'schema-col-badge ' + c.badge.toLowerCase();
        badge.textContent = c.badge;
        if (c.fkRef) badge.title = '→ ' + c.fkRef;
        row.appendChild(badge);
      }
      colsWrap.appendChild(row);
    });
    card.appendChild(colsWrap);

    if (tbl.rels.length) {
      const relNote = document.createElement('div');
      relNote.className = 'schema-rel-note';
      relNote.innerHTML = tbl.rels.map(r => `<span>${r}</span>`).join('<br>');
      card.appendChild(relNote);
    }
    grid.appendChild(card);
  });
}

function essayerExemple(sql) {
  document.getElementById('doc-requete').value = sql;
  document.getElementById('doc-requete').scrollIntoView({ behavior: 'smooth', block: 'center' });
  setTimeout(() => document.getElementById('doc-requete').focus(), 300);
}

function viderSandbox() {
  document.getElementById('doc-requete').value = '';
  docFeedback('', '');
  document.getElementById('doc-results').innerHTML = '';
  document.getElementById('doc-requete').focus();
}

async function executerDocSQL() {
  const req = document.getElementById('doc-requete').value.trim();
  if (!req) { docFeedback('> SAISIR UNE REQUÊTE SQL', 'err'); return; }

  docFeedback('> EXÉCUTION EN COURS…', 'ok');
  document.getElementById('doc-results').innerHTML = '';
  const btn = document.getElementById('btn-doc-exec');
  btn.disabled = true;

  try {
    const r = await fetch('/executer', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ requete: req }),
    });
    const d = await r.json();
    btn.disabled = false;

    if (!d.succes || d.erreur_sql) {
      docFeedback('> ERREUR SQL : ' + (d.message || d.erreur_sql || 'inconnue'), 'err');
      return;
    }
    const n = d.resultat.total;
    docFeedback(`> ${n} LIGNE${n !== 1 ? 'S' : ''} RETOURNÉE${n !== 1 ? 'S' : ''}`, 'ok');
    if (d.resultat.lignes.length) buildDocTable(d.resultat);
    else {
      const p = document.createElement('div');
      p.style.cssText = 'font-size:6px;color:var(--gb-dark);padding:4px 0';
      p.textContent = '> AUCUN RÉSULTAT';
      document.getElementById('doc-results').appendChild(p);
    }
  } catch {
    btn.disabled = false;
    docFeedback('> ERREUR : SERVEUR INJOIGNABLE', 'err');
  }
}

function buildDocTable(payload) {
  const res = document.getElementById('doc-results');
  const wrap = document.createElement('div');
  wrap.className = 'table-lcd-wrap';
  const table = document.createElement('table');
  table.className = 'table-lcd';
  const thead = table.createTHead();
  const hrow = thead.insertRow();
  payload.colonnes.forEach(c => {
    const th = document.createElement('th');
    th.textContent = c.toUpperCase();
    hrow.appendChild(th);
  });
  const tbody = table.createTBody();
  payload.lignes.forEach(row => {
    const tr = tbody.insertRow();
    row.forEach(val => {
      const td = tr.insertCell();
      if (val === null) { td.textContent = 'NULL'; td.className = 'null-v'; }
      else td.textContent = val;
    });
  });
  wrap.appendChild(table);
  if (payload.total > payload.lignes.length) {
    const note = document.createElement('div');
    note.className = 'table-trunc';
    note.textContent = `… ${payload.total} LIGNES (LIMITE: ${payload.lignes.length})`;
    wrap.appendChild(note);
  }
  res.appendChild(wrap);
}

function docFeedback(text, type) {
  const el = document.getElementById('doc-feedback');
  if (!text) { el.className = ''; el.textContent = ''; return; }
  el.textContent = text;
  el.className = `vis ${type}`;
}

// ── Pokéball aide rapide ───────────────────────────────────────────────────────
function toggleHelp() {
  document.getElementById('pokeball-help').classList.toggle('hidden');
}

// ── Son 8-bit (Web Audio API) ─────────────────────────────────────────────────
let _audioCtx  = null;
let soundEnabled = true;

function _getCtx() {
  if (!_audioCtx) _audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  return _audioCtx;
}

function _bip(freq, dur, type = 'square', vol = 0.08, delay = 0) {
  if (!soundEnabled) return;
  try {
    const ctx  = _getCtx();
    const osc  = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.type = type;
    osc.frequency.value = freq;
    const t = ctx.currentTime + delay;
    gain.gain.setValueAtTime(vol, t);
    gain.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    osc.start(t);
    osc.stop(t + dur + 0.01);
  } catch { /* silencieux si contexte audio bloqué */ }
}

function soundSucces() {
  _bip(523, 0.10, 'square', 0.07, 0.00);
  _bip(659, 0.10, 'square', 0.07, 0.11);
  _bip(784, 0.22, 'square', 0.09, 0.22);
}

function soundErreur() {
  _bip(330, 0.10, 'square', 0.07, 0.00);
  _bip(220, 0.18, 'square', 0.07, 0.10);
}

function soundChangementActe() {
  const notes = [523, 659, 784, 1047];
  notes.forEach((n, i) => _bip(n, 0.14, 'square', 0.07, i * 0.13));
}

function toggleSound() {
  soundEnabled = !soundEnabled;
  _updateSoundBtn();
  AudioManager.syncVolume();
}
