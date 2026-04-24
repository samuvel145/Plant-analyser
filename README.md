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
GEMINI_API_KEY=your_api_key_here

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
### 🏃‍♂️ Running the Application Locally (Unified Server)

You no longer need to run the frontend and backend in two separate terminals. I have unified the system so that FastAPI natively serves the compiled React application.

**For Windows Users:**
Just double-click the `start.bat` file in the project root! It will automatically:
1. Build your Vite frontend.
2. Install any missing Python dependencies.
3. Start the unified FastAPI server.

Then open your browser to: [http://127.0.0.1:8000](http://127.0.0.1:8000)

**Manual Execution (Mac/Linux):**
```bash
# 1. Build the frontend
cd frontend
npm install && npm run build

# 2. Run the unified backend server
cd ../backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```


---

### 🌐 Deployment (Vercel)

This repository is pre-configured with a highly stable `vercel.json` file. Vercel naturally excels at running "both at the same time" natively:
- It pushes the compiled React Frontend to its global Edge CDN for lightning-fast speeds.
- It deploys the FastAPI Backend as AWS Serverless Functions mapped to the `/api` route.

**To deploy:**
1. Import your GitHub repository to [Vercel](https://vercel.com/).
2. Vercel will auto-detect the configuration.
3. **Important:** Go to your Vercel Project Settings > Environment Variables, and securely add your `GEMINI_API_KEY` and `GEMINI_API_KEY_FALLBACK`.
4. Hit **Deploy**!
