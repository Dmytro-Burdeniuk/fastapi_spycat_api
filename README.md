# 

# Welcome to Spy Cat Agency API 

Spy Cat Agency API is a mission-management backend built with FastAPI, enabling the organization to manage spy cats, assign espionage missions, and monitor target intelligence notes.
The application integrates with TheCatAPI to ensure only real, recognized cat breeds graduate into the elite spy program.

Cats complete missions by tracking targets and logging field notes. Once all targets are completed, missions automatically lock and become immutable.

# Features

- Cat Management

    - - Add, view, delete spy cats

    - - Validate cat breed via TheCatAPI

    - - Update salary only (as specified)

- Mission Control

    - - Create missions with 1–3 targets in a single request

    - - Assign cats only if they have no active missions

    - - List missions with nested cats and targets

    - - Block mission deletion if linked to a cat

- Target Operations

    - - Targets exist only within missions (no standalone endpoints)

    - - Update notes while spying

    - - Notes freeze once a target is complete

    - - Mission auto-completes when all targets complete

    - - No edits allowed after mission completion

- Business Rules Enforced

    - - One active mission per cat

    - - 1–3 targets per mission

    - - Immutable state once completed

## Technologies Used

- FastAPI for building the REST API

- PostgreSQL for storing cats, missions, and targets

- SQLAlchemy 2.0 for typed ORM interactions

- TheCatAPI for breed lookup and validation

- pydantic-settings for structured configuration management

- Swagger UI for API documentation and testing

## Requirements

- Python 3.11

- Docker & Docker Compose

- Virtual environment tool (venv/pyenv/etc.)

## Installation
1. Clone the repository:
```bash
 git https://github.com/Dmytro-Burdeniuk/fastapi_spycat_api.git
```

2. Setup virtual environment
```bash
python -m venv .venv

# Linux/Mac
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create .env file in your root directory and fill it with necessary environment variables.
```bash
DATABASE_URL=

POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

CAT_API_BASE_URL=
CAT_API_KEY=
```

## Usage 

1. Start Docker Compose for Postgres 
```bash
docker-compose up -d
```

2. Start application 
```bash
uvicorn src.main:app --reload
```

## Postman Collection

[Spy Cat Agency API – Postman Collection](https://dimaburdeniuk.postman.co/workspace/Dima-Burdeniuk's-Workspace~3b7d2e43-3f86-43dc-8a14-d0f67e48d873/collection/43493558-1559b1f1-ef5c-443b-8d00-fab8a9e7a6c7?action=share&creator=43493558)