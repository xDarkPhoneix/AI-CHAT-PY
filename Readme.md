# 📄 PDF Chat AI – Production-Ready RAG Application

An end-to-end AI-powered PDF Chat application built with **FastAPI**, **MongoDB Atlas Vector Search**, **Google Gemini**, **LangChain**, **Celery**, and **Redis**.

Upload PDF documents, automatically process and embed their contents in the background, and ask natural language questions to retrieve accurate answers from the uploaded documents.

---

# ✨ Features

- 🔐 JWT Authentication
- 📄 PDF Upload
- ⚡ Background PDF Processing using Celery
- ✂️ Intelligent Text Chunking with LangChain
- 🧠 Google Gemini Embeddings
- 🔍 MongoDB Atlas Vector Search
- 🤖 Gemini 2.5 Flash for Question Answering
- 🚀 Redis Response Caching
- 🛡️ Redis-based Rate Limiting
- 📊 Redis Insight Support
- 🐳 Dockerized Development Environment
- ☁️ MongoDB Atlas Integration
- ⚙️ Production-Oriented Project Structure

---

# 🏗️ Architecture

```text
                   User
                     │
                     ▼
              FastAPI Backend
                     │
     ┌───────────────┴────────────────┐
     │                                │
     ▼                                ▼
JWT Authentication              Rate Limiter
     │                                │
     └───────────────┬────────────────┘
                     ▼
               Upload PDF
                     │
                     ▼
           Store Metadata (MongoDB)
                     │
                     ▼
              Celery Background Worker
                     │
                     ▼
              Extract PDF Text
                     │
                     ▼
          Recursive Text Chunking
                     │
                     ▼
       Gemini Embedding Generation
                     │
                     ▼
     MongoDB Atlas Vector Search
                     │
────────────────────────────────────────────

                User Question
                     │
                     ▼
        Generate Query Embedding
                     │
                     ▼
        MongoDB Atlas Vector Search
                     │
                     ▼
        Retrieve Relevant Chunks
                     │
                     ▼
            Gemini 2.5 Flash
                     │
                     ▼
               Final Response
```

---

# 🛠️ Tech Stack

### Backend

- FastAPI
- Python 3.12
- Beanie ODM
- Motor
- Pydantic v2

### AI

- Google Gemini 2.5 Flash
- Gemini Embedding Model
- LangChain
- PyMuPDF

### Database

- MongoDB Atlas
- MongoDB Atlas Vector Search

### Background Jobs

- Celery

### Cache & Messaging

- Redis
- Redis Insight

### Authentication

- JWT
- Passlib (bcrypt)

### DevOps

- Docker
- Docker Compose

---

# 📂 Project Structure

```text
backend/

app/
├── api/
├── auth/
├── core/
├── database/
├── middleware/
├── models/
├── repositories/
├── schemas/
├── services/
├── utils/
├── workers/
└── main.py

uploads/

Dockerfile
docker-compose.yml
requirements.txt
```

---

# ⚙️ How It Works

## 1. Upload PDF

Users upload a PDF document through the API.

The backend:

- validates the file
- stores metadata in MongoDB
- queues a Celery task

---

## 2. Background Processing

Celery worker:

- extracts text using PyMuPDF
- chunks the text using LangChain
- generates embeddings using Gemini
- stores embeddings in MongoDB Atlas

---

## 3. Chat

When a user asks a question:

1. Generate embedding for the question.
2. Perform MongoDB Atlas Vector Search.
3. Retrieve the most relevant chunks.
4. Build a context prompt.
5. Send the prompt to Gemini 2.5 Flash.
6. Return the generated answer.

---

# 🚀 API Endpoints

## Authentication

| Method | Endpoint         | Description           |
| ------ | ---------------- | --------------------- |
| POST   | `/auth/register` | Register a user       |
| POST   | `/auth/login`    | Login and receive JWT |

---

## Documents

| Method | Endpoint            | Description          |
| ------ | ------------------- | -------------------- |
| POST   | `/documents/upload` | Upload a PDF         |
| GET    | `/documents`        | List user documents  |
| GET    | `/documents/{id}`   | Get document details |

---

## Chat

| Method | Endpoint | Description                         |
| ------ | -------- | ----------------------------------- |
| POST   | `/chat`  | Ask questions about an uploaded PDF |

---

# ⚡ Background Processing

Celery is responsible for:

- PDF extraction
- Chunk generation
- Embedding generation
- Storing vector embeddings

This keeps upload requests fast and responsive.

---

# 🚦 Rate Limiting

Redis-backed rate limiting protects the API.

Example limits:

- Login: **10 requests/minute**
- Chat: **30 requests/minute**
- Upload: **5 PDFs/hour**

---

# ⚡ Redis Caching

Repeated questions for the same document are cached.

Benefits:

- Faster responses
- Reduced Gemini API calls
- Lower operational costs

---

# 🔍 Vector Search

Embeddings are stored in MongoDB Atlas.

Each user query:

1. Generates an embedding.
2. Performs Atlas Vector Search.
3. Retrieves the most relevant chunks.
4. Uses those chunks as context for Gemini.

---

# 🐳 Running with Docker

## Prerequisites

Before starting, ensure you have:

- Docker
- Docker Compose
- A MongoDB Atlas cluster
- A Google Gemini API Key

---

## Configure Environment Variables

Create a `.env` file inside the `backend` directory and add your configuration.

Example:

```env
MONGODB_URL=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority

DATABASE_NAME=pdf_chat_ai

REDIS_URL=redis://redis:6379

JWT_SECRET_KEY=your-secret-key

ACCESS_TOKEN_EXPIRE_MINUTES=60

GEMINI_API_KEY=your-gemini-api-key
```

---

## Build Docker Images

From the project backend, run:

```bash
docker compose build
```

---

## Start All Services

```bash
docker compose up
```

Run in detached mode:

```bash
docker compose up -d
```

---

## Verify Running Containers

```bash
docker ps
```

You should see containers similar to:

- `pdf-chat-api`
- `pdf-chat-worker`
- `pdf-chat-redis`
- `pdf-chat-redis-insight`

---

## View Logs

View logs for all services:

```bash
docker compose logs -f
```

View logs for the API only:

```bash
docker compose logs -f api
```

View logs for the Celery worker:

```bash
docker compose logs -f celery
```

---

## Stop the Application

```bash
docker compose down
```

Stop and remove volumes:

```bash
docker compose down -v
```

---

## Access the Services

| Service       | URL                         |
| ------------- | --------------------------- |
| FastAPI       | http://localhost:8000       |
| Swagger UI    | http://localhost:8000/docs  |
| ReDoc         | http://localhost:8000/redoc |
| Redis Insight | http://localhost:5540       |

---

## Docker Architecture

```text
                    Docker Compose

        ┌────────────────────────────┐
        │        FastAPI API         │
        └─────────────┬──────────────┘
                      │
                      ▼
        ┌────────────────────────────┐
        │       Celery Worker        │
        └─────────────┬──────────────┘
                      │
                      ▼
        ┌────────────────────────────┐
        │          Redis             │
        └─────────────┬──────────────┘
                      │
                      ▼
        ┌────────────────────────────┐
        │      Redis Insight         │
        └────────────────────────────┘

                 │
                 ▼

          MongoDB Atlas (Cloud)

                 │
                 ▼

          Google Gemini API
```

**Note:** MongoDB is hosted on **MongoDB Atlas** and is **not** part of the Docker Compose setup. Docker only runs the FastAPI application, Celery worker, Redis, and Redis Insight.

# 🐳 Running Locally

Clone the repository:

```bash
git clone https://github.com/xDarkPhoneix/AI-CHAT-PY.git
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

**Linux/macOS**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure environment variables by creating a `.env` file.

Start Redis and Redis Insight:

```bash
docker compose up -d
```

Run the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Start the Celery worker:

```bash
celery -A app.workers.celery_app:celery_app worker --loglevel=info
```

Open:

- API Docs: `http://localhost:8000/docs`
- Redis Insight: `http://localhost:5540`

# 💻 Running the Frontend

Navigate to the frontend directory:

```bash
cd client
```

Install the dependencies:

```bash
npm install
```

Start the Next.js development server:

```bash
npm run dev
```

The frontend will be available at:

- **Frontend:** http://localhost:3000

Make sure the FastApi Backend/ Celery Worker or Docker Container backend is running before starting the frontend. By default, the frontend communicates with the backend API running at:

- **Backend API:** http://localhost:8000

---

# 📈 Future Improvements

- Streaming AI responses
- Conversation history
- Source citations with page numbers
- Hybrid search (keyword + vector)
- OCR support for scanned PDFs
- Cloud storage integration (Cloudinary/S3)
- CI/CD with GitHub Actions
- Kubernetes deployment
- Monitoring with Prometheus & Grafana

---

# 🎯 Learning Outcomes

This project demonstrates experience with:

- Retrieval-Augmented Generation (RAG)
- FastAPI architecture
- Background task processing
- Vector databases
- Semantic search
- JWT authentication
- Redis caching
- Rate limiting
- Docker
- Production-ready backend design

---

# 📄 License

This project is released under the MIT License.

---

## ⭐ If you found this project helpful, consider giving it a star on GitHub!
