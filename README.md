# Incredible Journeys: Discover India with AI

[![Architecture](https://img.shields.io/badge/Architecture-FastAPI%20%7C%20ChromaDB%20%7C%20Next.js%2014-C85A32.svg)](#architecture-overview)
[![Coverage](https://img.shields.io/badge/Coverage-28%20States%20%2B%208%20UTs%20(36%20Divisions)-1E3A2F.svg)](#regional-coverage)
[![Zero Hallucination](https://img.shields.io/badge/Zero--Hallucination-Verified%20Grounding-D9822B.svg)](#provenance-and-grounding-policy)
[![License](https://img.shields.io/badge/License-CC--BY--SA%204.0%20%2F%20MIT-C5A869.svg)](#licensing-and-provenance)

Incredible Journeys is an editorial travel web application and conversational RAG tour guide celebrating the living heritage, sacred geography, biodiversity, and culinary soul of India across all 28 states and 8 union territories.

The platform combines a persistent ChromaDB vector index and dynamic live Wikipedia intelligence with an editorial user experience powered by Next.js 14, Tailwind CSS, Three.js, and FastAPI. All features are unified on a single localhost port (http://localhost:3000).

---

## Key Features

### 1. Interactive 3D World Globe and Aeroplane Animation
- Three.js WebGL interactive globe rendered on the landing page hero.
- Seven Wonders of the World pinned on the globe with gold markers and interactive hover cards (Taj Mahal, Great Wall of China, Petra, Colosseum, Christ the Redeemer, Machu Picchu, Chichen Itza).
- Animated passenger aircraft continuously banking and navigating atmospheric orbital flight paths above the globe.

### 2. Verified Subcontinental Destination Atlas
- Curated database of 639 verified destinations covering all 36 administrative divisions (28 states and 8 union territories).
- Filterable by State/Union Territory, Category (Heritage, Forts, Temples, Nature, Wildlife, Food, Festivals), and UNESCO World Heritage status.
- Verified geographic coordinates, ideal visitation seasons, and high-resolution Wikimedia Commons photography (verified architectural and landscape photography without human portraits).
- Direct Google Maps navigation links with coordinates and turn-by-turn directions.

### 3. Subcontinental Gastronomy Atlas
- Comprehensive culinary atlas featuring 30 authentic regional specialties across North, South, East, West, and Northeast India.
- Includes Kozhikode Dum Biryani, Kozhikodan Halwa, Mysore Masala Dosa, Mangalorean Kori Rotti, Hyderabadi Dum Biryani, Chettinad Pepper Chicken, Amritsari Kulcha, Awadhi Galouti Kebab, Litti Chokha, Puran Poli, Khaman Dhokla, Shorshe Ilish, Chhena Poda, Himalayan Momos, Sel Roti, and Assamese Masor Tenga.
- Detailed flavor profiles, cultural origin narratives, authentic pairings, and verified photography.
- Filterable in the Explorer interface under the Food category and queryable through dedicated REST endpoints.

### 4. Polyglot AI Tour Guide with 16 Indian Languages
- Full native language selector supporting:
  - English (en)
  - Hindi (hi)
  - Malayalam (ml)
  - Kannada (kn)
  - Telugu (te)
  - Tulu (tcy)
  - Tamil (ta)
  - Marathi (mr)
  - Punjabi (pa)
  - Bihari / Bhojpuri (bho)
  - Nepali (ne)
  - Bengali (bn)
  - Gujarati (gu)
  - Odia (or)
  - Assamese (as)
  - Urdu (ur)
- Dynamic UI adaptation: Selecting any language updates greetings, starter suggestion pills, input placeholders, and AI responses in native scripts.

### 5. Culturally Grounded Storytelling and Travel Humor
- Warm, local conversational persona that provides sensory storytelling (aromas, architecture, folklore).
- Context-aware local humor and travel jokes in every supported language (such as Kozhikode beach tea stall jokes in Malayalam, Hampi chariot jokes in Kannada, or Sasaram railway station jokes in Bhojpuri).
- Dedicated button to request travel jokes in the active language.

### 6. Omni-Source Knowledge Retrieval
- Local Dense Vector Search: ChromaDB vector database with 700+ indexed passages using multilingual embeddings.
- Culinary Atlas Integration: Automatically surfaces authentic food pairings for places discussed.
- Live Wikipedia and Open Data Fallback: Automatically queries live Wikipedia and Wikidata open APIs when users ask about unindexed landmarks, temples, or off-seed regional destinations.
- Grounded citations: Responses include clickable sources and Google Maps navigation links.

### 7. Unified Single Localhost Architecture
- Both the Next.js frontend and the FastAPI backend are accessible on http://localhost:3000.
- Next.js rewrites reverse-proxy all API traffic (/api/*), OpenAPI specifications (/openapi.json), and interactive documentation (/docs) to the backend service.

---

## Datasets Included in This Distribution

The package includes complete raw, seed, verified, and pre-indexed datasets in both CSV and JSON formats:

| Dataset File | Format | Records | Content Description |
| :--- | :--- | :--- | :--- |
| `dataset.csv` | CSV | 632 rows | Original candidate seed dataset with place names, states, cities, categories, and Wikipedia titles |
| `destinations_verified.csv` | CSV | 639 rows | Enriched destination dataset with verified coordinates, categories, best visitation seasons, Google Maps URLs, and Wikimedia photography URLs |
| `backend/data/destinations.json` | JSON | 639 records | Consolidated single-file JSON array containing complete architectural profiles, historical summaries, coordinates, categories, and image URLs |
| `backend/data/foods.json` | JSON | 30 dishes | Indian regional culinary atlas featuring native names, flavor profiles, origin stories, best places to try, pairings, and verified photography |
| `backend/data/india_regions.json` | JSON | 36 regions | Complete geographic metadata, capital cities, signatures, and destination counts across all 28 states and 8 union territories |
| `backend/data/raw/*.json` | JSON | 639 files | Individual deep-dive destination dossiers with OpenStreetMap coordinates and Wikimedia licensing |
| `backend/data/chroma_db/` | Vector Index | 724 embeddings | Pre-computed, persistent ChromaDB vector index built with the multilingual sentence transformer for immediate dense semantic search |

---

## Architecture Overview

```
                      +---------------------------------------+
                      |    Next.js 14 App Router Frontend     |
                      |   (Three.js, Tailwind CSS, Framer)    |
                      |         http://localhost:3000         |
                      +-------------------+-------------------+
                                          |
                      Reverse Proxy Rewrites (/api/*, /docs)
                                          |
                                          v
                      +---------------------------------------+
                      |         FastAPI Backend Engine        |
                      |         http://127.0.0.1:8000         |
                      +---------+-------------------+---------+
                                |                   |
                      Semantic Vector Search   Dynamic Open API
                                |                   |
                                v                   v
                      +-------------------+   +---------------+
                      | Persistent        |   | Live          |
                      | ChromaDB Index    |   | Wikipedia /   |
                      | (724 Vectors)     |   | Wikidata API  |
                      +-------------------+   +---------------+
                                |                   |
                                +---------+---------+
                                          |
                                          v
                              +-----------------------+
                              | Storytelling Engine   |
                              | (Gemini / Polyglot)   |
                              +-----------------------+
```

---

## Directory Structure

```text
incredible-journeys/
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI application entrypoint
│   │   ├── config.py                   # Environment and path configurations
│   │   ├── api/
│   │   │   └── routes.py               # Legacy API endpoints and health checks
│   │   ├── rag/
│   │   │   ├── embeddings.py           # Multilingual sentence transformer
│   │   │   ├── generator.py            # SSE streaming and grounded response generation
│   │   │   ├── ingest.py               # Idempotent vector ingestion pipeline
│   │   │   ├── retriever.py            # Omni-source vector and live Wikipedia retriever
│   │   │   └── vector_db.py            # Persistent ChromaDB service
│   │   ├── routers/
│   │   │   ├── chat.py                 # Polyglot chat and streaming endpoints
│   │   │   ├── destinations.py         # Destination catalog and geospatial queries
│   │   │   └── foods.py                # Regional culinary atlas endpoints
│   │   └── services/
│   │       ├── llm.py                  # Polyglot storytelling and joke generation service
│   │       ├── memory.py               # Multi-turn conversation memory manager
│   │       ├── query_rewriter.py       # Query normalizer and intent classifier
│   │       └── recommender.py          # Proactive circuit and destination recommender
│   ├── data/
│   │   ├── chroma_db/                  # Persistent ChromaDB vector database files (724 embeddings)
│   │   ├── dataset.csv                 # Seed candidate CSV dataset (632 destinations)
│   │   ├── destinations_verified.csv   # Verified CSV dataset with coordinates & Wikimedia URLs (639 records)
│   │   ├── destinations.json           # Consolidated destination profiles array (639 destinations)
│   │   ├── foods.json                  # Curated culinary atlas dataset (30 authentic dishes)
│   │   ├── india_regions.json          # Administrative division metadata (36 regions)
│   │   ├── ingestion_report.json       # Vector indexing audit report
│   │   ├── places_seed.csv             # Destination seed database
│   │   ├── raw/                        # 639 individual destination JSON profiles
│   │   └── seed_manifest.json          # Dataset licensing and provenance manifest
│   ├── tests/                          # Backend test suite (pytest)
│   ├── requirements.txt                # Python backend dependencies
│   └── .env.example                    # Backend environment configuration template
├── frontend/
│   ├── public/                         # Static assets and icons
│   ├── src/
│   │   ├── app/
│   │   │   ├── about/page.tsx          # Architecture and provenance page
│   │   │   ├── destinations/[slug]/    # Detailed destination dossier with Leaflet map
│   │   │   ├── explore/page.tsx        # Search, state, UNESCO, and food filter catalog
│   │   │   ├── guide/page.tsx          # Fullscreen multilingual AI guide with joke mode
│   │   │   ├── layout.tsx              # Root layout with navigation, drawer, and footer
│   │   │   └── page.tsx                # Hero landing page with 3D Globe and Gastronomy
│   │   ├── components/
│   │   │   ├── chat/
│   │   │   │   ├── ChatMessageItem.tsx # Message bubble with citations and actions
│   │   │   │   ├── GlobalChatDrawer.tsx# Floating drawer with language selector
│   │   │   │   └── LanguageSelector.tsx# 16-Indian-language selection dropdown
│   │   │   ├── globe/
│   │   │   │   └── AnimatedGlobeHero.tsx# Three.js 3D Globe, 7 Wonders, and Aeroplane
│   │   │   ├── map/
│   │   │   │   └── DestinationMap.tsx  # Leaflet / OpenStreetMap interactive viewer
│   │   │   ├── motion/
│   │   │   │   └── MotionWrapper.tsx   # Framer Motion animation utilities
│   │   │   └── ui/
│   │   │       ├── DestinationCard.tsx # Destination card with Google Maps link
│   │   │       ├── FoodCard.tsx        # Authentic food card with photo fallback
│   │   │       ├── Footer.tsx          # Footer with license disclosures
│   │   │       └── Navbar.tsx          # Navigation bar with dark mode toggle
│   │   └── lib/
│   │       ├── api.ts                  # Frontend API client
│   │       ├── foods.json              # Client-side copy of regional culinary atlas
│   │       ├── languages.ts            # Configuration for all 16 Indian languages
│   │       └── types.ts                # TypeScript interfaces and contracts
│   ├── tests/                          # Frontend test suites
│   ├── next.config.js                  # Next.js configuration with reverse proxy rewrites
│   ├── package.json                    # Node dependencies and scripts
│   ├── tailwind.config.ts              # Tailwind CSS styling and theme configuration
│   └── tsconfig.json                   # TypeScript configuration
├── scripts/
│   └── ingest.py                       # Vector ingestion CLI utility
├── .vscode/                            # VS Code workspace settings, launch & task configs
│   ├── launch.json                     # F5 debug launcher for unified server
│   ├── settings.json                   # File associations and tab formatting
│   └── tasks.json                      # VS Code build and test tasks
├── dataset.csv                         # Original seed candidate dataset (632 destinations)
├── destinations_verified.csv           # Complete verified destination dataset with GPS (639 destinations)
├── docker-compose.yml                  # Docker deployment configuration
├── incredible-journeys.code-workspace  # One-click VS Code workspace file
├── open_in_vscode.bat                  # One-click launcher to open project in VS Code
├── package.json                        # Root npm script runner
├── README.md                           # Project documentation
├── requirements.txt                    # Root Python dependencies
├── run.bat                             # Windows single-click application launcher
├── run.py                              # Unified cross-platform single localhost launcher
└── setup.bat                           # Windows one-click dependency installer and launcher
```

---

## How to View and Edit in VS Code

You can view, browse, and edit all codes and datasets in plain human-readable format inside Visual Studio Code:

### Method 1: One-Click Script
Double-click `open_in_vscode.bat` in the project folder. This opens the entire project workspace directly in VS Code.

### Method 2: Open Workspace File
Double-click `incredible-journeys.code-workspace` to open the configured multi-folder workspace in VS Code.

### Method 3: Standard File Menu
1. Launch VS Code.
2. Click `File` -> `Open Folder...`.
3. Select the `incredible-journeys` folder.

Once opened in VS Code:
- All source files (`.py`, `.tsx`, `.ts`, `.json`, `.css`) open directly as human-readable code with syntax highlighting.
- All dataset files (`dataset.csv`, `destinations_verified.csv`, `foods.json`, `destinations.json`) open as plain text data tables.
- Press `F5` in VS Code to launch the application directly using the pre-configured `.vscode/launch.json` profile.

---

## Installation and Quick Start

### Prerequisites
- Python 3.10, 3.11, or 3.12
- Node.js 18 or higher (Node 20 or Node 22 recommended)
- npm or pnpm

---

### Option A: One-Click Launch (Windows)

1. Double-click `setup.bat` (or run it from terminal):
```cmd
setup.bat
```
This automatically installs Python backend dependencies, installs frontend npm packages, starts all services, and opens `http://localhost:3000` in your default browser.

2. On subsequent runs, you can simply run:
```cmd
run.bat
```

---

### Option B: Cross-Platform Single-Command Launch (Windows, macOS, Linux)

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the unified launcher:
```bash
python run.py
```
`run.py` automatically checks for frontend dependencies, starts the FastAPI backend silently on port 8000, starts the Next.js frontend on port 3000, verifies health connectivity, and opens `http://localhost:3000` in your web browser.

---

### Option C: Manual Step-by-Step Setup

#### Step 1: Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment (optional)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Start backend server
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

#### Step 2: Frontend Setup
```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start Next.js development server
npm run dev
```

Open `http://localhost:3000` in your browser.

---

## Configuration

Configuration values can be customized via `.env` files. Both root `.env.example` and `backend/.env.example` are provided.

```env
# Optional: Google Gemini API key for cloud model generation.
# If omitted, the system runs with the high-eloquence local polyglot storyteller.
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# Vector DB and Embeddings
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2
CHROMA_PERSIST_DIRECTORY=./backend/data/chroma_db
SIMILARITY_THRESHOLD=0.35

# Network Configuration
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Frontend Configuration
NEXT_PUBLIC_API_URL=
```

Note: Leaving `NEXT_PUBLIC_API_URL` empty allows the frontend to call its own origin (`http://localhost:3000`), routing through Next.js reverse proxies to the backend.

---

## Unified Endpoints on Localhost 3000

All endpoints are accessible directly through `http://localhost:3000`:

| Path | Purpose |
| :--- | :--- |
| `http://localhost:3000/` | Main portal with 3D Globe, 7 Wonders, Airplane, and Gastronomy |
| `http://localhost:3000/explore` | Filterable destination catalog (States, UNESCO, Food) |
| `http://localhost:3000/guide` | Polyglot AI tour guide with 16 languages, jokes, and storytelling |
| `http://localhost:3000/destinations/[slug]` | Deep-dive destination dossiers with Leaflet maps |
| `http://localhost:3000/about` | Transparency, 5-stage RAG diagram, and license disclosures |
| `http://localhost:3000/api/destinations` | Filterable destination JSON API |
| `http://localhost:3000/api/foods` | Authentic Indian regional dishes API |
| `http://localhost:3000/api/chat` | Polyglot chat endpoint |
| `http://localhost:3000/api/chat/stream` | Server-Sent Events (SSE) streaming chat endpoint |
| `http://localhost:3000/api/health` | System health, vector DB counts, and model status |
| `http://localhost:3000/docs` | Interactive Swagger API documentation |

---

## Running Automated Tests

### Backend Unit and Integration Tests
```bash
python -m pytest backend/tests
```
Verifies query normalization, ChromaDB retrieval, multi-turn conversational memory, fallback guardrails, and API routes.

### Frontend Smoke Tests
```bash
npm --prefix frontend test
```
Verifies route rendering, component contracts, and TypeScript types.

---

## Provenance and Grounding Policy

1. **Zero Hallucination Policy**: If coordinates cannot be verified from authoritative geographic datasets, fields remain null rather than synthesized.
2. **Authentic Imagery**: Photographs are sourced strictly from Wikimedia Commons under Creative Commons licensing, prioritizing architectural and landscape views without human portraits.
3. **Open Access Data**: Destination data and narratives derive from open-access datasets under the Creative Commons Attribution-ShareAlike 4.0 International license (CC BY-SA 4.0).
4. **Interactive Maps**: Powered by OpenStreetMap contributors under the Open Database License (ODbL).

---

## Licensing and Provenance

- Software Code: Released under the MIT License.
- Content and Curated Datasets: Licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).
- Map Data: Copyright OpenStreetMap contributors, licensed under the Open Database License (ODbL).
