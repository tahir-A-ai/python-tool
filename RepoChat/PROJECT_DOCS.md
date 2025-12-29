# RepoChat — Secure Codebase Intelligence System

## 1. Overview
RepoChat is a hybrid microservices application that allows users to "chat" with their codebase securely using AI. It leverages RAG (Retrieval-Augmented Generation) to process code locally, ensuring privacy and security. Users can upload ZIP files containing their code repositories, and the system indexes them for intelligent question-answering.

**Key Features:**
- Upload code repositories as ZIP files
- Automatic code indexing and embedding
- AI-powered chat interface for codebase queries
- Local processing for enhanced security
- Multi-repository support with isolated contexts
- User authentication and authorization

---

## 2. Architecture

### 2.1 System Components
The application follows a **microservices architecture** with two main services:

1. **Web Portal (Django)** - Port 8000
   - User interface and authentication
   - Repository management
   - Request routing and orchestration
   - File upload handling

2. **AI Engine (FastAPI)** - Port 8001
   - Code processing and chunking
   - Vector embeddings generation
   - Semantic search
   - LLM integration for chat responses

### 2.2 Communication Flow
```
User → Django (Web Portal) → FastAPI (AI Engine) → Vector DB (FAISS)
                ↓                      ↓
           SQLite3 DB          Gemini 2.5 Flash API
```

### 2.3 Data Flow
1. **Upload Phase:**
   - User uploads ZIP file via Django
   - Django saves file and creates Repository record
   - Django signal triggers FastAPI ingestion endpoint
   - FastAPI processes ZIP in background task

2. **Indexing Phase:**
   - Extract files from ZIP
   - Filter supported file types
   - Chunk code into manageable pieces
   - Generate embeddings using Sentence Transformers
   - Store in FAISS vector database

3. **Query Phase:**
   - User sends question via chat interface
   - Django forwards query to FastAPI
   - FastAPI retrieves relevant code chunks from FAISS
   - Gemini generates contextual response
   - Response displayed in chat UI

---

## 3. Tech Stack

### 3.1 Backend Frameworks
- **Django 6.0** - Web framework for portal
- **FastAPI** - High-performance API for AI services
- **Uvicorn** - ASGI server for FastAPI

### 3.2 AI & Machine Learning
- **Google Gemini 2.5 Flash** - Large Language Model for chat responses
- **Sentence Transformers** - Local embedding model (`all-MiniLM-L6-v2`)
- **FAISS (CPU)** - Facebook AI Similarity Search for vector storage
- **NumPy** - Numerical operations for embeddings

### 3.3 Database
- **SQLite3** - Relational database for user data and repository metadata
- **FAISS Index** - Vector database for code embeddings
- **Pickle** - Metadata storage alongside FAISS index

### 3.4 Utilities
- **Requests** - HTTP communication between services
- **Python-dotenv** - Environment variable management
- **TikToken** - Token counting (optional)
- **PyPDF** - PDF processing (optional)

---

## 4. Project Structure

```
RepoChat/
├── web_portal/                 # Django Application
│   ├── config/                 # Django project settings
│   │   ├── settings.py         # Configuration
│   │   ├── urls.py             # URL routing
│   │   └── wsgi.py             # WSGI entry point
│   ├── core/                   # Main Django app
│   │   ├── models.py           # Repository model
│   │   ├── views.py            # View controllers
│   │   ├── signals.py          # Post-save signal handlers
│   │   ├── admin.py            # Admin interface
│   │   └── migrations/         # Database migrations
│   ├── templates/              # HTML templates
│   │   ├── base.html           # Base template
│   │   ├── dashboard.html      # Repository list
│   │   ├── chat.html           # Chat interface
│   │   ├── upload.html         # Upload form
│   │   ├── login.html          # Login page
│   │   ├── register.html       # Registration page
│   │   └── confirm_delete.html # Delete confirmation
│   ├── forms.py                # Django forms
│   ├── manage.py               # Django CLI
│   ├── db.sqlite3              # SQLite database
│   └── media/                  # Uploaded files
│       └── repos/              # Repository ZIP files
│
├── ai_engine/                  # FastAPI Application
│   ├── app/
│   │   ├── main.py             # FastAPI app initialization
│   │   ├── api/
│   │   │   └── routes.py       # API endpoints
│   │   ├── services/
│   │   │   ├── file_processing.py    # ZIP extraction & chunking
│   │   │   ├── vector_store.py       # FAISS operations
│   │   │   └── gemini_service.py     # LLM integration
│   │   └── schemas/
│   │       └── payload.py      # Pydantic models
│   ├── faiss_index.bin         # FAISS vector index
│   └── metadata.pkl            # Document metadata
│
├── requirements.txt            # Python dependencies
└── PROJECT_DOCS.md            # This file
```

---

## 5. Database Schema

### 5.1 Django Models (SQLite3)

#### Repository Model
```python
class Repository(models.Model):
    id: int (Primary Key)
    name: str (max_length=255)
    description: str (TextField, optional)
    repo_files: FileField (upload_to='repos/')
    status: str (choices: pending, processing, indexed, failed)
    uploaded_at: datetime (auto_now_add=True)
```

**Status Flow:**
- `pending` → Initial state after upload
- `processing` → During ingestion (optional)
- `indexed` → Ready for queries
- `failed` → Error during processing

### 5.2 Vector Database (FAISS)

**Index Type:** `IndexFlatL2` (L2 distance metric)
**Embedding Dimension:** 384 (from all-MiniLM-L6-v2 model)

**Metadata Structure:**
```python
{
    "text": str,              # Code chunk content
    "metadata": {
        "source": str,        # Relative file path
        "extension": str,     # File extension
        "repo_id": int        # Repository identifier
    }
}
```

---

## 6. API Endpoints

### 6.1 Django (Web Portal) - Port 8000

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Dashboard - List repositories | Yes |
| GET/POST | `/login/` | User login | No |
| GET/POST | `/register/` | User registration | No |
| GET | `/logout/` | User logout | Yes |
| GET/POST | `/upload/` | Upload repository ZIP | Yes |
| GET/POST | `/repository/<id>/chat/` | Chat interface | Yes |
| POST | `/repository/<id>/delete/` | Delete repository | Yes |
| GET | `/admin/` | Django admin panel | Admin |

### 6.2 FastAPI (AI Engine) - Port 8001

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| GET | `/` | Health check | - |
| POST | `/ingest` | Queue repository for indexing | `{repo_id: int, file_path: str}` |
| POST | `/search` | Search code chunks | `{query: str, repo_id: int, limit: int}` |
| POST | `/chat` | Get AI response | `{repo_id: int, query: str}` |

---

## 7. Core Services

### 7.1 File Processing Service
**Location:** `ai_engine/app/services/file_processing.py`

**Responsibilities:**
- Extract ZIP files to temporary directory
- Filter files by supported extensions
- Read file contents with error handling
- Chunk text into overlapping segments

**Supported File Types:**
`.py`, `.js`, `.ts`, `.html`, `.css`, `.md`, `.txt`, `.json`, `.java`, `.cpp`

**Chunking Strategy:**
- **Chunk Size:** 1000 characters
- **Overlap:** 100 characters
- **Purpose:** Maintain context across chunk boundaries

### 7.2 Vector Store Service
**Location:** `ai_engine/app/services/vector_store.py`

**Responsibilities:**
- Initialize FAISS index
- Generate embeddings using Sentence Transformers
- Add documents to vector database
- Perform semantic similarity search
- Persist index and metadata to disk

**Key Features:**
- Automatic index persistence
- Metadata filtering by `repo_id`
- Top-K retrieval with distance scoring

### 7.3 Gemini Service
**Location:** `ai_engine/app/services/gemini_service.py`

**Responsibilities:**
- Configure Google Gemini API
- Construct prompts with code context
- Generate AI responses
- Handle API errors gracefully

**Prompt Engineering:**
- System role: "Expert Senior Software Engineer"
- Context-aware responses
- Fallback for missing information

---

## 8. Key Workflows

### 8.1 Repository Upload & Indexing

```
1. User uploads ZIP via Django form
2. Django saves file to media/repos/
3. Django creates Repository record (status: pending)
4. post_save signal triggers in signals.py
5. Signal sends POST to FastAPI /ingest endpoint
6. FastAPI validates file path
7. FastAPI queues background task
8. FastAPI returns "accepted" immediately
9. Background worker:
   a. Extracts ZIP to temp directory
   b. Reads supported files
   c. Chunks text (1000 chars, 100 overlap)
   d. Generates embeddings (384-dim vectors)
   e. Stores in FAISS with metadata
   f. Saves index to disk
   g. Cleans up temp directory
10. Repository ready for queries
```

### 8.2 Chat Query Processing

```
1. User types question in chat interface
2. JavaScript sends POST to Django chat view
3. Django forwards to FastAPI /chat endpoint
4. FastAPI:
   a. Embeds user query
   b. Searches FAISS for top 3 relevant chunks
   c. Filters by repo_id
   d. Combines chunks into context
   e. Sends to Gemini with prompt
   f. Returns AI response
5. Django returns JSON to frontend
6. JavaScript displays response in chat
```

---

## 9. Configuration

### 9.1 Environment Variables

Create a `.env` file in the `ai_engine/` directory:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### 9.2 Django Settings
**Location:** `web_portal/config/settings.py`

**Key Configurations:**
- `DEBUG = True` (Development only)
- `MEDIA_ROOT` - File upload directory
- `LOGIN_URL = 'login'`
- `LOGIN_REDIRECT_URL = 'dashboard'`

### 9.3 Service URLs
- **Django:** `http://127.0.0.1:8000`
- **FastAPI:** `http://127.0.0.1:8001`
- **AI Engine URL in signals.py:** `http://127.0.0.1:8001/ingest`

---

## 10. Installation & Setup

### 10.1 Prerequisites
- Python 3.8+
- pip package manager
- Google Gemini API key

### 10.2 Installation Steps

```bash
# 1. Clone the repository
cd RepoChat

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cd ai_engine
echo "GEMINI_API_KEY=your_key_here" > .env

# 4. Run Django migrations
cd ../web_portal
python manage.py migrate

# 5. Create superuser (optional)
python manage.py createsuperuser

# 6. Start FastAPI (Terminal 1)
cd ../ai_engine
uvicorn app.main:app --reload --port 8001

# 7. Start Django (Terminal 2)
cd ../web_portal
python manage.py runserver 8000
```

### 10.3 Access the Application
- **Web Portal:** http://127.0.0.1:8000
- **API Docs:** http://127.0.0.1:8001/docs
- **Admin Panel:** http://127.0.0.1:8000/admin

---

## 11. Security Considerations

### 11.1 Current Implementation
- User authentication via Django's built-in system
- CSRF protection on forms
- File upload validation
- HTML escaping in chat interface
- Local code processing (no external code sharing)

---

## 12. Credits & License

**Project:** RepoChat - Secure Codebase Intelligence System
**Architecture:** Hybrid Microservices (Django + FastAPI)
**AI Models:**
- Google Gemini 2.5 Flash (LLM)
- Sentence Transformers all-MiniLM-L6-v2 (Embeddings)

**Key Technologies:**
- Django, FastAPI, FAISS, Sentence Transformers, Google Generative AI

---

**Last Updated:** December 2025