# Agentic RAG

A FastAPI-based agentic retrieval-augmented generation (RAG) application that lets users register, log in, upload PDF documents, and ask questions based on the uploaded content. The app stores user documents in a MySQL database and indexes their content in a Chroma vector database for semantic retrieval.

## Features

- User authentication with JWT-based login
- Secure password hashing using Argon2
- PDF upload and storage per user
- Document chunking and vector embedding for semantic search
- Chat sessions tied to individual users
- RAG chat agent powered by Groq + LangChain
- Chroma vector database persistence for stored embeddings

## Tech Stack

- Python 3.14+
- FastAPI
- SQLAlchemy
- MySQL
- LangChain
- LangGraph
- Chroma
- Groq LLM
- PyMuPDF / PyPDF
- Sentence Transformers
- Pydantic + Email validation

## Project Structure

```text
agentic_rag/
├── main.py
├── pyproject.toml
├── README.md
├── auth/
│   ├── config.py
│   ├── controller.py
│   ├── db.py
│   ├── models.py
│   ├── router.py
│   ├── schemas.py
│   └── security.py
├── rag/
│   ├── config.py
│   ├── controller.py
│   ├── llm.py
│   ├── models.py
│   ├── prompt.py
│   ├── router.py
│   ├── schemas.py
│   ├── vectordb.py
│   ├── Ingesting/
│   │   ├── embedding.py
│   │   ├── loader.py
│   │   ├── splitter.py
│   │   └── upload_pdf.py
│   ├── query/
│   │   ├── create_chat.py
│   │   ├── retrive_chat_history.py
│   │   └── save_message.py
│   └── tools/
│       └── tools.py
├── storage/
│   └── uploads/
├── chroma_db/
└── .env
```

## Prerequisites

Before running the project, make sure you have:

- Python 3.14 or newer
- MySQL server running
- A Groq API key
- A package manager such as uv or pip

## Installation

1. Clone the repository:

```bash
git clone <your-repo-url>
cd agentic_rag
```

2. Create and activate a virtual environment:

Using uv:

```bash
uv venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows PowerShell
```

Or using standard Python:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows PowerShell
```

3. Install dependencies:

```bash
uv sync
```

If you are not using uv, install requirements with:

```bash
pip install -r requirements.txt
```

> This project uses a pyproject.toml-based installation and depends on FastAPI, LangChain, SQLAlchemy, Chroma, and the Groq SDK stack.

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=agentic_rag
DB_USER=root
DB_PASSWORD=your_mysql_password
GROQ_API_KEY=your_groq_api_key
```

### Notes

- The application reads database settings from `auth/config.py`.
- The Groq key is required by `rag/llm.py` for the chat agent.
- The app creates the database and tables automatically at startup using SQLAlchemy metadata.

## Running the Project

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The app will be available at:

```text
http://localhost:8000
```

## API Overview

### Authentication

#### Register user

```http
POST /auth/register
```

Request body:

```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "secret123"
}
```

#### Login user

```http
POST /auth/login
```

Request body:

```json
{
  "username": "john",
  "password": "secret123"
}
```

Response includes JWT tokens.

#### Get current user

```http
GET /auth/get_user
```

Requires Bearer token authentication.

### RAG Endpoints

#### Upload PDFs

```http
POST /api/ingest
```

- Accepts one or more PDF files
- Stores uploaded files in `storage/uploads/`
- Splits and embeds the document content into Chroma

#### Create a new chat

```http
POST /api/chat
```

Query parameter:

```text
title=<chat title>
```

#### Send a message

```http
POST /api/chat/{chat_id}
```

Request body:

```json
{
  "message": "Summarize the uploaded documents."
}
```

#### Get chat history

```http
GET /api/chat/{chat_id}
```

#### Get all chats

```http
GET /api/chats
```

#### Delete chat

```http
DELETE /api/chat/{chat_id}
```

#### Get all documents

```http
GET /api/documents
```

#### View document

```http
GET /api/documents/{document_id}
```

#### Delete document

```http
DELETE /api/documents/{document_id}
```

## Example Usage

### Register

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "secret123"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "password": "secret123"
  }'
```

### Upload PDF

```bash
curl -X POST "http://localhost:8000/api/ingest" \
  -H "Authorization: Bearer <your_token>" \
  -F "files=@sample.pdf"
```

### Chat with uploaded documents

```bash
curl -X POST "http://localhost:8000/api/chat/1" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What does this document say about the main topic?"
  }'
```

## How It Works

1. A user registers and logs in.
2. The user uploads one or more PDFs.
3. The app stores the original file in `storage/uploads/` and saves metadata to MySQL.
4. PDFs are extracted, split into chunks, and embedded into Chroma.
5. When the user sends a chat message, the app retrieves relevant chunks from the user-specific vector store.
6. The LLM answers using those document chunks as context.

## Screenshots

Add project screenshots here to showcase the user flow and interface.

### Login / Authentication

```text
![Login screen](docs/screenshots/login.png)
```

### Document Upload

```text
![PDF upload page](docs/screenshots/upload.png)
```

### Chat with Retrieved Context

```text
![Chat interface](docs/screenshots/chat.png)
```

> Replace the placeholder image paths with your actual screenshots once they are added to the project.

## Important Notes

- The project uses `Chroma` with the local persistent directory `./chroma_db`.
- Uploaded document metadata is tied to the authenticated user.
- All chat and document access are scoped to the current user.
- The default security secret is defined in `auth/config.py` and should be replaced with a stronger secret in production.

## License

This project currently does not include a formal license file. Add one if you plan to distribute or publish it.
