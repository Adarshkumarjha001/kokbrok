/* ============================================================
   KOKBOROK NLP — MAIN SCRIPT
   Three.js gold particles · API calls · Animations
   ============================================================ */

const API_BASE_URL = 'http://localhost:5000';

const POS_TAGS = [
  { tag:'NOUN',  color:'#D4922A', label:'Noun'              },
  { tag:'VERB',  color:'#2E8B7A', label:'Verb'              },
  { tag:'PRON',  color:'#C0392B', label:'Pronoun'           },
  { tag:'ADJ',   color:'#7B68EE', label:'Adjective'         },
  { tag:'ADV',   color:'#E67E22', label:'Adverb'            },
  { tag:'ADP',   color:'#3D5A8A', label:'Adposition'        },
  { tag:'AUX',   color:'#27AE60', label:'Auxiliary'         },
  { tag:'DET',   color:'#8E44AD', label:'Determiner'        },
  { tag:'NUM',   color:'#F39C12', label:'Numeral'           },
  { tag:'PART',  color:'#16A085', label:'Particle'          },
  { tag:'CCONJ', color:'#D35400', label:'Co. Conjunction'   },
  { tag:'SCONJ', color:'#2980B9', label:'Sub. Conjunction'  },
  { tag:'PROPN', color:'#E74C3C', label:'Proper Noun'       },
  { tag:'INTJ',  color:'#F1C40F', label:'Interjection'      },
  { tag:'PUNCT', color:'#95A5A6', label:'Punctuation'       },
  { tag:'X',     color:'#7F8C8D', label:'Other'             },
  { tag:'UNK',   color:'#BDC3C7', label:'Unknown'           },
];

const TAG_COLOR = {};
POS_TAGS.forEach(t => { TAG_COLOR[t.tag] = t.color; });

/* ── THREE.JS — 800 GOLD MOTES ─────────────────────────────── */
function initParticles() {
  const canvas = document.getElementById('webgl-canvas');
  if (!canvas || typeof THREE === 'undefined') return;

  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: false });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
  renderer.setSize(window.innerWidth, window.innerHeight);

  const scene  = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.z = 50;

  const COUNT = 800;
  const geo   = new THREE.BufferGeometry();
  const pos   = new Float32Array(COUNT * 3);
  const vel   = new Float32Array(COUNT * 3);

  for (let i = 0; i < COUNT; i++) {
    pos[i*3]   = (Math.random() - 0.5) * 120;
    pos[i*3+1] = (Math.random() - 0.5) * 120;
    pos[i*3+2] = (Math.random() - 0.5) * 60;
    vel[i*3]   = (Math.random() - 0.5) * 0.008;
    vel[i*3+1] = (Math.random() - 0.5) * 0.006 + 0.003;
    vel[i*3+2] = (Math.random() - 0.5) * 0.003;
  }

  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));

  const mat = new THREE.PointsMaterial({
    color: 0xD4922A, size: 1.2,
    transparent: true, opacity: 0.55, sizeAttenuation: true,
  });

  const points = new THREE.Points(geo, mat);
  scene.add(points);

  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });

  (function loop() {
    requestAnimationFrame(loop);
    const p = points.geometry.attributes.position;
    for (let i = 0; i < COUNT; i++) {
      p.array[i*3]   += vel[i*3];
      p.array[i*3+1] += vel[i*3+1];
      p.array[i*3+2] += vel[i*3+2];
      if (p.array[i*3+1] >  60) p.array[i*3+1] = -60;
      if (p.array[i*3]   >  60) p.array[i*3]   = -60;
      if (p.array[i*3]   < -60) p.array[i*3]   =  60;
    }
    p.needsUpdate = true;
    points.rotation.y += 0.0003;
    renderer.render(scene, camera);
  })();
}

/* ── SCROLL REVEALS ─────────────────────────────────────────── */
function initScrollReveals() {
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach(el => obs.observe(el));
}

/* ── MODEL STATUS ────────────────────────────────────────────── */
async function checkModelStatus() {
  const dot  = document.getElementById('status-dot');
  const txt  = document.getElementById('status-text');
  if (!dot || !txt) return;
  dot.className = 'status-dot loading';
  txt.textContent = 'Connecting…';
  try {
    const res  = await fetch(`${API_BASE_URL}/`, { signal: AbortSignal.timeout(8000) });
    const data = await res.json();
    if (data.model_loaded) {
      dot.className = 'status-dot ready';
      txt.textContent = 'Model Ready';
    } else {
      dot.className = 'status-dot loading';
      txt.textContent = 'Model Loading…';
    }
  } catch {
    dot.className = 'status-dot error';
    txt.textContent = 'API Unreachable';
  }
}

/* ── ANALYZE ─────────────────────────────────────────────────── */
async function analyzeText() {
  const input   = document.getElementById('text-input');
  const spinner = document.getElementById('spinner');
  const btn     = document.querySelector('[onclick="analyzeText()"]');
  const results = document.getElementById('results-area');
  const flex    = document.getElementById('tokens-flex');
  const err     = document.getElementById('error-inline');
  if (!input) return;

  const text = input.value.trim();
  if (!text) { showErr(err, 'Please enter some Kokborok text.'); return; }

  err.style.display = 'none';
  results.classList.remove('visible');
  flex.innerHTML = '';
  spinner.classList.add('visible');
  if (btn) { btn.disabled = true; btn.style.opacity = '0.6'; }

  try {
    const res = await fetch(`${API_BASE_URL}/api/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
      signal: AbortSignal.timeout(30000),
    });
    if (!res.ok) { const e = await res.json(); throw new Error(e.error || `HTTP ${res.status}`); }
    const data = await res.json();
    renderTokens(data.tokens);
  } catch (e) {
    showErr(err, e.message || 'Failed to reach API. Is the backend running on port 5000?');
  } finally {
    spinner.classList.remove('visible');
    if (btn) { btn.disabled = false; btn.style.opacity = '1'; }
  }
}

function showErr(el, msg) {
  if (!el) return;
  el.textContent = '⚠ ' + msg;
  el.style.display = 'block';
}

/* ── RENDER TOKENS ───────────────────────────────────────────── */
function renderTokens(list) {
  const flex    = document.getElementById('tokens-flex');
  const results = document.getElementById('results-area');
  if (!flex || !results) return;
  flex.innerHTML = '';
  results.classList.add('visible');

  list.forEach((tok, i) => {
    const color = TAG_COLOR[tok.tag] || '#BDC3C7';
    const chip  = document.createElement('div');
    chip.className = 'token-chip';
    chip.title     = `${tok.tag} — ${tok.score}% confidence`;
    chip.innerHTML = `
      <span class="token-word">${esc(tok.text)}</span>
      <span class="token-tag" style="background:${color};color:#1A0F0A;">${tok.tag}</span>
      <div class="token-bar-wrap">
        <div class="token-bar" style="width:0%;background:${color};" data-w="${tok.score}%"></div>
      </div>`;
    flex.appendChild(chip);
    setTimeout(() => {
      chip.classList.add('visible');
      chip.querySelector('.token-bar').style.width = chip.querySelector('.token-bar').dataset.w;
    }, i * 40);
  });
}

function esc(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

/* ── LEGEND ──────────────────────────────────────────────────── */
function populateLegend() {
  const grid = document.getElementById('legend-grid');
  if (!grid) return;
  POS_TAGS.forEach(t => {
    const item = document.createElement('div');
    item.className = 'legend-item';
    item.innerHTML = `<span class="legend-swatch" style="background:${t.color};"></span>
                      <span class="legend-name">${t.tag} — ${t.label}</span>`;
    grid.appendChild(item);
  });
}

function toggleLegend() {
  const grid = document.getElementById('legend-grid');
  const btn  = document.querySelector('.legend-toggle');
  if (!grid) return;
  const open = grid.classList.toggle('open');
  if (btn) btn.textContent = open ? '▲ Hide POS Tags' : '▼ Show All POS Tags';
}

/* ── ACCORDION ───────────────────────────────────────────────── */
function toggleAccordion(hdr) {
  const body   = hdr.nextElementSibling;
  const isOpen = body.classList.contains('open');
  document.querySelectorAll('.accordion-body').forEach(b => b.classList.remove('open'));
  document.querySelectorAll('.accordion-header').forEach(h => h.classList.remove('open'));
  if (!isOpen) { body.classList.add('open'); hdr.classList.add('open'); }
}

/* ── CTRL+ENTER in textarea ──────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  const ta = document.getElementById('text-input');
  if (ta) ta.addEventListener('keydown', e => { if (e.key === 'Enter' && e.ctrlKey) analyzeText(); });
});

/* ── INIT ────────────────────────────────────────────────────── */
initParticles();
initScrollReveals();
