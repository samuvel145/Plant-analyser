# Product Requirements Document (PRD)
# AI Plant Disease Detection Chat Agent

---

> **Version:** 1.0.0
> **Status:** Draft — Ready for Engineering Review
> **Author:** Senior PM & AI Architect
> **Last Updated:** April 2026

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Goals & Objectives](#3-goals--objectives)
4. [User Personas](#4-user-personas)
5. [User Stories](#5-user-stories)
6. [Functional Requirements](#6-functional-requirements)
7. [Non-Functional Requirements](#7-non-functional-requirements)
8. [System Architecture](#8-system-architecture)
9. [API Design](#9-api-design)
10. [AI/ML Design](#10-aiml-design)
11. [Data Flow Diagram](#11-data-flow-diagram)
12. [UI/UX Description](#12-uiux-description)
13. [Edge Cases & Error Handling](#13-edge-cases--error-handling)
14. [Guardrails & Safety](#14-guardrails--safety)
15. [Metrics for Success](#15-metrics-for-success)
16. [Future Enhancements](#16-future-enhancements)
17. [Development Roadmap](#17-development-roadmap)

---

## 1. Executive Summary

The **AI Plant Disease Detection Chat Agent** is a production-grade, chat-based web application that empowers farmers, agronomists, gardeners, and agricultural researchers to identify plant diseases in real time. Users interact via a ChatGPT-style conversational interface where they can upload leaf/plant images and receive structured AI-generated diagnoses — including disease name, confidence level, symptoms, and actionable treatment steps.

The system is powered by **Google Gemini API** (Vision + LLM), served through a **Python FastAPI** backend, and rendered in a **React + Tailwind CSS** frontend. All session data is held in Python in-memory structures (RAM-based), with no external database dependency. The agent is strictly domain-locked to plant and agriculture topics, with guardrails to prevent off-topic hallucinations.

This product directly addresses the gap between expensive lab-based plant pathology services and the need for instant, accessible, and reliable field-level diagnostics.

---

## 2. Problem Statement

### Context

Plant diseases are responsible for an estimated **20–40% of global crop yield loss** annually. Early and accurate identification is the single most impactful intervention — yet most farmers, home gardeners, and smallholder agricultural operators lack access to:

- Expert plant pathologists (costly, inaccessible in rural areas)
- Reliable mobile tools that combine image recognition with contextual reasoning
- AI systems that provide structured, actionable treatment guidance — not just classification labels

### Core Problem

> **Farmers and growers cannot quickly, accurately, and affordably identify what disease is affecting their plants — and therefore cannot treat it in time.**

Existing solutions (e.g., PlantNet, Pl@ntApp) provide species identification but lack:

- Conversational follow-up capability
- Structured disease treatment protocols
- Domain-restricted safety (they often hallucinate off-topic answers)
- Session-aware multi-turn diagnosis workflows

### Opportunity

By combining Gemini's vision capabilities with a constrained, domain-locked conversational agent, this product can deliver **expert-level plant disease diagnosis in under 10 seconds**, accessible via any browser, at zero marginal cost per diagnosis.

---

## 3. Goals & Objectives

### Product Goals

| # | Goal | Measurable Target |
|---|------|-------------------|
| G1 | Deliver accurate plant disease detection via image upload | ≥ 85% user-reported accuracy in first 3 months |
| G2 | Enable multi-turn conversational diagnosis | ≥ 3 follow-up turns per session average |
| G3 | Keep the AI strictly within the agriculture domain | < 2% off-topic responses reaching the user |
| G4 | Provide structured, actionable output every time | 100% of image analysis responses follow the defined schema |
| G5 | Achieve fast response times to maintain usability | ≤ 8 seconds end-to-end for image analysis |

### Business Objectives

- Launch MVP within 8 weeks with a working chat + image analysis flow
- Serve as a foundation for future mobile app, multilingual support, and API monetization
- Establish domain authority in AI-assisted agricultural diagnostics

### Out of Scope (v1.0)

- User authentication / accounts
- Persistent storage / history across sessions
- Mobile native apps
- Multilingual support
- Crop yield forecasting

---

## 4. User Personas

### Persona 1 — Ravi, The Smallholder Farmer

| Attribute | Detail |
|-----------|--------|
| Age | 38 |
| Location | Rural Tamil Nadu, India |
| Tech literacy | Low–medium; uses WhatsApp, basic smartphone |
| Goal | Identify why his tomato leaves are turning yellow before losing the harvest |
| Pain point | Nearest agronomist is 40 km away; lab tests cost money and take days |
| Usage pattern | Uploads a photo, reads the diagnosis, follows treatment steps |

### Persona 2 — Dr. Priya, The Agricultural Researcher

| Attribute | Detail |
|-----------|--------|
| Age | 34 |
| Location | University of Agricultural Sciences, Bangalore |
| Tech literacy | High; uses Python, academic tools |
| Goal | Cross-reference AI diagnosis with field samples to validate model accuracy |
| Pain point | Existing tools lack confidence scores and symptom breakdowns |
| Usage pattern | Uploads multiple images in sequence, asks follow-up questions |

### Persona 3 — Sam, The Urban Home Gardener

| Attribute | Detail |
|-----------|--------|
| Age | 27 |
| Location | Bangalore, India |
| Tech literacy | High; uses apps daily |
| Goal | Figure out why his balcony basil plants have white powdery spots |
| Pain point | Generic web searches return conflicting advice |
| Usage pattern | Chats conversationally, asks about organic treatments |

---

## 5. User Stories

### Epic 1: Image-Based Disease Detection

- **US-01**: As a farmer, I want to upload a photo of my diseased plant leaf so that I can get an instant AI diagnosis without visiting an expert.
- **US-02**: As a user, I want to see the plant type detected automatically so I can confirm the AI understood my image correctly.
- **US-03**: As a user, I want to see a confidence percentage so I can gauge how reliable the diagnosis is.
- **US-04**: As a user, I want to receive a list of symptoms and treatment steps so I know exactly what to do next.

### Epic 2: Conversational Follow-Up

- **US-05**: As a user, I want to ask follow-up questions like "Is this treatment safe for organic farming?" and get relevant answers.
- **US-06**: As a user, I want to upload a second image mid-conversation without restarting the chat.
- **US-07**: As a user, I want to ask "What causes this disease?" and get an educational explanation.

### Epic 3: Guardrails & Safety

- **US-08**: As a product owner, I want the AI to refuse non-plant-related questions politely so users are not misled by off-topic answers.
- **US-09**: As a user, if my image is not a plant, I want a clear message asking me to upload a relevant image.

### Epic 4: UX & Interaction

- **US-10**: As a user, I want to see action buttons like "Upload another image" or "Ask another question" after each diagnosis so I know my options.
- **US-11**: As a user, I want to see a typing indicator while the AI is thinking so I know the system is working.
- **US-12**: As a user, I want the chat history to be scrollable so I can review previous responses.

---

## 6. Functional Requirements

### 6.1 Chat Interface

| ID | Requirement |
|----|-------------|
| FR-01 | The system shall render a scrollable, real-time chat interface with distinct user and AI message bubbles |
| FR-02 | The system shall support plain-text message input via a text field |
| FR-03 | The system shall display a typing/loading indicator while the AI processes a request |
| FR-04 | The system shall display action buttons ("Upload another image", "Ask another question", "Start over") after every AI diagnosis response |
| FR-05 | The system shall maintain full in-session chat history (RAM-based, cleared on page refresh) |

### 6.2 Image Upload

| ID | Requirement |
|----|-------------|
| FR-06 | The system shall allow users to upload images (JPEG, PNG, WEBP) via a clip/upload button within the chat input bar |
| FR-07 | Uploaded images shall render as a thumbnail within the user's chat bubble |
| FR-08 | The system shall validate image MIME type and size (max 10 MB) client-side before submission |
| FR-09 | Images shall be encoded to Base64 and sent to the FastAPI backend via a multipart POST request |

### 6.3 AI Disease Analysis

| ID | Requirement |
|----|-------------|
| FR-10 | Upon receiving an image, the system shall invoke Gemini Vision API to analyse the plant/leaf |
| FR-11 | The system shall return a structured response in the following exact schema every time: **Plant, Disease, Confidence, Symptoms, Treatment** |
| FR-12 | If no disease is detected, the system shall return: Disease: None detected, Confidence: High, and a healthy plant summary |
| FR-13 | If the image is not a plant, the system shall return a domain guardrail message requesting a valid plant image |

### 6.4 Conversational Follow-Up

| ID | Requirement |
|----|-------------|
| FR-14 | After an image analysis, the system shall maintain conversation context (session-scoped) for follow-up Q&A |
| FR-15 | Follow-up questions shall be answered using Gemini LLM with the previous diagnosis as context |
| FR-16 | The system shall handle at least 20 turns per session without context degradation |

### 6.5 Domain Guardrails

| ID | Requirement |
|----|-------------|
| FR-17 | The system shall reject any user query unrelated to plants, agriculture, or crop science with a polite, fixed refusal message |
| FR-18 | Guardrail classification shall occur server-side before the query reaches the Gemini LLM |

### 6.6 Session Management (In-Memory)

| ID | Requirement |
|----|-------------|
| FR-19 | Each browser session shall be assigned a UUID-based session ID |
| FR-20 | Session data (chat history, last image analysis result) shall be stored in a Python `dict` keyed by session ID |
| FR-21 | Sessions shall automatically expire after 30 minutes of inactivity (TTL enforced in-memory) |
| FR-22 | On session expiry or "Start Over", all session data shall be purged from RAM |

---

## 7. Non-Functional Requirements

### 7.1 Performance

| ID | Requirement |
|----|-------------|
| NFR-01 | Image analysis response time shall be ≤ 8 seconds (p95) under normal Gemini API latency |
| NFR-02 | Text-only follow-up response time shall be ≤ 4 seconds (p95) |
| NFR-03 | The frontend shall achieve a Lighthouse Performance score ≥ 85 |

### 7.2 Reliability

| ID | Requirement |
|----|-------------|
| NFR-04 | The FastAPI backend shall handle Gemini API timeout gracefully with a user-facing retry message |
| NFR-05 | The system shall not crash on malformed or corrupted image uploads |

### 7.3 Scalability

| ID | Requirement |
|----|-------------|
| NFR-06 | The in-memory session store shall support up to 500 concurrent sessions before RAM pressure is flagged |
| NFR-07 | The FastAPI app shall support async request handling via `asyncio` for non-blocking I/O |

### 7.4 Security

| ID | Requirement |
|----|-------------|
| NFR-08 | The Gemini API key shall be stored as an environment variable and never exposed client-side |
| NFR-09 | All image data shall be processed in-memory and never written to disk |
| NFR-10 | CORS shall be configured to allow only the deployed frontend origin |
| NFR-11 | Request payload size shall be limited to 12 MB at the FastAPI level |

### 7.5 Maintainability

| ID | Requirement |
|----|-------------|
| NFR-12 | Backend code shall follow a modular architecture: `routes/`, `services/`, `utils/`, `models/` |
| NFR-13 | All AI prompts shall be centralised in a `prompts.py` constants file for easy tuning |
| NFR-14 | The codebase shall include type annotations (Python) and PropTypes/TypeScript (React) |

### 7.6 Usability

| ID | Requirement |
|----|-------------|
| NFR-15 | The UI shall be fully responsive across desktop, tablet, and mobile viewports |
| NFR-16 | Colour contrast ratios shall meet WCAG 2.1 AA standards |
| NFR-17 | All interactive elements shall have accessible labels and keyboard navigation support |

---

## 8. System Architecture

### 8.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                         │
│          React + Tailwind CSS  (Browser / SPA)              │
│   [Chat UI] [Image Upload] [Session UUID] [Action Buttons]  │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS REST (JSON / multipart)
┌──────────────────────▼──────────────────────────────────────┐
│                      API GATEWAY LAYER                      │
│              Python FastAPI (Uvicorn / ASGI)                │
│   [CORS Middleware] [Rate Limiter] [Request Validator]      │
└──────────┬────────────────────────────┬─────────────────────┘
           │                            │
┌──────────▼──────────┐      ┌──────────▼──────────────────┐
│   ROUTING LAYER     │      │    SESSION STORE (RAM)      │
│  /api/chat          │      │  Python dict[session_id]    │
│  /api/analyse       │      │  { history, last_result,   │
│  /api/session/reset │      │    ttl_timestamp }          │
└──────────┬──────────┘      └─────────────────────────────┘
           │
┌──────────▼──────────────────────────────────────────────────┐
│                      SERVICE LAYER                          │
│                                                             │
│  ┌─────────────────┐   ┌──────────────────┐                │
│  │  GuardrailSvc   │   │  GeminiVisionSvc  │                │
│  │  (topic filter) │   │  (image analysis) │                │
│  └─────────────────┘   └──────────────────┘                │
│  ┌─────────────────┐   ┌──────────────────┐                │
│  │  GeminiLLMSvc   │   │  SessionManager  │                │
│  │  (follow-up QA) │   │  (RAM CRUD/TTL)  │                │
│  └─────────────────┘   └──────────────────┘                │
└──────────┬──────────────────────────────────────────────────┘
           │ HTTPS (google-generativeai SDK)
┌──────────▼──────────────────────────────────────────────────┐
│                   EXTERNAL AI LAYER                         │
│              Google Gemini API                              │
│   gemini-1.5-pro-vision  │  gemini-1.5-pro (LLM)           │
└─────────────────────────────────────────────────────────────┘
```

### 8.2 Backend Project Structure

```
backend/
├── main.py                  # FastAPI app entry point, middleware config
├── config.py                # Environment variables, constants
├── prompts.py               # All Gemini prompt templates (centralised)
├── routes/
│   ├── __init__.py
│   ├── chat.py              # POST /api/chat
│   ├── analyse.py           # POST /api/analyse
│   └── session.py           # DELETE /api/session/{session_id}
├── services/
│   ├── __init__.py
│   ├── gemini_vision.py     # Gemini Vision API wrapper
│   ├── gemini_llm.py        # Gemini LLM conversational wrapper
│   ├── guardrail.py         # Domain topic classification
│   └── session_manager.py   # In-memory session store + TTL logic
├── models/
│   ├── __init__.py
│   ├── request_models.py    # Pydantic request schemas
│   └── response_models.py   # Pydantic response schemas
└── utils/
    ├── __init__.py
    ├── image_utils.py       # Base64 decode, MIME validation
    └── response_formatter.py # Structured output parser
```

### 8.3 Frontend Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── App.jsx
│   ├── main.jsx
│   ├── api/
│   │   └── agentApi.js      # Axios wrappers for backend endpoints
│   ├── components/
│   │   ├── ChatWindow.jsx   # Scrollable message history
│   │   ├── MessageBubble.jsx # User vs AI bubble renderer
│   │   ├── InputBar.jsx     # Text input + image upload button
│   │   ├── TypingIndicator.jsx
│   │   ├── DiagnosisCard.jsx # Structured diagnosis renderer
│   │   └── ActionButtons.jsx # Post-response CTA buttons
│   ├── hooks/
│   │   └── useChat.js       # Chat state management hook
│   ├── utils/
│   │   └── imageUtils.js    # Client-side validation
│   └── styles/
│       └── index.css        # Tailwind directives + custom CSS
├── tailwind.config.js
└── vite.config.js
```

---

## 9. API Design

### 9.1 Endpoint Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/analyse` | Upload plant image for disease detection |
| POST | `/api/chat` | Send follow-up text message in a session |
| DELETE | `/api/session/{session_id}` | Reset/clear a session from memory |
| GET | `/api/health` | Health check endpoint |

---

### 9.2 `POST /api/analyse` — Image Analysis

**Request (multipart/form-data)**

```
Content-Type: multipart/form-data

Fields:
  image       : binary file   (required) JPEG/PNG/WEBP, max 10MB
  session_id  : string        (required) UUID v4
  message     : string        (optional) User's accompanying note e.g. "Leaves are yellowing"
```

**Success Response — 200 OK**

```json
{
  "session_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "type": "diagnosis",
  "data": {
    "plant": "Tomato (Solanum lycopersicum)",
    "disease": "Early Blight (Alternaria solani)",
    "confidence": "91%",
    "symptoms": [
      "Dark brown concentric ring lesions on lower/older leaves",
      "Yellow halo surrounding lesions",
      "Premature defoliation starting from the base",
      "Stem lesions with dark, sunken cankers near soil level"
    ],
    "treatment": [
      "Remove and destroy all infected leaves immediately; do not compost",
      "Apply copper-based fungicide (e.g. Bordeaux mixture) every 7–10 days",
      "Ensure adequate plant spacing (≥ 60 cm) to improve air circulation",
      "Avoid overhead irrigation; use drip irrigation to keep foliage dry",
      "Rotate crops — avoid planting tomatoes in the same bed for ≥ 2 years",
      "Apply mulch to prevent soil-splash inoculum reaching lower leaves"
    ]
  },
  "follow_up_prompt": "You can ask me more about this disease, organic treatment alternatives, or upload another image."
}
```

**Error Response — 422 Unprocessable Entity (non-plant image)**

```json
{
  "session_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "type": "guardrail",
  "message": "The uploaded image does not appear to be a plant or leaf. Please upload a clear photo of a plant, leaf, or crop for accurate diagnosis."
}
```

**Error Response — 400 Bad Request (invalid file)**

```json
{
  "error": "invalid_image",
  "message": "Unsupported file type. Please upload a JPEG, PNG, or WEBP image under 10 MB."
}
```

---

### 9.3 `POST /api/chat` — Conversational Follow-Up

**Request (application/json)**

```json
{
  "session_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "message": "Is the copper fungicide safe to use if my tomatoes are close to harvest?"
}
```

**Success Response — 200 OK**

```json
{
  "session_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "type": "chat",
  "message": "Copper-based fungicides have a pre-harvest interval (PHI) of typically 0–7 days depending on the specific product formulation. If your tomatoes are within 1–2 weeks of harvest, check the product label for the PHI. As an organic-safe alternative, consider Bacillus subtilis-based biofungicides (e.g., Serenade) which have a 0-day PHI and are approved for use right up to harvest."
}
```

**Guardrail Response — 200 OK (off-topic query)**

```json
{
  "session_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "type": "guardrail",
  "message": "I'm specialised in plant health and agricultural diagnostics only. I'm not able to help with that topic. Feel free to ask me about your plant's disease, treatment options, or upload a new image!"
}
```

---

### 9.4 `DELETE /api/session/{session_id}` — Reset Session

**Response — 200 OK**

```json
{
  "message": "Session f47ac10b-58cc-4372-a567-0e02b2c3d479 has been cleared successfully."
}
```

---

### 9.5 `GET /api/health` — Health Check

**Response — 200 OK**

```json
{
  "status": "ok",
  "active_sessions": 42,
  "gemini_api": "reachable"
}
```

---

## 10. AI/ML Design

### 10.1 Model Selection

| Task | Model | Justification |
|------|-------|---------------|
| Image analysis + plant/disease detection | `gemini-1.5-pro` (vision) | Best-in-class multimodal understanding; handles varied lighting, angles, image quality |
| Conversational follow-up & formatting | `gemini-1.5-pro` (LLM) | Strong instruction-following; maintains context window for multi-turn |
| Domain guardrail classification | `gemini-1.5-flash` (LLM) | Lightweight, fast, cost-efficient for binary topic classification |

### 10.2 Prompt Design

#### Vision Analysis System Prompt

```
You are an expert plant pathologist and agricultural AI assistant.

When provided with an image, you MUST:
1. Identify the plant species or leaf type visible in the image.
2. Detect any visible disease, infection, pest damage, or nutrient deficiency.
3. Respond ONLY in the following strict JSON format:

{
  "plant": "<common name (scientific name)>",
  "disease": "<disease name or 'None detected — plant appears healthy'>",
  "confidence": "<percentage, e.g. 87%>",
  "symptoms": ["<symptom 1>", "<symptom 2>", "..."],
  "treatment": ["<step 1>", "<step 2>", "..."]
}

Rules:
- If the image is NOT a plant or leaf, return: {"error": "not_a_plant"}
- Do NOT add any text outside of the JSON block.
- Treatment steps must be specific, actionable, and ordered by priority.
- Confidence must reflect your true certainty level — do not over-inflate.
- Base symptoms and treatment only on what is visually evident.
```

#### Conversational Follow-Up System Prompt

```
You are a specialised agricultural AI assistant. Your ONLY domain is:
- Plant diseases, pests, and nutrient deficiencies
- Crop management, soil health, and irrigation
- Organic and chemical treatment protocols
- Agricultural science and botany

Context from last diagnosis:
Plant: {plant}
Disease: {disease}
Confidence: {confidence}

Rules:
- Answer ONLY plant/agriculture-related questions.
- If the user asks about anything outside this domain, respond:
  "I'm specialised in plant health and agricultural diagnostics only. I'm not able to help with that topic."
- Be concise, accurate, and grounded in evidence-based agronomy.
- Do not speculate beyond your agricultural knowledge domain.
- Format lists as bullet points where appropriate.
```

#### Guardrail Classification Prompt

```
You are a topic classifier. Determine if the following user message is related to:
plants, agriculture, farming, crops, soil, plant diseases, pests, gardening, botany, or horticulture.

Respond with ONLY one word: "ALLOWED" or "BLOCKED".

User message: "{user_message}"
```

### 10.3 Context Window Management

- Each session stores a rolling message history (max 20 turns = 40 messages)
- The system prompt + last diagnosis result is prepended on every LLM call
- If history exceeds 20 turns, the oldest 4 turns (2 user + 2 assistant) are dropped using a FIFO strategy
- Image binary data is never stored in the session; only the parsed diagnosis result is retained

### 10.4 Confidence Scoring

The confidence level returned by Gemini Vision is parsed and categorised:

| Confidence Range | Display Label | UI Colour |
|------------------|--------------|-----------|
| 90–100% | Very High | Green |
| 75–89% | High | Light Green |
| 55–74% | Moderate | Amber |
| 35–54% | Low | Orange |
| < 35% | Very Low | Red — with disclaimer |

For "Very Low" confidence, the UI appends: *"This result has low confidence. Please consult a local agricultural extension officer for confirmation."*

---

## 11. Data Flow Diagram

### 11.1 Image Upload & Diagnosis Flow

```
USER BROWSER                    FASTAPI BACKEND               GEMINI API
     │                                │                            │
     │  1. Select image file          │                            │
     │  2. Client-side validation     │                            │
     │     (MIME, size ≤ 10MB)        │                            │
     │                                │                            │
     │──POST /api/analyse ──────────▶│                            │
     │   multipart: image, session_id │                            │
     │                                │                            │
     │                        3. Validate session_id               │
     │                        4. Decode image to Base64            │
     │                        5. Run guardrail: is_plant_image()   │
     │                                │                            │
     │                                │──Gemini Flash classify──▶ │
     │                                │◀── "PLANT" / "NOT_PLANT"──│
     │                                │                            │
     │                        6. If NOT_PLANT → return 422        │
     │                                │                            │
     │                        7. Build vision prompt              │
     │                                │──Gemini Vision analyse──▶ │
     │                                │◀── JSON diagnosis ────────│
     │                                │                            │
     │                        8. Parse JSON response              │
     │                        9. Map confidence → tier            │
     │                       10. Store diagnosis in session RAM   │
     │                       11. Append to chat history           │
     │                                │                            │
     │◀──── 200 OK: DiagnosisResponse─│                            │
     │                                │                            │
    12. Render DiagnosisCard in chat  │                            │
    13. Show ActionButtons            │                            │
```

### 11.2 Conversational Follow-Up Flow

```
USER BROWSER                    FASTAPI BACKEND               GEMINI API
     │                                │                            │
     │  1. User types follow-up msg   │                            │
     │                                │                            │
     │──POST /api/chat ─────────────▶│                            │
     │   {session_id, message}        │                            │
     │                                │                            │
     │                        2. Load session from RAM            │
     │                        3. Run guardrail on user message    │
     │                                │                            │
     │                                │──Gemini Flash classify──▶ │
     │                                │◀── "ALLOWED"/"BLOCKED"────│
     │                                │                            │
     │                        4a. If BLOCKED → return guardrail msg
     │                        4b. If ALLOWED:                     │
     │                            Build LLM prompt with:          │
     │                            - System prompt + diagnosis ctx │
     │                            - Full chat history             │
     │                            - New user message              │
     │                                │                            │
     │                                │──Gemini LLM generate────▶ │
     │                                │◀── assistant reply────────│
     │                                │                            │
     │                        5. Append both turns to history    │
     │                        6. Enforce 20-turn FIFO limit       │
     │                                │                            │
     │◀──── 200 OK: ChatResponse ─────│                            │
     │                                │                            │
     7. Render AI bubble in chat      │                            │
```

---

## 12. UI/UX Description

### 12.1 Overall Layout

The interface adopts a **clean, nature-inspired design language** — deep forest greens and earthy tones contrast against a light off-white canvas. The aesthetic communicates trust, expertise, and calmness appropriate for agricultural diagnostics.

```
┌────────────────────────────────────────────────────────┐
│  🌿 PlantMD  — AI Plant Disease Diagnostics    [🔄]    │
├────────────────────────────────────────────────────────┤
│                                                        │
│   ┌──────────────────────────────────────────┐        │
│   │ 👤 Hello! Upload a photo of your plant   │        │
│   │    leaf to get an instant diagnosis.     │        │
│   └──────────────────────────────────────────┘        │
│                                                        │
│          ┌─────────────────────────────────┐          │
│          │ 🖼️ [leaf_photo.jpg thumbnail]   │  👤      │
│          │ "My tomato leaves look bad"     │          │
│          └─────────────────────────────────┘          │
│                                                        │
│   ┌────────────────────────────────────────────┐      │
│   │ 🌿 Diagnosis Complete                      │      │
│   │ ────────────────────────────────────────   │      │
│   │ 🌱 Plant:      Tomato                      │      │
│   │ 🦠 Disease:    Early Blight                │      │
│   │ 📊 Confidence: ████████░░ 91% (Very High) │      │
│   │                                            │      │
│   │ Symptoms:                                  │      │
│   │ • Dark concentric ring lesions             │      │
│   │ • Yellow halo around spots                 │      │
│   │                                            │      │
│   │ Treatment:                                 │      │
│   │ 1. Remove infected leaves                  │      │
│   │ 2. Apply copper fungicide every 7–10 days  │      │
│   │ 3. Use drip irrigation                     │      │
│   │                                            │      │
│   │ [Upload another image] [Ask a question]   │      │
│   └────────────────────────────────────────────┘      │
│                                                        │
│ ┌──────────────────────────────┐ [📎] [➤ Send]       │
│ │ Ask a follow-up question...  │                      │
│ └──────────────────────────────┘                      │
└────────────────────────────────────────────────────────┘
```

### 12.2 Component Specifications

#### Header Bar
- Fixed top bar with app name "🌿 PlantMD", tagline, and a "Start Over" (reset) icon button
- Subtle green gradient background; white text

#### Chat Window
- Scrollable `div` with `overflow-y: auto`; auto-scrolls to latest message on update
- User bubbles: right-aligned, green background, rounded corners (br-0)
- AI bubbles: left-aligned, white background with green left border, drop shadow
- Image thumbnails: max 200px wide, rounded, shown inline inside user bubble

#### Diagnosis Card (AI Bubble variant)
- Rendered as a structured card, not plain text
- Plant / Disease: Bold labels with leaf and bug emoji
- Confidence: Horizontal progress bar + percentage + tier badge (colour-coded)
- Symptoms: Bulleted list
- Treatment: Numbered, ordered list

#### Typing Indicator
- Three animated green dots (`●●●`) pulsing in sequence
- Displayed in an AI bubble while awaiting API response
- Replaced by actual response when received

#### Input Bar
- Fixed at the bottom of the viewport
- Paper-clip icon button opens native file picker (image only)
- Text input expands vertically up to 3 lines
- Send button activates on non-empty input or image selection

#### Action Buttons
- Rendered below each diagnosis card
- "📸 Upload another image" → focuses input bar and triggers file picker
- "💬 Ask another question" → focuses text input
- "🔄 Start over" → calls `DELETE /api/session/{id}` and resets chat state

### 12.3 Responsive Behaviour

| Viewport | Layout Adjustment |
|----------|-------------------|
| Desktop (≥ 1024px) | Chat window max-width 760px, centred |
| Tablet (768–1023px) | Full width, reduced padding |
| Mobile (< 768px) | Full-screen chat, input bar fixed, diagnosis card scrolls horizontally |

---

## 13. Edge Cases & Error Handling

| # | Scenario | Detection | Handling |
|---|----------|-----------|----------|
| EC-01 | User uploads a non-plant image (selfie, food, etc.) | Gemini Vision returns `{"error":"not_a_plant"}` | Display: "This doesn't appear to be a plant image. Please upload a clear photo of a leaf or crop." |
| EC-02 | Image is too blurry or dark for analysis | Gemini returns low confidence (< 35%) | Return diagnosis with "Very Low" confidence badge + disclaimer to consult an expert |
| EC-03 | Gemini API timeout (> 15s) | `asyncio.timeout` exception | Display: "Analysis is taking longer than usual. Please try again." with retry button |
| EC-04 | Gemini returns malformed JSON | JSON parse error in `response_formatter.py` | Log error server-side; return: "Could not parse the AI response. Please try uploading again." |
| EC-05 | User sends off-topic message | Guardrail returns "BLOCKED" | Return polite refusal message (never escalate to Gemini LLM) |
| EC-06 | File exceeds 10 MB | Client-side size check | Alert: "Image too large. Please upload a file under 10 MB." |
| EC-07 | Invalid file type (PDF, HEIC, etc.) | Client-side MIME check | Alert: "Only JPEG, PNG, and WEBP images are supported." |
| EC-08 | Session ID not found in RAM | Session lookup miss | Auto-create new session; front-end receives new `session_id` |
| EC-09 | Session TTL expired (30 min idle) | TTL check in `session_manager.py` | Auto-purge session; front-end detects 404 on next request and reinitialises |
| EC-10 | Multiple rapid image uploads (spam) | Request rate limiter (10 req/min/session) | Return 429 Too Many Requests with backoff hint |
| EC-11 | Empty text message submission | Client-side input validation | Send button disabled when input is empty and no image is queued |
| EC-12 | Network error (offline browser) | Fetch API error catch | Display: "Connection error. Please check your internet and try again." |
| EC-13 | Chat history exceeds 20 turns | FIFO in `session_manager.py` | Silently truncate oldest 4 turns; user experience unaffected |
| EC-14 | Plant detected but no disease visible | Gemini returns healthy result | Display positive card: "No disease detected — your plant appears healthy!" with general care tips |

---

## 14. Guardrails & Safety

### 14.1 Domain Restriction (Topic Guardrail)

The system implements a two-layer guardrail architecture:

**Layer 1 — Pre-LLM Classifier**
Every user text message is first routed to `gemini-1.5-flash` with the guardrail classification prompt (Section 10.2). Only messages classified as "ALLOWED" proceed to the main LLM. This prevents any off-topic query from consuming Gemini Pro capacity.

**Layer 2 — System Prompt Instruction**
The main Gemini 1.5 Pro system prompt explicitly instructs the model to refuse non-agricultural queries. This is a safety backstop in case the flash classifier passes a borderline query.

### 14.2 Image Safety

- Images are processed in RAM only and never persisted to disk
- Gemini's built-in content safety filters apply to all image inputs
- If Gemini returns a safety block on an uploaded image, the system returns: "The image could not be processed due to content safety filters. Please upload a standard plant/leaf photo."

### 14.3 Hallucination Mitigation

| Strategy | Implementation |
|----------|---------------|
| Structured output enforcement | System prompt demands strict JSON; any deviation is caught by parser |
| Confidence transparency | Confidence scores are displayed verbatim — low confidence triggers explicit disclaimer |
| Grounding instruction | Prompts explicitly instruct Gemini to "base symptoms and treatment only on what is visually evident" |
| No web browsing | The Gemini API call does not use web grounding tools — responses are based on model knowledge only, preventing fabricated URLs or fake citations |

### 14.4 Data Privacy

- No user data, images, or session content is written to disk or logged to external services
- All data lives exclusively in server RAM for the session lifetime (max 30 min)
- The `DELETE /api/session/{id}` endpoint allows users to explicitly clear their session data
- Session IDs are randomly generated UUIDs — no PII is captured or required

### 14.5 Rate Limiting

- 10 requests per minute per session_id (enforced via in-memory counter in `session_manager.py`)
- 20 maximum image uploads per session (prevents API cost abuse)

---

## 15. Metrics for Success

### 15.1 Product Health Metrics

| Metric | Target (Month 1) | Target (Month 3) |
|--------|-----------------|-----------------|
| Average image analysis response time | ≤ 8s | ≤ 6s |
| Diagnosis accuracy (user-rated thumbs up) | ≥ 75% | ≥ 85% |
| Off-topic query block rate | ≥ 98% | ≥ 99% |
| Guardrail false positive rate | ≤ 5% | ≤ 2% |
| Session error rate (5xx) | ≤ 1% | ≤ 0.5% |
| Average turns per session | ≥ 2 | ≥ 3.5 |

### 15.2 Engagement Metrics

| Metric | Target |
|--------|--------|
| Daily active sessions | 500+ by end of Month 2 |
| Image uploads per session | ≥ 1.5 average |
| Action button click-through rate | ≥ 40% |
| Session completion rate (user gets a diagnosis) | ≥ 80% |

### 15.3 Quality Metrics

| Metric | Method | Target |
|--------|--------|--------|
| Structured response schema compliance | Automated parser success rate | 100% |
| Very Low confidence diagnoses | % of total diagnoses | ≤ 10% |
| Gemini API error rate | Backend error logs | ≤ 0.5% |
| RAM session store pressure (> 500 sessions) | Server monitoring | Alert threshold |

---

## 16. Future Enhancements

### Phase 2 (Months 3–5)

- **Persistent Storage Option**: Optional user account + database (PostgreSQL) for saving diagnosis history
- **Multilingual Support**: Translate UI and responses to Hindi, Tamil, Swahili, and Spanish
- **Feedback Loop**: Thumbs up/down on each diagnosis; collect corrections to fine-tune prompts

### Phase 3 (Months 6–9)

- **Mobile App**: React Native wrapper with native camera integration (no file-picker needed)
- **Severity Scoring**: Map disease severity to a 1–10 scale based on visible damage percentage
- **Agronomist Escalation**: "Connect with a human expert" CTA for low-confidence or critical diagnoses
- **Treatment Product Lookup**: Link treatment steps to locally available products via an external agrochemical API

### Phase 4 (Months 10–12)

- **Batch Analysis**: Upload 5–10 images in a single session for field survey workflows
- **Geo-tagged Disease Alerts**: Aggregate anonymised disease reports by region; display heatmap
- **Crop Calendar Integration**: Contextualise treatment advice with local planting season data
- **API Monetisation**: Public REST API for third-party agtech apps (freemium model)

---

## 17. Development Roadmap

### Phase 1 — MVP (Weeks 1–8)

| Week | Milestone | Deliverables |
|------|-----------|-------------|
| W1 | Project Setup | Repo, CI/CD skeleton, FastAPI project structure, React project scaffold, environment config |
| W2 | Backend Core | Session manager (in-memory), Pydantic models, health endpoint, CORS setup |
| W3 | Gemini Integration | `gemini_vision.py`, `gemini_llm.py`, prompt templates, manual JSON output testing |
| W4 | Guardrail + API Routes | `guardrail.py`, `/api/analyse`, `/api/chat`, `/api/session` endpoints with full error handling |
| W5 | Frontend Foundation | Chat UI layout, MessageBubble, InputBar, TypeIndicator, Tailwind design system |
| W6 | Frontend Integration | Connect to backend APIs, DiagnosisCard renderer, confidence progress bar, action buttons |
| W7 | End-to-End Testing | Integration tests (Pytest), UI testing (Playwright), edge case validation, performance profiling |
| W8 | MVP Launch Prep | Deployment (Docker + Render/Railway), monitoring setup, README documentation, internal demo |

### Phase 2 — Hardening & Growth (Weeks 9–16)

| Week | Milestone |
|------|-----------|
| W9–10 | User feedback collection, prompt tuning based on real usage |
| W11–12 | Multilingual support (Hindi + Spanish) |
| W13–14 | Feedback loop UI (thumbs up/down), diagnosis quality scoring |
| W15–16 | Mobile responsiveness polish, PWA support |

### Phase 3 — Scale (Months 5–9)

- Mobile native app (React Native)
- Persistent storage option
- Severity scoring & treatment urgency flags
- Agronomist escalation integration

---

## Appendix A — Technology Stack Summary

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend Framework | React | 18.x |
| Frontend Styling | Tailwind CSS | 3.x |
| Frontend Build | Vite | 5.x |
| Backend Framework | Python FastAPI | 0.111.x |
| ASGI Server | Uvicorn | 0.30.x |
| AI SDK | google-generativeai | 0.7.x |
| Image Vision Model | Gemini 1.5 Pro (Vision) | Latest |
| LLM Model | Gemini 1.5 Pro | Latest |
| Guardrail Model | Gemini 1.5 Flash | Latest |
| Data Validation | Pydantic | 2.x |
| HTTP Client | Axios (frontend) | 1.x |
| Session Storage | Python dict (RAM) | — |
| Containerisation | Docker | 25.x |

---

## Appendix B — Environment Variables

```env
# Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# Session Configuration
SESSION_TTL_MINUTES=30
MAX_SESSIONS=500
MAX_TURNS_PER_SESSION=20
MAX_IMAGES_PER_SESSION=20

# Request Limits
MAX_IMAGE_SIZE_MB=10
RATE_LIMIT_RPM=10

# CORS
ALLOWED_ORIGINS=http://localhost:5173,https://your-production-domain.com

# App
DEBUG=false
LOG_LEVEL=info
```

---

*End of PRD — AI Plant Disease Detection Chat Agent v1.0.0*
