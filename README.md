# Hybrid Fake Job Detection

An enterprise-grade, production-ready web application for detecting fraudulent job postings using a hybrid verification strategy that combines **Traditional Machine Learning** (Scikit-Learn) with **Agentic AI** (LangGraph + Google Gemini).

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (React/Vite)                   │
│                                                              │
│  Landing → Login → Verify → Dashboard → History → 404       │
│                                                              │
│  Firebase Auth (Google OAuth) → JWT → API Layer (Axios)     │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP + Bearer Token
┌──────────────────────▼──────────────────────────────────────┐
│                      Backend (FastAPI)                       │
│                                                              │
│  Routes → Auth Middleware → Validators → Services            │
│                                                              │
│  ┌─────────────────┐    ┌──────────────────┐                │
│  │  Pipeline A      │    │  Pipeline B       │               │
│  │  (ML Pipeline)   │    │  (Agent Pipeline) │               │
│  │                  │    │                   │               │
│  │  Preprocessor    │    │  Company Extract  │               │
│  │  Feature Extrac  │    │  WHOIS Check      │               │
│  │  Classifier      │    │  Website Invest   │               │
│  │  Keyword Detect  │    │  Online Reputation│               │
│  │  Risk Scoring    │    │  Evidence Aggr    │               │
│  │                  │    │  Gemini Reasoning  │               │
│  └────────┬─────────┘    └────────┬──────────┘               │
│           │                      │                          │
│           └──────────┬───────────┘                          │
│                      ▼                                       │
│           ┌──────────────────┐                               │
│           │ Synthesis Service│                               │
│           │ (Score Combine)  │                               │
│           └────────┬─────────┘                               │
│                    ▼                                         │
│           ┌──────────────────┐                               │
│           │   Repository     │──► MongoDB (Motor)            │
│           └──────────────────┘                               │
└──────────────────────────────────────────────────────────────┘
```

## Folder Structure

```
Hybrid-Fake-Job-Detection/
├── frontend/                    # React + Vite + Tailwind CSS
│   ├── src/
│   │   ├── api/                 # Axios instance & endpoint functions
│   │   ├── components/          # Reusable UI components
│   │   │   ├── common/          # Button, Card, Input, Spinner, Badge, Modal
│   │   │   ├── layout/          # Navbar, Footer, MainLayout
│   │   │   ├── auth/            # GoogleLoginButton
│   │   │   ├── verification/    # VerificationForm, LoadingProgress, ResultCard
│   │   │   └── dashboard/       # ScoreCard, EvidenceList, HistoryItem
│   │   ├── pages/               # Landing, Login, Verify, Dashboard, History, 404
│   │   ├── contexts/            # AuthContext, VerificationContext
│   │   ├── hooks/               # useAuth, useVerify, useHistory
│   │   ├── services/            # API service layer
│   │   ├── firebase/            # Firebase initialization
│   │   ├── routes/              # React Router configuration
│   │   ├── utils/               # Formatters, Validators
│   │   ├── constants/           # App constants
│   │   ├── config/              # Environment config
│   │   ├── App.jsx              # Root component with providers
│   │   └── main.jsx             # Entry point
│   ├── .env.example
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── package.json
│
├── backend/                     # FastAPI + LangGraph + Scikit-Learn
│   ├── app/
│   │   ├── api/routes/          # auth.py, verify.py, history.py
│   │   ├── schemas/             # Pydantic models (verification, auth, response)
│   │   ├── models/              # MongoDB document models
│   │   ├── services/            # verification, synthesis, agent, history services
│   │   ├── repositories/        # VerificationRepository (MongoDB)
│   │   ├── agents/              # LangGraph StateGraph nodes
│   │   │   ├── graph.py         # StateGraph definition
│   │   │   ├── input_node.py
│   │   │   ├── company_extraction_node.py
│   │   │   ├── whois_investigation_node.py
│   │   │   ├── website_investigation_node.py
│   │   │   ├── online_reputation_investigation_node.py
│   │   │   ├── evidence_aggregation_node.py
│   │   │   └── gemini_reasoning_node.py
│   │   ├── ml/                  # Traditional ML pipeline
│   │   │   ├── pipeline.py
│   │   │   ├── preprocessor.py
│   │   │   ├── feature_extractor.py
│   │   │   ├── classifier.py
│   │   │   ├── keyword_detector.py
│   │   │   └── risk_scorer.py
│   │   ├── database/            # MongoDB connection (Motor)
│   │   ├── config/              # Settings, Firebase config
│   │   ├── auth/                # Firebase JWT verification
│   │   ├── middleware/          # CORS, error handlers
│   │   ├── core/                # Exception handlers
│   │   ├── constants/           # ML & agent constants
│   │   ├── state/               # AgentState TypedDict
│   │   ├── prompts/             # Gemini & synthesis prompts
│   │   ├── validators/          # Input validation
│   │   ├── utils/               # URL & text utilities
│   │   ├── exceptions/          # Custom exceptions
│   │   ├── logging/             # Structured logging (loguru)
│   │   └── dependencies/        # DI container
│   ├── main.py                  # FastAPI app entry point
│   ├── .env.example
│   └── requirements.txt
│
├── README.md
├── requirements.md
└── .gitignore
```

## Tech Stack

### Frontend

-   **React 18** - UI framework (JavaScript + JSX only)
-   **Vite** - Build tool with HMR
-   **Tailwind CSS** - Utility-first CSS
-   **Axios** - HTTP client
-   **React Router DOM v6** - Client-side routing
-   **Firebase** - Google OAuth authentication
-   **Context API** - State management

### Backend

-   **Python 3.10+** - Runtime
-   **FastAPI** - Web framework
-   **Uvicorn** - ASGI server
-   **Scikit-Learn** - ML pipeline (TF-IDF, Random Forest)
-   **LangGraph** - Agentic workflow orchestration
-   **LangChain** - LLM integration
-   **Google Gemini** - AI reasoning
-   **Motor** - Async MongoDB driver
-   **tavily-python** - Web reputation search API
-   **python-whois** - Domain investigation
-   **httpx + selectolax** - Web scraping
-   **Firebase Admin SDK** - JWT verification
-   **loguru** - Structured logging

## Prerequisites

-   **Node.js 18+** and **npm**
-   **Python 3.10+**
-   **MongoDB Atlas** account
-   **Firebase** project (for authentication)
-   **Google Gemini API** key
-   **Tavily Search API** key (for online reputation investigation)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Hybrid-Fake-Job-Detection.git
cd Hybrid-Fake-Job-Detection
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your actual credentials
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your actual Firebase credentials
```

## Environment Variables

### Backend (.env)

| Variable                  | Description                          |
| ------------------------- | ------------------------------------ |
| `APP_ENV`                 | Environment (development/production) |
| `FRONTEND_URL`            | Frontend URL for CORS                |
| `MONGODB_URI`             | MongoDB Atlas connection string      |
| `DATABASE_NAME`           | MongoDB database name                |
| `GEMINI_API_KEY`          | Google Gemini API key                |
| `TAVILY_API_KEY`          | Tavily Search API key                |
| `FIREBASE_PROJECT_ID`     | Firebase project ID                  |
| `FIREBASE_CLIENT_EMAIL`   | Firebase service account email       |
| `FIREBASE_PRIVATE_KEY`    | Firebase service account private key |
| `FIREBASE_STORAGE_BUCKET` | Firebase storage bucket              |
| `LOG_LEVEL`               | Logging level (INFO, DEBUG, etc.)    |

### Frontend (.env)

| Variable                            | Description             |
| ----------------------------------- | ----------------------- |
| `VITE_API_BASE_URL`                 | Backend API URL         |
| `VITE_FIREBASE_API_KEY`             | Firebase API key        |
| `VITE_FIREBASE_AUTH_DOMAIN`         | Firebase auth domain    |
| `VITE_FIREBASE_PROJECT_ID`          | Firebase project ID     |
| `VITE_FIREBASE_STORAGE_BUCKET`      | Firebase storage bucket |
| `VITE_FIREBASE_MESSAGING_SENDER_ID` | Firebase sender ID      |
| `VITE_FIREBASE_APP_ID`              | Firebase app ID         |
| `VITE_FIREBASE_MEASUREMENT_ID`      | Firebase measurement ID |

## Running the Application

### Backend (Development)

```bash
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/api/docs`

### Frontend (Development)

```bash
cd frontend
npm run dev
```

The application will be available at `http://localhost:5173`

## API Endpoints

### Authentication

-   `POST /api/v1/auth/verify` - Verify Firebase token
-   `GET /api/v1/auth/profile` - Get user profile

### Verification

-   `POST /api/v1/verify/` - Submit job posting for verification

### History

-   `GET /api/v1/history/` - Get verification history (paginated)
-   `GET /api/v1/history/{id}` - Get verification detail

### Health

-   `GET /api/health` - Health check

## Pipeline Details

### Pipeline A: Traditional ML (Scikit-Learn)

1. **Text Preprocessing** - Cleaning, stopword removal, stemming
2. **Feature Extraction** - TF-IDF vectorization (5000 features, n-grams)
3. **Classification** - Random Forest classifier
4. **Keyword Detection** - 6 categories of suspicious keywords
5. **Risk Scoring** - Weighted combination (70% classifier + 30% keywords)

### Pipeline B: Agentic AI (LangGraph + Gemini)

1. **Input Processing** - Validate and normalize input
2. **Company Extraction** - Gemini extracts company info
3. **Parallel Investigation**:
    - **WHOIS** - Domain age, registrar, registration dates
    - **Website** - Career page, HTML quality, redirects
    - **Online Reputation** - Tavily web search for scam reports, reviews, sentiment
4. **Evidence Aggregation** - Structure all evidence
5. **Gemini Reasoning** - LLM analyzes evidence and produces verdict

### Synthesis Service

-   Combines ML and Agent scores (40% ML + 60% Agent)
-   Generates explainable verdict (legitimate/suspicious/fraudulent)
-   Produces actionable recommendations

## Deployment

### Frontend (Vercel)

1. Push code to GitHub
2. Import repository in Vercel
3. Set environment variables from `.env.example`
4. Deploy

### Backend (Render)

1. Create a Web Service in Render
2. Connect GitHub repository
3. Set:
    - Runtime: Python 3
    - Build Command: `pip install -r requirements.txt`
    - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add all environment variables
5. Deploy

### Database (MongoDB Atlas)

1. Create Atlas cluster
2. Set up database user and network access
3. Copy connection string to `MONGODB_URI`

## Security

-   **Authentication**: Firebase Google OAuth with JWT verification
-   **Authorization**: Every request validated via Firebase Admin SDK
-   **Input Validation**: Pydantic schemas + custom validators
-   **CORS**: Restricted to frontend domain
-   **No Secrets in Code**: All credentials via environment variables
-   **Rate Limiting**: Per-user database isolation via Firebase UID

## Future Improvements

-   LinkedIn profile verification
-   Email domain verification
-   Company reputation API integration
-   VirusTotal URL scanning
-   Browser automation for deeper investigation
-   Additional LLM providers (OpenAI, Claude)
-   Additional ML models (XGBoost, Neural Networks)
-   Email notifications for verification results
-   Real-time WebSocket updates during verification

## Troubleshooting

### Backend fails to start

-   Ensure all environment variables are set correctly
-   Check MongoDB Atlas IP whitelist
-   Verify Firebase service account credentials

### Frontend build fails

-   Run `npm cache clean --force`
-   Delete `node_modules` and `package-lock.json`, then `npm install`
-   Check Node.js version (18+ required)

### Authentication fails

-   Verify Firebase project is configured for Google sign-in
-   Check Firebase API key in frontend `.env`
-   Ensure Firebase Admin SDK credentials are correct

### ML pipeline errors

-   Install NLTK data: `python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"`
-   Check model file paths in configuration

## License

MIT License - see LICENSE file for details.
