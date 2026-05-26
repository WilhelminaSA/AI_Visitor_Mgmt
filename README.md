# AI Visitor Management System

A Python-based AI-powered visitor management system that uses **face recognition** and **CLIP embeddings** to register, identify, and monitor visitors in real time using a webcam.

---

## Features

- Register visitors with face embeddings and CLIP image embeddings
- Real-time webcam monitoring with automatic face detection
- Identify known vs unknown persons using cosine similarity
- Search visitors by ID or name
- Delete visitor records
- Structured image storage with auto-incremented naming
- PostgreSQL backend with pgvector for vector similarity search

## Project Structure

```
AI_Visitor_Mgmt/
├── app/
│   ├── main.py                  # Main entry point (full featured menu)
│   └── menu.py                  # Lightweight menu (Version 1)
├── config/
│   └── settings.py              # DB config, thresholds, intervals
├── database/
│   ├── db_connection.py         # PostgreSQL connection handler
│   └── person_repository.py     # CRUD operations (insert, search, delete)
├── services/
│   ├── embedding_service.py     # InsightFace + CLIP embedding generation
│   ├── face_matching_service.py # Cosine similarity face matching
│   └── monitoring_service.py    # Webcam capture and monitoring loop
├── utils/
│   └── image_storage.py         # Image saving with naming convention
├── schema/
│   └── schema.sql               # PostgreSQL schema with pgvector
└── requirements/
    └── requirements.txt
```

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.11 |
| Face Detection & Embedding | InsightFace (buffalo_l) |
| Image Embedding | CLIP (clip-ViT-B-32) |
| Database | PostgreSQL + pgvector |
| Computer Vision | OpenCV |
| DB Driver | psycopg2 |

---

## How It Works

### Registration
1. User provides name, age, gender, type, and image path
2. InsightFace detects exactly one face and extracts a 512-dim embedding
3. CLIP generates a 512-dim image embedding
4. Both embeddings and person details are stored in PostgreSQL

### Monitoring
1. Webcam captures an image every 30 seconds (configurable)
2. InsightFace detects all faces in the captured frame
3. Each face embedding is compared against all registered persons using cosine similarity
4. Persons above the similarity threshold are identified as known
5. Unknown faces are flagged with their nearest match suggestion

---

## Database Schema

| Table | Description |
|---|---|
| `persons` | Stores visitor details (name, age, gender, type) |
| `person_reference_images` | Stores image path + face/CLIP embeddings (vector 512) |
| `detection_events` | Logs each monitoring detection event |
| `monitoring_control` | Controls monitoring state and interval |

Vector indexes use HNSW with cosine similarity via pgvector.

---

## Prerequisites

- Python 3.11
- PostgreSQL with [pgvector](https://github.com/pgvector/pgvector) extension enabled
- InsightFace model: `buffalo_l`
- CLIP model: `clip-ViT-B-32`

---

## Setup Instructions

**1. Clone the repository**
```bash
git clone https://github.com/WilhelminaSA/AI_Visitor_Mgmt.git
cd AI_Visitor_Mgmt
```

**2. Install dependencies**
```bash
pip install -r requirements/requirements.txt
```

**3. Set up the database**
```bash
psql -U postgres -d ai_visitor_db -f schema/schema.sql
```

**4. Configure settings**

Open `config/settings.py` and update your database credentials:
```python
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "ai_visitor_db"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
```

> ⚠️ Never commit real credentials to GitHub. Use environment variables in production.

**5. Run the application**
```bash
python app/main.py
```

---

## Menu Options

Register Person
Delete Person
Search Person by ID
Search by Name
List All Persons
Start Monitoring
Stop Monitoring
Exit


---

## Configuration

| Setting | Default | Description |
|---|---|---|
| `MONITORING_INTERVAL` | 30 sec | How often webcam captures an image |
| `MATCH_THRESHOLD` | 0.58 | Minimum cosine similarity to identify a person |
| `SIMILARITY_THRESHOLD` | 0.65 | Threshold used inside monitoring service |

---

## Image Storage Format

Registered images are saved in the format:
img_001_full_name.jpg
img_002_another_name.jpg

---

## Versions

| Branch | Description |
|---|---|
| `main` | Version 1 — core registration and monitoring |
| `version-2` | Version 2 — extended features |

---

## Author

Developed by **Sneha** — B.Tech Computer Science Engineering