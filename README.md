# PlantMD 🌿 — AI Plant Disease Diagnostics

PlantMD is a full-stack, AI-powered agricultural chat agent designed to help farmers, gardeners, and plant enthusiasts identify plant diseases and get actionable treatment advice in real-time. 

Built with a conversational interface, users can simply upload a photo of a leaf and chat naturally with the AI to understand the underlying causes and solutions for their crop's health issues.

## 🚀 Features

- **Instant Image Diagnostics**: Upload a photo of any plant leaf, and the AI (powered by Google Gemini Vision) instantly returns the detected plant species, disease, confidence tier, symptoms, and actionable treatments.
- **Conversational Follow-ups**: After a diagnosis, you can ask follow-up questions (e.g. "Is neem oil safe for this?") and the agent will respond with context-aware, agriculture-specific knowledge.
- **Pre-flight Guardrails**: The system uses a secondary fast classifier to ensure users stay on the topic of botany and agriculture, politely declining unrelated questions.
- **Privacy-First RAM Sessions**: Chat history is handled entirely in RAM with a 30-minute Time-To-Live (TTL). No images or chat logs are permanently persisted to any database.
- **Premium Glassmorphism UI**: A beautifully designed React interface featuring smooth animations, color-coded confidence bars, and responsive text inputs.

## 🛠️ Tech Stack

- **Frontend**: React, Vite, Vanilla CSS (Custom Design System / Glassmorphism)
- **Backend**: Python, FastAPI, Pydantic
- **AI Models**: 
  - `gemini-2.5-flash` (Vision & LLM Follow-ups)
  - `gemini-2.0-flash-lite` (Guardrail classifier)

---

## 💻 How to Run Locally

### 1. Prerequisites
- **Node.js** (v18+)
- **Python** (v3.10+)
- **Google Gemini API Key** (Get one from Google AI Studio)

### 2. Backend Setup
Open your terminal at the root of the project and navigate into the backend folder:
```bash
cd backend
```
Install the Python dependencies:
```bash
pip install -r requirements.txt
```
Create a `.env` file in the `backend/` directory with your configuration:
```env
# Gemini API
GEMINI_API_KEY=your_primary_api_key_here
GEMINI_API_KEY_FALLBACK=your_secondary_api_key_here_if_needed

# Session Configuration
SESSION_TTL_MINUTES=30
MAX_SESSIONS=500
MAX_TURNS_PER_SESSION=20
MAX_IMAGES_PER_SESSION=20

# Request Limits
MAX_IMAGE_SIZE_MB=10
RATE_LIMIT_RPM=10

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# App
DEBUG=true
LOG_LEVEL=info
```
Start the FastAPI server **(Keep this terminal open)**:
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Frontend Setup
Open a **NEW** terminal at the root of the project and navigate into the frontend folder:
```bash
cd frontend
```
Install the Node dependencies:
```bash
npm install
```
Start the Vite development server **(Keep this terminal open)**:
```bash
npm run dev
```

### 4. Access the App
Open your browser and navigate to: **http://localhost:5173/**
