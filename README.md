# 🔐 Cipher Lab & Secure Vault

> A resume-grade full-stack cryptography playground combining an interactive classical cipher simulator with modern AES-256-GCM encryption.

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.139-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?logo=typescript)](https://typescriptlang.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-v3-38B2AC?logo=tailwind-css)](https://tailwindcss.com)
[![Tests](https://img.shields.io/badge/Tests-46%20passed-brightgreen?logo=pytest)](#testing)

---

## 🧠 What Is This?

**Cipher Lab** demonstrates *why* classical ciphers break — by letting you encode messages and then attack them with cryptanalysis tools (frequency analysis, index of coincidence, brute-force).

**Secure Vault** shows how *real* encryption works — AES-256-GCM with PBKDF2 key derivation, random salts and nonces — the kind of code you'd actually ship in production.

Together they demonstrate: algorithmic thinking, correct use of cryptographic primitives, full-stack engineering, and the judgment to know the difference between an educational toy and something production-grade.

---

## 🏗 Architecture

```
cipher-lab/
├── backend/                     # Python 3.12 + FastAPI
│   ├── app/
│   │   ├── ciphers/             # Classical cipher implementations (pure functions)
│   │   │   ├── caesar.py        ✅ Caesar cipher — shift encoding/decoding
│   │   │   ├── vigenere.py      ✅ Vigenère — polyalphabetic substitution
│   │   │   ├── substitution.py  ✅ Simple substitution — 26-char key permutation
│   │   │   └── playfair.py      ✅ Playfair — 5×5 digraph cipher
│   │   ├── cryptanalysis/       # Attack algorithms (Phase 2)
│   │   ├── vault/               # AES-256-GCM vault (Phase 5)
│   │   ├── api/                 # FastAPI routers (Phase 3)
│   │   └── main.py              # App entrypoint + CORS
│   ├── tests/
│   │   ├── test_main.py         ✅ Health check API test
│   │   └── test_ciphers.py      ✅ 45 cipher unit tests
│   └── requirements.txt
├── frontend/                    # React 19 + TypeScript + Vite + Tailwind CSS v3
│   └── src/
│       ├── components/          # Reusable UI components (Phase 4)
│       ├── pages/               # Page-level components (Phase 4)
│       └── App.tsx              # Landing page + health check dashboard
└── README.md
```

**Key design principle:** cipher logic, cryptanalysis logic, and the "real crypto" vault are three separate modules that never import from each other — educational/breakable code paths are fully isolated from production-grade code.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+ (v24 recommended)
- Git

---

### Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn app.main:app --reload --port 8000
```

The API will be live at **http://localhost:8000**
Interactive docs (Swagger UI): **http://localhost:8000/docs**

---

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

The frontend will be live at **http://localhost:5173**

> The Vite dev server proxies all `/api/*` requests to the backend on port 8000 — no CORS setup needed during local development.

---

## 🧪 Testing

```bash
cd backend

# Run all tests with verbose output
python -m pytest tests/ -v
```

**Current test suite: 46 tests, 46 passed ✅**

| Module | Tests | Coverage |
|---|---|---|
| `test_main.py` | 1 | Health check API |
| `TestCaesar` | 12 | Known vectors, round-trips, edge cases |
| `TestVigenere` | 12 | Known vectors, key stepping, error cases |
| `TestSubstitution` | 11 | Atbash, QWERTY key, validation errors |
| `TestPlayfair` | 10 | Wikipedia vector, J→I merge, padding |

---

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health check → `{"status": "ok"}` |
| — | — | *More routes coming in Phase 3* |

Auto-generated Swagger docs available at `/docs` when the server is running.

---

## 🗺 Project Roadmap

| Phase | Status | Description |
|---|---|---|
| **Phase 0** | ✅ Done | Project scaffolding, health check, end-to-end wiring |
| **Phase 1** | ✅ Done | Caesar, Vigenère, Substitution, Playfair ciphers + 46 tests |
| **Phase 2** | 🔜 Next | Cryptanalysis — frequency analysis, index of coincidence, brute-force cracker |
| **Phase 3** | 🔜 | FastAPI routes: `/encode`, `/decode`, `/analyze`, `/crack` |
| **Phase 4** | 🔜 | Frontend cipher UI — animated rotors, live frequency histogram |
| **Phase 5** | 🔜 | Secure Vault — AES-256-GCM, PBKDF2, passphrase entropy estimator |
| **Phase 6** | 🔜 | Polish, deployment (Render + Vercel), architecture write-up |

---

## 🔒 Classical Ciphers Implemented

### Caesar Cipher
Shifts each letter by a fixed number of positions. Key: integer `[0–25]`.
- Preserves case and non-alphabetic characters
- Shift is reduced modulo 26 (any integer accepted)

### Vigenère Cipher
Polyalphabetic substitution using a repeating keyword. Key: any non-empty alphabetic string.
- Non-alpha characters pass through unchanged
- Keyword index only advances on alphabetic characters

### Substitution Cipher
Maps each letter to a unique replacement letter. Key: 26-char permutation of the alphabet.
- Key validated for distinctness (exactly 26 unique letters)
- Preserves case; non-alpha characters unchanged

### Playfair Cipher
5×5 key-square digraph substitution. Key: any keyword.
- I and J merged into a single cell
- X inserted between repeated letters in a pair
- Output always uppercase, even-length

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, FastAPI, Uvicorn |
| Crypto (Phase 5) | `cryptography` (PyCA) — AES-256-GCM, PBKDF2 |
| Frontend | React 19, TypeScript, Vite |
| Styling | Tailwind CSS v3 |
| Testing | pytest, FastAPI TestClient |
| Deployment | Render (backend), Vercel (frontend) — *coming Phase 6* |

---

## 📝 Resume Blurb

> **Cipher Lab & Secure Vault** — Full-stack cryptography playground (Python/FastAPI, React/TypeScript). Implemented classical ciphers alongside cryptanalysis tools (frequency analysis, index-of-coincidence attacks) to demonstrate algorithmic understanding, plus a production-grade AES-256-GCM vault with PBKDF2 key derivation to demonstrate correct use of modern cryptographic primitives.

---

## 📄 License

MIT
