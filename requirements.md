# Project Dependencies & Justification

## Backend (Python)

### Web Framework

-   **fastapi** - Modern, fast web framework for building APIs with Python async support
-   **uvicorn** - ASGI server to run FastAPI applications
-   **python-multipart** - Required for form data parsing

### Validation

-   **pydantic** - Data validation using Python type annotations, used for request/response schemas
-   **pydantic-settings** - Environment variable management with Pydantic

### Machine Learning

-   **scikit-learn** - Traditional ML library for TF-IDF vectorization, classification (Random Forest), and feature extraction
-   **numpy** - Numerical computing, array operations for ML pipeline
-   **pandas** - Data manipulation and analysis for ML preprocessing
-   **joblib** - Model serialization for saving/loading trained ML models
-   **nltk** - Natural Language Toolkit for text preprocessing (tokenization, stopwords, stemming)

### Agentic AI (LangGraph)

-   **langgraph** - Framework for building stateful, multi-agent applications with graph-based workflows
-   **langchain** - LLM orchestration framework for chaining operations
-   **langchain-google-genai** - LangChain integration for Google's Gemini models
-   **google-generativeai** - Google's official Gemini API client

### Web Scraping & Investigation

-   **httpx** - Modern async HTTP client for making HTTP requests (career page verification)
-   **selectolax** - Fast HTML parser for extracting content from web pages
-   **python-whois** - WHOIS domain lookup for domain registration investigation
-   **tavily-python** - Tavily Search API for online reputation investigation (web search, scam reports, reviews)
-   **beautifulsoup4** - HTML parsing fallback

### Database

-   **motor** - Async MongoDB driver for FastAPI integration
-   **pymongo** - MongoDB driver (Motor is built on top of pymongo)

### Authentication

-   **firebase-admin** - Firebase Admin SDK for verifying Firebase JWT tokens
-   **pyjwt** - JSON Web Token library for token handling

### Security

-   **python-dotenv** - Load environment variables from .env files

### Utilities

-   **python-dateutil** - Date parsing utilities for WHOIS data
-   **tldextract** - Extract top-level domains from URLs for domain analysis
-   **validators** - URL validation library
-   **pydantic** - Data validation (also listed above)

### Logging & Monitoring

-   **loguru** - Structured logging library for Python (preferred over standard logging)

### Development

-   **pytest** - Testing framework
-   **pytest-asyncio** - Async test support for pytest
-   **httpx** - Also used for testing HTTP endpoints
-   **black** - Code formatter
-   **flake8** - Linter

## Frontend (JavaScript/React)

### Core

-   **react** - UI library for building component-based interfaces
-   **react-dom** - React rendering for the browser
-   **react-router-dom** - Client-side routing for single-page application

### Build & Development

-   **vite** - Modern build tool with fast HMR and optimized builds
-   **@vitejs/plugin-react** - Vite plugin for React

### Styling

-   **tailwindcss** - Utility-first CSS framework for rapid UI development
-   **postcss** - CSS transformation tool
-   **autoprefixer** - PostCSS plugin for vendor prefixes

### HTTP & API

-   **axios** - Promise-based HTTP client for API requests with interceptors

### Authentication

-   **firebase** - Firebase client SDK for Google OAuth authentication

### Routing

-   **react-router-dom** - Client-side routing

### Environment

-   **dotenv** (built into Vite) - Environment variable management via import.meta.env
