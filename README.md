# 🌐 Kokborok Language NLP Model

> **Advanced Part-of-Speech (POS) Tagging for the Kokborok language**, powered by a fine-tuned XLM-RoBERTa transformer model. This project combines a Flask REST API backend with an interactive 3D-animated frontend to bring state-of-the-art NLP to an indigenous Indian language.

[![Model on HuggingFace](https://img.shields.io/badge/🤗%20HuggingFace-ritik3412%2FKokborok__model-yellow)](https://huggingface.co/ritik3412/Kokborok_model)
[![Backend: Flask](https://img.shields.io/badge/Backend-Flask-green)](https://flask.palletsprojects.com/)
[![Frontend: HTML/CSS/JS](https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-blue)]()
[![Deployed on Render](https://img.shields.io/badge/Deploy-Render-purple)](https://render.com)
[![Deployed on Vercel](https://img.shields.io/badge/Deploy-Vercel-black)](https://vercel.com)

---

## 📸 Overview

The **Kokborok NLP Model** is a full-stack web application that lets users type or paste Kokborok text and instantly receive a color-coded, confidence-scored Part-of-Speech analysis. The UI features a **3D WebGL animated background** (Three.js), **glassmorphism design**, and smooth scroll-reveal animations.

---

## 📁 Project Structure

```
Kokborok_Model/
├── backend/                    # 🔧 Flask REST API
│   ├── app.py                  # Main server — model loading & inference endpoints
│   ├── requirements.txt        # Python dependencies
│   ├── Procfile                # Render/Gunicorn start command
│   ├── render.yaml             # Render.com blueprint config
│   ├── .env                    # Environment variables (MODEL_NAME, PORT)
│   └── .gitignore
│
├── frontend/                   # 🎨 Static Website
│   ├── index.html              # Home page — interactive POS demo
│   ├── history.html            # Kokborok language history page
│   ├── importance.html         # Why this research matters
│   ├── technology.html         # Technology stack explained
│   ├── styles.css              # Full glassmorphism + 3D styling
│   ├── script.js               # Frontend logic, API calls, 3D scene
│   └── vercel.json             # Vercel deployment config
│
├── start.bat                   # ▶ One-click local launcher (Windows)
├── requirements.txt            # Root-level Python deps
├── model.safetensors           # Local model weights (1.06 GB)
├── tokenizer.json              # Tokenizer vocab
└── README.md                   # This file
```

---

## 🚀 Running Locally

### Prerequisites

- Python 3.9+
- pip

### Option 1 — One Click (Windows)

Simply double-click **`start.bat`** in the project root.

It will:

1. Start the **Flask backend** on `http://localhost:5000`
2. Start the **frontend HTTP server** on `http://localhost:8001`

> ⏳ Wait ~30–60 seconds for the model to load, then open [http://localhost:8001](http://localhost:8001)

---

### Option 2 — Manual Setup

**Step 1: Install backend dependencies**

```bash
cd backend
pip install -r requirements.txt
```

**Step 2: Start the backend server**

```bash
python app.py
```

> Backend runs at `http://localhost:5000`

**Step 3: Start the frontend server** (in a new terminal)

```bash
cd frontend
python -m http.server 8001
```

> Frontend runs at `http://localhost:8001`

**Step 4: Open your browser** and navigate to [http://localhost:8001](http://localhost:8001)

---

## 🌍 Deployment

### Backend → Render.com

1. Go to [render.com](https://render.com) → **New Web Service**
2. Connect your GitHub repository
3. Set **Root Directory** to `backend`
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120`
   - **Environment**: Python 3
5. Add environment variable: `MODEL_NAME` = `ritik3412/Kokborok_model`
6. Deploy and note your URL (e.g., `https://kokborok-api.onrender.com`)

### Frontend → Vercel

1. Update `API_BASE_URL` in `frontend/script.js` (line ~4) to your Render URL:

   ```javascript
   const API_BASE_URL = 'https://kokborok-api.onrender.com';
   ```

2. Go to [vercel.com](https://vercel.com) → **Import Project**
3. Connect your GitHub repository
4. Set **Root Directory** to `frontend`
5. Framework Preset: **Other** → Deploy

---

## 📡 API Reference

### `GET /`

Health check — confirms model load status.

**Response:**

```json
{
  "status": "ready",
  "model_loaded": true,
  "model_name": "ritik3412/Kokborok_model"
}
```

---

### `POST /api/analyze`

Analyze Kokborok text and return POS tags with confidence scores.

**Request:**

```json
{ "text": "Ang nwng kwrwi sa." }
```

**Response:**

```json
{
  "tokens": [
    { "text": "Ang",   "tag": "PRON",  "score": 97.3 },
    { "text": "nwng",  "tag": "ADP",   "score": 94.1 },
    { "text": "kwrwi", "tag": "VERB",  "score": 91.8 },
    { "text": "sa",    "tag": "PART",  "score": 88.5 }
  ]
}
```

---

### `GET /api/model-info`

Returns model architecture metadata.

**Response:**

```json
{
  "architecture": "XLMRobertaForTokenClassification",
  "num_labels": 17,
  "labels": ["ADJ", "ADP", "ADV", "AUX", ...],
  "vocab_size": 250002,
  "max_length": 512
}
```

---

## 🤖 Model Details

| Property | Value |
|---|---|
| **Architecture** | XLM-RoBERTa (Token Classification) |
| **Task** | Named Entity Recognition / POS Tagging |
| **Parameters** | ~125 Million |
| **Hidden Size** | 768 dimensions |
| **Transformer Layers** | 12 |
| **Attention Heads** | 12 |
| **POS Tag Categories** | 17 |
| **Max Sequence Length** | 512 tokens |
| **HuggingFace Hub** | [ritik3412/Kokborok_model](https://huggingface.co/ritik3412/Kokborok_model) |

---

## 🏷️ POS Tag Reference

| Tag | Full Name | Example |
|-----|-----------|---------|
| `NOUN` | Noun | kwrwi (work) |
| `VERB` | Verb | phang (go) |
| `PRON` | Pronoun | ang (I), nwng (you) |
| `ADJ` | Adjective | naior (good) |
| `ADV` | Adverb | chwkna (quickly) |
| `ADP` | Adposition | khamni (with) |
| `AUX` | Auxiliary Verb | — |
| `DET` | Determiner | — |
| `NUM` | Numeral | phai (one) |
| `PART` | Particle | sa, ya |
| `CCONJ` | Coordinating Conjunction | ebola (and) |
| `SCONJ` | Subordinating Conjunction | — |
| `PROPN` | Proper Noun | Tripura |
| `INTJ` | Interjection | — |
| `PUNCT` | Punctuation | . , ? |
| `X` | Other | — |
| `UNK` | Unknown | — |

---

## 🎨 Frontend Features

- **3D WebGL Background** — Animated particle/mesh scene via Three.js with OrbitControls
- **Glassmorphism UI** — Frosted glass cards with blur, glow effects, and depth
- **Scroll Animations** — GSAP + ScrollTrigger powered reveal animations
- **Interactive Demo** — Real-time POS analysis with color-coded token display
- **4-Page Website** — Home, History, Importance, Technology
- **Responsive Design** — Adapts to all screen sizes
- **Dark Theme** — Premium dark mode with gradient accents

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **ML Model** | XLM-RoBERTa (HuggingFace Transformers) |
| **Backend** | Python, Flask, Flask-CORS |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **3D Graphics** | Three.js r128, GSAP 3.12 |
| **Fonts** | Google Fonts (Inter, Outfit) |
| **Hosting (API)** | Render.com (Gunicorn) |
| **Hosting (Web)** | Vercel |

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Model not loading | Wait 60s; check terminal for errors |
| `ModuleNotFoundError` | Run `pip install -r backend/requirements.txt` |
| CORS errors in browser | Ensure backend is running on port 5000 |
| Frontend shows "Model Loading..." forever | Check backend is reachable at `http://localhost:5000` |
| Port 5000 already in use | Kill existing process or change `PORT` in `.env` |

---

## 📜 About Kokborok

**Kokborok** (also called Tripuri) is a **Tibeto-Burman language** of the Sino-Tibetan family, spoken by approximately **1 million native speakers** primarily in the Indian state of **Tripura** and parts of Bangladesh. It is one of the **official languages of Tripura** and holds deep cultural significance for the Borok people.

Despite its rich oral tradition dating back centuries, Kokborok remains an **under-resourced language** in the NLP world. This project aims to bridge that gap by applying state-of-the-art multilingual models to preserve and advance the language through technology.

---

## 📄 License

This project is created for **educational and research purposes** to support indigenous language preservation.

---

*© 2025 Kokborok NLP Project — Preserving and Advancing Indigenous Language Technology*
