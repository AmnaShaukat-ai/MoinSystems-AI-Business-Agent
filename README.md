# MoinSystems AI Business Agent

An advanced Agentic AI system designed for **MoinSystems** to handle customer inquiries, retrieve service knowledge via Retrieval-Augmented Generation (RAG), and capture leads autonomously. This project was built as part of the Round 8 (Agentic AI) internship requirement.

---

## Key Features

- **True Agentic Behavior:** Autonomously classifies user intent and decides whether to query a knowledge base (RAG), provide service details, or capture a lead using **Function Calling**.
- **State & Memory Management:** Retains conversation history using `session_id`, enabling seamless multi-turn conversations without context loss.
- **Human-in-the-Loop (Guardrail):** Enforces user verification before taking action; the agent confirms lead details with the user prior to triggering backend lead storage.
- **Robust Failure Handling:** Employs comprehensive `try-except` blocks to handle API timeouts and connection errors gracefully without crashing the application.
- **n8n & API Integration:** Upon user confirmation, triggers an n8n webhook to persist lead data into a CSV file and dispatch automated email notifications via the Resend API.

---

## Tech Stack

- **Backend Framework:** Python, FastAPI
- **AI & LLM Integration:** OpenAI API (`gpt-4.1-mini`), Pydantic (for structured output and data validation)
- **Automation & Orchestration:** n8n, Docker
- **Email Service:** Resend API

---

## 📁 Project Structure

```text
├── agent/
│   ├── controller.py     # Core logic for routing AI actions to tools
│   └── prompt.py         # System prompts and behavioral rules
├── tools/
│   ├── lead_tool.py      # Tool to capture leads and post to n8n
│   ├── rag_tool.py       # Tool for knowledge retrieval
│   └── service_tool.py   # Tool for fetching service details
├── n8n_files/            # Folder mapped to Docker for CSV exports
├── data/                 # Knowledge base JSON files
├── main.py               # FastAPI application entry point
└── config.py             # Environment variables configuration handler
```

---

## How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/AmnaShaukat-ai/MoinSystems-AI-Business-Agent.git
cd MoinSystems-AI-Business-Agent
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the root directory and configure your keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
N8N_WEBHOOK_URL=http://localhost:5679/webhook/lead-capture
```

### 4. Start the FastAPI Server
```bash
python -m uvicorn main:app --reload
```

### 5. Start n8n Container (Docker)
Ensure Docker Desktop is running, then start your container:

```bash
docker start n8n-ollama-project
```

---

## Usage Example

You can test the agent API using Thunder Client, Postman, or cURL.

* **Endpoint:** `POST http://localhost:8000/business-agent`
* **Content-Type:** `application/json`

### Step 1: Initial Request (Lead Info Provided)
**Request Body:**
```json
{
  "message": "Hi, I want a WhatsApp chatbot for my clothing business. My name is Amna, email is amna@test.com, and contact is 123456789.",
  "session_id": "user_123"
}
```

**Agent Response (Human-in-the-Loop Confirmation):**
> *"I have your details (Name: Amna, Email: amna@test.com). Should I save this lead for our team?"*

---

### Step 2: User Confirmation
**Request Body:**
```json
{
  "message": "Yes, save it.",
  "session_id": "user_123"
}
```

**Final Agent Response:**
> *"Thank you! Your details have been successfully captured. Our team will contact you shortly."*