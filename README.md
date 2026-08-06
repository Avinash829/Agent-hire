# 🚀 AgentHire - Hybrid Fake Job Detection

AgentHire is an AI-powered web application that detects fraudulent job postings using a **Hybrid Machine Learning + Agentic AI** approach.

Unlike traditional fake job detectors that rely only on machine learning, AgentHire combines:

-   🤖 Machine Learning for textual fraud detection
-   🧠 Agentic AI for autonomous investigations
-   🌐 Company & Website Verification
-   🔍 WHOIS Analysis
-   📰 Web Intelligence
-   📊 Explainable Risk Assessment

---

## ✨ Features

-   🔐 Firebase Authentication
-   📄 Analyze job descriptions
-   🔗 Verify job application links
-   🏢 Company legitimacy verification
-   🌍 Website investigation
-   📅 WHOIS domain lookup
-   🤖 Gemini-powered AI reasoning
-   📊 Hybrid ML + AI risk score
-   📜 Investigation history
-   📱 Responsive UI
-   🐳 Dockerized local development

---

# 🏗️ System Architecture

```text
                User
                  │
                  ▼
        React + Vite Frontend
                  │
          REST API Requests
                  │
                  ▼
        FastAPI Backend Server
                  │
     ┌────────────┼────────────┐
     │            │            │
     ▼            ▼            ▼
 Machine      Agentic AI    Firebase
 Learning      Pipeline       Auth
     │            │
     │            ├──────── WHOIS
     │            ├──────── Website Analysis
     │            ├──────── Tavily Search
     │            └──────── Gemini AI
     │
     └────────────┬────────────┘
                  ▼
          Final Fraud Score
                  │
                  ▼
             MongoDB Atlas
```

---

# 📁 Project Structure

```text
AgentHire/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── Dockerfile.dev
│   ├── package.json
│   └── .dockerignore
│
├── backend/
│   ├── app/
│   ├── models/
│   ├── routes/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env
│   └── .dockerignore
│
├── docker-compose.yml
│
└── README.md
```

---

# 🛠 Tech Stack

## Frontend

-   React
-   Vite
-   React Router
-   Axios
-   Firebase Authentication

## Backend

-   FastAPI
-   Python 3.12
-   LangGraph
-   LangChain
-   Gemini AI
-   Scikit-Learn
-   Motor
-   MongoDB Atlas

## AI Stack

-   Machine Learning
-   Agentic AI
-   Google Gemini
-   Tavily Search
-   WHOIS
-   BeautifulSoup

## Database

-   MongoDB Atlas

## Authentication

-   Firebase Authentication

## DevOps

-   Docker
-   Docker Compose

---

# 🚀 Local Development (Without Docker)

## Clone Repository

```bash
git clone https://github.com/Avinash829/Agent-hire.git

cd Agent-hire
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Runs on

```
http://localhost:5173
```

---

## Backend

Create virtual environment

### Windows

```bash
cd backend

py -3.12 -m venv .venv

.venv\Scripts\activate
```

### Linux/macOS

```bash
python3.12 -m venv .venv

source .venv/bin/activate
```

Install dependencies

```bash
python -m pip install -r requirements.txt
```

Start server

```bash
python main.py
```

Runs on

```
http://localhost:8000
```

---

# 🐳 Local Development (Docker)

## Prerequisites

Install:

-   Docker Desktop
-   Docker Compose

Verify installation

```bash
docker --version

docker compose version
```

---

## Build & Run

From project root

```bash
docker compose up --build
```

This starts both services:

| Service  | URL                   |
| -------- | --------------------- |
| Frontend | http://localhost:5173 |
| Backend  | http://localhost:8000 |

---

## Stop Containers

```bash
docker compose down
```

---

## Rebuild Images

Whenever dependencies or Dockerfiles change:

```bash
docker compose up --build
```

---

## View Running Containers

```bash
docker ps
```

---

# 🌐 Deployment

This project uses Docker **only for local development**.

Deployment remains unchanged.

## Frontend

Deploy to:

-   Vercel

Build Command

```bash
npm run build
```

---

## Backend

Deploy to:

-   Render

Build Command

```bash
python -m pip install -r requirements.txt
```

Start Command

```bash
python main.py
```

---

## Database

-   MongoDB Atlas

---

## Authentication

-   Firebase

---
