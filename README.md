# RAG Application — FastAPI + Streamlit + ChromaDB
<img width="1919" height="912" alt="image" src="https://github.com/user-attachments/assets/e7404b06-099b-4c93-966d-d30cbbae06d3" />

A fully functional Retrieval-Augmented Generation (RAG) system built using:

* **FastAPI** — Backend API
* **Streamlit** — Frontend UI
* **ChromaDB** — Vector database
* **SQLite** — Application logs + document store
* **Python** — End-to-end implementation

This project allows users to upload documents, automatically index them, and query an LLM with accurate, context-aware responses.

---

## Features

### Retrieval-Augmented Generation (RAG)

* Uses **ChromaDB** for vector storage
* Automatic **text chunking + embeddings**
* Enhanced responses grounded in uploaded documents

### File Upload & Document Indexing

* Supports **PDF / TXT** uploads
* Stores metadata inside SQLite (`document_store`)
* Chunks → embeds → stores vectors in Chroma

### Chat Interface

* Streamlit chat UI
* Maintains session chat history
* Displays LLM response + source context

---

## Backend (FastAPI)

| Endpoint              | Description                  |
| --------------------- | ---------------------------- |
| `POST /upload`        | Upload & index a document    |
| `POST /query`         | Query the RAG system         |
| `GET /documents`      | List uploaded documents      |
| `DELETE /delete/{id}` | Delete document & embeddings |

---

## Logging System

Stored in SQLite table: `application_logs`

* user queries
* model responses
* timestamps
* session IDs

---

## Project Structure
```
rag_app/
│
├── api/
│   ├── main.py               # FastAPI server
│   ├── db_utils.py           # SQLite operations
│   ├── rag_utils.py          # Chunking, embedding, retrieval
│   ├── chroma_db/            # ChromaDB persisted data
│
├── streamlit_app/
│   ├── app.py                # Streamlit UI
│
├── requirements.txt
├── README.md
└── rag_app.db                # SQLite database (auto-created)
```
---

## Technologies Used

| Component   | Technology                             |
| ----------- | -------------------------------------- |
| Backend API | FastAPI                                |
| Frontend    | Streamlit                              |
| Vector DB   | ChromaDB                               |
| Embeddings  | SentenceTransformers / Gemini / OpenAI |
| LLM         | Gemini 2.5 Flash                       |
| Database    | SQLite                                 |

---

## System Architecture

```
               Streamlit UI (Chat + File Upload)
                          |
                        HTTP
                          |
                        FastAPI
                /upload /query /delete
                          |
       ┌───────────────┬───────────────┬────────────────┐
       |               |                |                |
   ChromaDB       SQLite Logs     Document Store     Others
```

---

## Installation

### 1. Clone the Repository

git clone <your-repo-url>
cd rag_app


### 2. Create a Virtual Environment


python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\\Scripts\\activate    # Windows


### 3. Install Dependencies


pip install -r requirements.txt


## Environment Variables

Create a `.env` file:

GEMINI_API_KEY=your_key_here
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
CHROMA_DB_PATH=./api/chroma_db




## Running the Project

### FastAPI Backend


uvicorn api.main:app --reload --port 8000

### Streamlit Frontend

streamlit run streamlit_app/app.py


## Upload Documents

### Using Streamlit UI

Upload directly via the interface.

### Using cURL

curl -X POST "http://localhost:8000/upload" \
     -F "file=@sample.pdf"

---

## Query the RAG Model

curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is inside the document?"}'


---

## Delete a Document

curl -X DELETE "http://localhost:8000/delete/3"


---

## Debugging Tips

If you get this error:


sqlite3.OperationalError: no such table: document_store


Run this in Python shell:

from api.db_utils import create_document_store, create_application_logs
create_document_store()
create_application_logs()


---

## Contributing

Pull requests are welcome. For major changes, open an issue first to discuss.

Pull requests are welcome.
For major changes, open an issue first to discuss.


