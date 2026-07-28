# Hybrid Fake Job Detection - Architecture Plan

## Overview

Production-ready web application that detects fraudulent job postings using a hybrid strategy:

-   **Pipeline A**: Traditional Machine Learning (Scikit-Learn NLP pipeline)
-   **Pipeline B**: Agentic AI (LangGraph with LangChain + Gemini)
-   **Synthesis Service**: Combines both outputs into an explainable fraud risk report

## Complete Folder Structure

```
Hybrid-Fake-Job-Detection/
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── assets/
│   │   │   ├── logos/
│   │   │   └── icons/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── Button.jsx
│   │   │   │   ├── Card.jsx
│   │   │   │   ├── Input.jsx
│   │   │   │   ├── Spinner.jsx
│   │   │   │   ├── Badge.jsx
│   │   │   │   └── Modal.jsx
│   │   │   ├── layout/
│   │   │   │   ├── Navbar.jsx
│   │   │   │   ├── Footer.jsx
│   │   │   │   └── MainLayout.jsx
│   │   │   ├── auth/
│   │   │   │   └── GoogleLoginButton.jsx
│   │   │   ├── verification/
│   │   │   │   ├── VerificationForm.jsx
│   │   │   │   ├── LoadingProgress.jsx
│   │   │   │   └── ResultCard.jsx
│   │   │   └── dashboard/
│   │   │       ├── ScoreCard.jsx
│   │   │       ├── EvidenceList.jsx
│   │   │       └── VerificationHistoryItem.jsx
│   │   ├── pages/
│   │   │   ├── LandingPage.jsx
│   │   │   ├── LoginPage.jsx
│   │   │   ├── VerifyPage.jsx
│   │   │   ├── DashboardPage.jsx
│   │   │   ├── HistoryPage.jsx
│   │   │   └── NotFoundPage.jsx
│   │   ├── layouts/
│   │   │   └── AuthLayout.jsx
│   │   ├── contexts/
│   │   │   ├── AuthContext.jsx
│   │   │   └── VerificationContext.jsx
│   │   ├── hooks/
│   │   │   ├── useAuth.js
│   │   │   ├── useVerify.js
│   │   │   └── useHistory.js
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── api/
│   │   │   ├── axiosInstance.js
│   │   │   └── endpoints.js
│   │   ├── routes/
│   │   │   └── AppRoutes.jsx
│   │   ├── firebase/
│   │   │   └── firebase.js
│   │   ├── utils/
│   │   │   ├── validators.js
│   │   │   └── formatters.js
│   │   ├── constants/
│   │   │   └── index.js
│   │   ├── styles/
│   │   │   └── index.css
│   │   ├── config/
│   │   │   └── index.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── .env.example
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── index.html
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes/
│   │   │       ├── __init__.py
│   │   │       ├── auth.py
│   │   │       ├── verify.py
│   │   │       └── history.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── verification.py
│   │   │   ├── auth.py
│   │   │   └── response.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── verification.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── verification_service.py
│   │   │   ├── synthesis_service.py
│   │   │   ├── history_service.py
│   │   │   └── agent_service.py
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   └── verification_repository.py
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── graph.py
│   │   │   ├── input_node.py
│   │   │   ├── company_extraction_node.py
│   │   │   ├── whois_investigation_node.py
│   │   │   ├── website_investigation_node.py
│   │   │   ├── online_reputation_investigation_node.py
│   │   │   ├── evidence_aggregation_node.py
│   │   │   └── gemini_reasoning_node.py
│   │   ├── ml/
│   │   │   ├── __init__.py
│   │   │   ├── pipeline.py
│   │   │   ├── preprocessor.py
│   │   │   ├── feature_extractor.py
│   │   │   ├── classifier.py
│   │   │   ├── keyword_detector.py
│   │   │   └── risk_scorer.py
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   └── connection.py
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   ├── settings.py
│   │   │   └── firebase_config.py
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── dependencies.py
│   │   │   └── firebase_auth.py
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   ├── cors.py
│   │   │   └── error_handler.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── exceptions.py
│   │   ├── constants/
│   │   │   ├── __init__.py
│   │   │   └── ml_constants.py, agent_constants.py
│   │   ├── state/
│   │   │   ├── __init__.py
│   │   │   └── agent_state.py
│   │   ├── prompts/
│   │   │   ├── __init__.py
│   │   │   ├── gemini_prompts.py
│   │   │   └── synthesis_prompts.py
│   │   ├── validators/
│   │   │   ├── __init__.py
│   │   │   └── input_validators.py
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── url_utils.py
│   │   │   └── text_utils.py
│   │   ├── exceptions/
│   │   │   ├── __init__.py
│   │   │   └── custom_exceptions.py
│   │   ├── logging/
│   │   │   ├── __init__.py
│   │   │   └── logger.py
│   │   ├── dependencies/
│   │   │   ├── __init__.py
│   │   │   └── container.py
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_ml.py
│   │       ├── test_agents.py
│   │       └── test_synthesis.py
│   ├── main.py
│   ├── .env.example
│   └── requirements.txt
│
├── README.md
├── requirements.md
└── .gitignore
```

## Layer Responsibilities

### Backend Layers

1. **Routes** (`api/routes/`) - HTTP endpoints only. Validate payload, authenticate, call service, return response.
2. **Schemas** (`schemas/`) - Pydantic models for request/response validation.
3. **Services** (`services/`) - Business logic orchestration. Never access DB directly.
4. **Repositories** (`repositories/`) - Database access layer. MongoDB queries only.
5. **Models** (`models/`) - Database document models.
6. **ML** (`ml/`) - Traditional ML pipeline. Independent from LangGraph.
7. **Agents** (`agents/`) - LangGraph agent pipeline. Independent from ML.
8. **Auth** (`auth/`) - Firebase JWT verification.
9. **Config** (`config/`) - Environment variable loading and validation.
10. **Middleware** (`middleware/`) - CORS, error handling.
11. **Database** (`database/`) - MongoDB connection (Motor).
12. **Validators** (`validators/`) - Input validation logic.
13. **Utils** (`utils/`) - Shared utility functions.
14. **Logging** (`logging/`) - Structured logging configuration.
15. **Exceptions** (`exceptions/`) - Custom exception classes.
16. **Constants** (`constants/`) - Configuration constants.
17. **State** (`state/`) - LangGraph agent state definition.
18. **Prompts** (`prompts/`) - LLM prompt templates.

### Frontend Layers

1. **pages/** - Page-level components (one per route).
2. **components/** - Reusable UI components.
3. **layouts/** - Layout wrapper components.
4. **contexts/** - React Context providers.
5. **hooks/** - Custom React hooks.
6. **services/** - API service layer.
7. **api/** - Axios configuration and endpoints.
8. **firebase/** - Firebase initialization.
9. **routes/** - React Router configuration.
10. **utils/** - Utility functions.
11. **constants/** - Application constants.
12. **config/** - Environment configuration.

## Communication Flow

```
Frontend (React)
    │
    │ (HTTP + Bearer Token)
    ▼
FastAPI Routes
    │
    ├──► Auth Middleware (Firebase JWT)
    │
    ├──► Validators (Input Validation)
    │
    ├──► Verification Service (Orchestrator)
    │       │
    │       ├──► ML Pipeline (Pipeline A)
    │       │       ├── Preprocessor
    │       │       ├── Feature Extractor (TF-IDF)
    │       │       ├── Classifier
    │       │       ├── Keyword Detector
    │       │       └── Risk Scorer
    │       │
    │       ├──► Agent Service (Pipeline B)
    │       │       └── LangGraph StateGraph
    │       │           ├── Input Node
    │       │           ├── Company Extraction Node
    │       │           ├── WHOIS Investigation Node
    │       │           ├── Website Investigation Node
│       │           ├── Online Reputation Investigation Node
    │       │           ├── Evidence Aggregation Node
    │       │           └── Gemini Reasoning Node
    │       │
    │       └──► Synthesis Service (Combine Results)
    │               ├── Normalize Scores
    │               ├── Weighted Combination
    │               └── Generate Report
    │
    ├──► History Service
    │       └──► Verification Repository
    │               └──► MongoDB (Motor)
    │
    └──► Response (JSON)
```

## Data Flow

1. User submits job posting via VerificationForm
2. Frontend sends POST to `/api/v1/verify` with Bearer token
3. Route validates payload via Pydantic schema
4. Auth middleware verifies Firebase JWT
5. VerificationService orchestrates:
   a. Runs ML Pipeline (sync, fast)
   b. Runs Agent Pipeline (async, slower)
   c. Runs Synthesis Service (combines results)
6. Results stored in MongoDB via Repository
7. Response returned to frontend

## Security

-   Firebase Google OAuth for authentication
-   JWT verification on every request
-   Input sanitization and validation
-   CORS configured for frontend URL only
-   No secrets in code (all environment variables)
-   MongoDB access per user (Firebase UID)

## Scalability

-   ML Pipeline is stateless - can be scaled horizontally
-   Agent nodes are independent - can be parallelized
-   Repository pattern allows swapping MongoDB
-   New verification sources can be added as services
-   New ML models can be added as modules
