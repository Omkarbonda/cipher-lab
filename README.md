# 🔐 Cipher Lab & Secure Vault

> A resume-grade full-stack cryptography playground combining an interactive classical cipher simulator with modern AES-256-GCM encryption.

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.139-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?logo=typescript)](https://typescriptlang.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-v3-38B2AC?logo=tailwind-css)](https://tailwindcss.com)
[![Tests](https://img.shields.io/badge/Tests-136%20passed-brightgreen?logo=pytest)](#testing)

---

## 🧠 What Is This?

**Cipher Lab** demonstrates *why* classical ciphers break — by letting you encode messages and then attack them with cryptanalysis tools (frequency analysis, index of coincidence, brute-force).

**Secure Vault** shows how *real* encryption works — AES-256-GCM with PBKDF2 key derivation, random salts and nonces — the kind of code you'd actually ship in production.

Together they demonstrate: algorithmic thinking, correct use of cryptographic primitives, full-stack engineering, and the judgment to know the difference between an educational toy and something production-grade.

---

## 🏗 Architecture

```
cipher-lab/
├── backend/                          # Python 3.12 + FastAPI
│   ├── app/
│   │   ├── ciphers/                  # Classical cipher implementations (pure functions)
│   │   │   ├── caesar.py             ✅ Caesar — shift encoding/decoding
│   │   │   ├── vigenere.py           ✅ Vigenère — polyalphabetic substitution
│   │   │   ├── substitution.py       ✅ Substitution — 26-char key permutation
│   │   │   ├── playfair.py           ✅ Playfair — 5×5 digraph cipher
│   │   │   ├── rail_fence.py         ✅ Rail Fence — transposition cipher
│   │   │   ├── beaufort.py           ✅ Beaufort — reciprocal polyalphabetic
│   │   │   ├── affine.py             ✅ Affine — linear substitution
│   │   │   └── columnar.py           ✅ Columnar — transposition cipher
│   │   ├── cryptanalysis/            # Attack algorithms
│   │   │   ├── frequency.py          ✅ Letter frequency analysis, chi-squared
│   │   │   ├── index_of_coincidence.py  ✅ IC-based key length estimation
│   │   │   └── brute_force.py        ✅ 7 crack functions (Caesar, Vigenère,
│   │   │                                Substitution, Playfair, Rail Fence,
│   │   │                                Beaufort, Affine)
│   │   ├── vault/                    # AES-256-GCM vault (Phase 5)
│   │   ├── api/                      # FastAPI routers
│   │   │   ├── ciphers.py            ✅ 16 encode/decode endpoints
│   │   │   └── cryptanalysis.py      ✅ Analyze + 5 crack endpoints
│   │   └── main.py                   # App entrypoint + CORS
│   ├── tests/
│   │   ├── test_main.py              ✅ Health check API test
│   │   ├── test_ciphers.py           ✅ 8 cipher test classes (76 tests)
│   │   └── test_cryptanalysis.py     ✅ Frequency, IC, crack tests (59 tests)
│   └── requirements.txt
├── frontend/                         # React 19 + TypeScript + Vite + Tailwind CSS v3
│   └── src/
│       ├── api/
│       │   └── cipherApi.ts          ✅ Typed API client
│       ├── types/
│       │   └── cipher.ts             ✅ Shared types
│       ├── components/
│       │   ├── Header.tsx            ✅ Branding + connection status
│       │   ├── Footer.tsx            ✅ Footer with tech stack
│       │   ├── WorkspaceConsole.tsx  ✅ Input/output + action buttons
│       │   ├── CipherConfig.tsx      ✅ Tabbed cipher configuration
│       │   ├── configs/
│       │   │   ├── CaesarConfig.tsx
│       │   │   ├── VigenereConfig.tsx
│       │   │   ├── SubstitutionConfig.tsx
│       │   │   ├── PlayfairConfig.tsx
│       │   │   ├── RailFenceConfig.tsx
│       │   │   ├── BeaufortConfig.tsx
│       │   │   ├── AffineConfig.tsx
│       │   │   └── ColumnarConfig.tsx
│       │   ├── LiveCryptanalysis.tsx ✅ IC + frequency chart container
│       │   ├── FrequencyBarChart.tsx ✅ 26-letter bar chart
│       │   ├── CrackerResults.tsx    ✅ Crack candidates panel
│       │   └── Toast.tsx             ✅ Toast notification system
│       └── App.tsx                   # Orchestrator — 8 cipher tabs
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

**Current test suite: 136 tests, 136 passed ✅**

| Module | Tests | Coverage |
|---|---|---|
| `test_main.py` | 1 | Health check API |
| `TestCaesar` | 12 | Known vectors, round-trips, edge cases |
| `TestVigenere` | 12 | Known vectors, key stepping, error cases |
| `TestSubstitution` | 11 | Atbash, QWERTY key, validation errors |
| `TestPlayfair` | 10 | Wikipedia vector, J→I merge, padding |
| `TestRailFence` | 8 | Zigzag pattern, non-alpha preservation, edge cases |
| `TestBeaufort` | 8 | Reciprocal property, known vectors, key validation |
| `TestAffine` | 8 | Modular arithmetic, identity, coprime validation |
| `TestColumnar` | 7 | Column order, round-trip, key validation |
| `TestFrequency` | 9 | Counts, relative, chi-squared, scoring |
| `TestIndexCoincidence` | 12 | IC computation, split columns, key length estimation |
| `TestCrackCaesar` | 8 | All 26 shifts, chi-squared ranking, structure |
| `TestCrackVigenere` | 4 | IC-based attack, key recovery |
| `TestCrackRailFence` | 3 | Transposition cracking |
| `TestCrackBeaufort` | 3 | Per-column key search |
| `TestCrackAffine` | 3 | Brute-force all valid (a,b) pairs |
| `TestCrackSubstitution` | 3 | Frequency-mapping attack |
| `TestCrackPlayfair` | 2 | Best-effort keyword brute-force |

---

## 📡 API Reference

### Cipher Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/ciphers/caesar/encode` | Caesar cipher encryption |
| `POST` | `/api/ciphers/caesar/decode` | Caesar cipher decryption |
| `POST` | `/api/ciphers/vigenere/encode` | Vigenère cipher encryption |
| `POST` | `/api/ciphers/vigenere/decode` | Vigenère cipher decryption |
| `POST` | `/api/ciphers/substitution/encode` | Substitution cipher encryption |
| `POST` | `/api/ciphers/substitution/decode` | Substitution cipher decryption |
| `POST` | `/api/ciphers/playfair/encode` | Playfair cipher encryption |
| `POST` | `/api/ciphers/playfair/decode` | Playfair cipher decryption |
| `POST` | `/api/ciphers/railfence/encode` | Rail Fence cipher encryption |
| `POST` | `/api/ciphers/railfence/decode` | Rail Fence cipher decryption |
| `POST` | `/api/ciphers/beaufort/encode` | Beaufort cipher encryption |
| `POST` | `/api/ciphers/beaufort/decode` | Beaufort cipher decryption |
| `POST` | `/api/ciphers/affine/encode` | Affine cipher encryption |
| `POST` | `/api/ciphers/affine/decode` | Affine cipher decryption |
| `POST` | `/api/ciphers/columnar/encode` | Columnar Transposition encryption |
| `POST` | `/api/ciphers/columnar/decode` | Columnar Transposition decryption |

### Cryptanalysis Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/cryptanalysis/analyze` | Letter frequencies, IC, top-5 letters |
| `POST` | `/api/cryptanalysis/crack/caesar` | Brute-force all 25 Caesar shifts |
| `POST` | `/api/cryptanalysis/crack/vigenere` | IC-based key length + per-column attack |
| `POST` | `/api/cryptanalysis/crack/substitution` | Frequency-mapping substitution crack |
| `POST` | `/api/cryptanalysis/crack/playfair` | Best-effort keyword brute-force |
| `POST` | `/api/cryptanalysis/crack/railfence` | Brute-force rail count 2–10 |
| `POST` | `/api/cryptanalysis/crack/beaufort` | IC-based key length + per-column attack |
| `POST` | `/api/cryptanalysis/crack/affine` | Brute-force all 312 valid (a,b) pairs |

Auto-generated Swagger docs available at `/docs` when the server is running.

---

## 🗺 Project Roadmap

| Phase | Status | Description |
|---|---|---|---|
| **Phase 0** | ✅ Done | Project scaffolding, health check, end-to-end wiring |
| **Phase 1** | ✅ Done | 8 classical ciphers + 136 tests + cryptanalysis attacks |
| **Phase 2** | ✅ Done | Cryptanalysis — frequency analysis, index of coincidence, brute-force cracker (7 attack functions) |
| **Phase 3** | ✅ Done | FastAPI routes: 16 encode/decode endpoints + 6 crack endpoints |
| **Phase 4** | ✅ Done | Frontend cipher UI — 8 cipher tabs, live frequency histogram, toast notifications |
| **Phase 5** | 🔜 Next | Secure Vault — AES-256-GCM, PBKDF2, passphrase entropy estimator |
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

### Rail Fence Cipher
Transposition cipher that writes letters in a zigzag pattern across multiple rails. Key: integer `[2–10]`.
- Preserves case and non-alphabetic characters in original positions
- rails=1 acts as identity transformation
- Decoding reconstructs the zigzag pattern from row-order ciphertext

### Beaufort Cipher
Reciprocal polyalphabetic substitution (encode == decode). Key: any non-empty alphabetic string.
- Formula: E(x) = (K - x) mod 26
- Key only advances on alphabetic characters
- Reciprocal property means encryption and decryption are identical

### Affine Cipher
Mathematical substitution using linear transformation. Key: integer pair `(a, b)` where gcd(a, 26) = 1.
- Formula: E(x) = (a × x + b) mod 26
- Decryption uses modular inverse: D(y) = a⁻¹ × (y − b) mod 26
- a=1, b=0 is the identity transformation
- 312 valid key pairs total

### Columnar Transposition
Transposition cipher using keyword-ordered column reading. Key: any alphabetic string.
- Plaintext written row-wise into a key-width grid
- Columns read in alphabetical order of key characters
- Non-alphabetic characters are stripped before encoding

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
