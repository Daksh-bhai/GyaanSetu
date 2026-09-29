# 🌉 GyaanSetu (SkillWeave)

**GyaanSetu** (Hindi: "Bridge of Knowledge") is a peer-to-peer skill exchange web application built around a **barter-style credit economy** — users teach what they know and learn what they don't, without any money changing hands.

> 🎓 Teach a skill → Earn credits → Spend credits to learn a skill from someone else.

This repository contains the complete source code for the GyaanSetu platform, including the frontend, backend, ML models, and project documentation for demo and academic use.

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Machine Learning Components](#-machine-learning-components)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [API Overview](#-api-overview)
- [Team & Contributions](#-team--contributions)
- [Roadmap / Status](#-roadmap--status)
- [License](#-license)

---

## 🚀 Overview

GyaanSetu connects **learners** and **tutors** through an AI-assisted skill-exchange platform:

- Users sign up as a **Tutor** or **Learner** (roles can be switched)
- Tutors take a **skill verification test** before they can teach
- Learners spend **credits** to book sessions; tutors earn credits by completing them
- Sessions include **real-time chat** and **peer-to-peer video calling**
- ML models power **tutor recommendations**, **badge levels**, **Smart Match**, and **fraud detection**
- An **admin panel** oversees users, sessions, reports, and platform health

This is a full-stack academic project with a Flask/MongoDB backend and a React/Tailwind frontend.

---

## ✨ Features

| Category | Details |
|---|---|
| 🔐 **Authentication** | JWT-based auth, bcrypt password hashing, role-based access (tutor/learner) |
| ✅ **Skill Verification** | Domain-wise MCQ tests (IT, Communication, Social Science) with attempt limits & cooldowns |
| 💰 **Credit Escrow System** | Credits locked on session request, released/refunded based on completion, early-end, or cancellation |
| 🤖 **Smart Match** | Mutual skill-matching algorithm for tutors (weighted scoring: rating, badge, sessions, response time) |
| 🧠 **ML Recommendations** | Cosine-similarity based tutor/learner/similar-tutor recommendations |
| 🏅 **Badge Prediction** | Random Forest classifier predicts tutor badge (Beginner / Intermediate / Expert) |
| 🚨 **Fraud Detection** | Rule-based detection for spam requests, rating abuse, and suspicious account behavior |
| 💬 **Real-time Chat** | Flask-SocketIO powered messaging with typing indicators & join/leave events |
| 📹 **Video Calling** | WebRTC peer-to-peer video calls (via `simple-peer`), synced session timers |
| 📚 **Learning Roadmaps** | Curated step-by-step roadmaps with docs/video/practice resources per skill & level |
| 🚩 **Reporting System** | User reports with categories, auto-ban thresholds (severe/total report counts) |
| 🛠️ **Admin Panel** | Platform stats, user/session management, bans, credit adjustments, report review |
| 🌗 **Light/Dark Theme** | App-wide theme toggle |

---

## 🛠️ Tech Stack

### Backend
- **Flask** (Python) — REST API, organized into blueprints
- **MongoDB Atlas** — database via **PyMongo**
- **JWT (PyJWT)** + **bcrypt** — authentication & password security
- **Flask-SocketIO** — real-time chat & call signaling
- **Flask-CORS** — cross-origin support

### Frontend
- **React** (Create React App)
- **Tailwind CSS v3**
- **React Router DOM**
- **Axios**
- **Socket.IO Client**
- **simple-peer** — WebRTC video calling

### Machine Learning
- **scikit-learn**
  - `RandomForestClassifier` — badge prediction
  - **Cosine similarity** — skill-based recommendations & Smart Match
- Rule-based fraud detection engine
- Static, structured learning-roadmap data module

---

## 📂 Project Structure

```
SkillWeave/
├── ai_models/                  # ML models (outside backend/, needs sys.path insert)
│   ├── badge_prediction.py     # RandomForest badge classifier
│   ├── fraud_detection.py      # Rule-based fraud checks
│   ├── recommendation_model.py # Cosine similarity recommendations
│   └── learning_module.py      # Static learning roadmap data
│
├── backend/
│   ├── app.py                  # Flask app entrypoint + SocketIO init
│   ├── data/
│   │   └── question_bank.py    # Skill verification MCQ bank
│   ├── models/
│   │   ├── user_model.py       # MongoDB connection + users collection
│   │   ├── session_model.py    # sessions collection
│   │   └── review_model.py     # reviews collection
│   ├── routes/
│   │   ├── auth_routes.py      # register/login/profile/rating/smart-match
│   │   ├── session_routes.py   # request/accept/reject/complete/cancel sessions
│   │   ├── test_routes.py      # skill verification test flow
│   │   ├── learning_routes.py  # roadmap endpoints
│   │   ├── admin_routes.py     # admin dashboard & moderation
│   │   └── report_routes.py    # user reporting + auto-ban logic
│   ├── utils/
│   │   └── jwt_utils.py        # token generation/verification + ban check
│   └── socket_events.py        # Socket.IO chat & WebRTC signaling
│
└── frontend/
    ├── src/
    │   ├── api.js               # Axios API client
    │   ├── App.js                # Route definitions
    │   ├── pages/
    │   │   ├── Landing.jsx
    │   │   ├── Login.jsx / Register.jsx
    │   │   ├── TutorDashboard.jsx / LearnerDashboard.jsx
    │   │   ├── BrowseTutors.jsx
    │   │   ├── SmartMatch.jsx      # + Roadmap + VerifySkill
    │   │   ├── Sessions.jsx
    │   │   ├── SessionRoom.jsx     # chat + video + timer
    │   │   └── ChatRoom.jsx
    │   └── components/
    │       └── Navbar.jsx
    └── public/
```

---

## 🧠 Machine Learning Components

| Model | Purpose | Technique |
|---|---|---|
| **Badge Prediction** | Classifies tutors as Beginner/Intermediate/Expert | `RandomForestClassifier` trained on sessions completed, rating, rating count, response time |
| **Recommendation Engine** | Suggests tutors/learners to match with | Cosine similarity over binary skill vectors, blended with rating/badge/session-count scoring |
| **Smart Match** | Finds *mutual* teach/learn matches between tutors | Set-intersection matching + weighted scoring formula |
| **Fraud Detection** | Flags suspicious session/rating activity | Rule-based checks (request frequency, rejection rate, account age, rating patterns) |
| **Learning Roadmap** | Generates structured learning paths | Curated static dataset keyed by skill + level (Phase 1; GPT-generated roadmap planned for Phase 2) |

---

## ⚙️ Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- MongoDB Atlas connection string

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```
The Flask + SocketIO server runs on `http://localhost:5000`.

### Frontend Setup
```bash
cd frontend
npm install
npm start
```
The React app runs on `http://localhost:3000`.

### Tailwind Setup Note
This project uses **Tailwind CSS v3** with Create React App. If setting up fresh:
```bash
npx tailwindcss@3 init -p
```
(The plain `npx tailwindcss init` command does not work correctly in this CRA setup.)

---

## 🔑 Environment Variables

Create a `.env` file inside `backend/`:

```env
MONGO_URI=your_mongodb_atlas_connection_string
JWT_SECRET=your_jwt_secret_key
```

> ⚠️ Never commit real credentials to GitHub — use `.env.example` as a template and add `.env` to `.gitignore`.

---

## 📡 API Overview

Base URL: `http://localhost:5000/api`

| Blueprint | Prefix | Key Endpoints |
|---|---|---|
| Auth | `/api/auth` | `/register`, `/login`, `/profile`, `/smart_match`, `/rate_tutor/<email>`, `/recommendations` |
| Sessions | `/api/sessions` | `/send_request/<email>`, `/accept-request/<id>`, `/complete-session/<id>`, `/cancel/<id>` |
| Test | `/api/test` | `/start`, `/submit`, `/status` |
| Learning | `/api/learn` | `/roadmap`, `/my_roadmap`, `/skills` |
| Admin | `/api/admin` | `/stats`, `/users`, `/ban/<email>`, `/fraud_logs`, `/reports` |
| Report | `/api/report` | `/user/<email>`, `/my_reports`, `/against_me` |

All protected routes require a header: `Authorization: Bearer <token>`
Admin routes require: `X-Admin-Key: <admin_key>`

---




## 🗺️ Roadmap / Status

- ✅ Phases 1–15: Core backend, ML models, frontend, real-time features — **Complete**
- ⏳ Phase 16: Deployment — **In Progress**
- ⏳ Phase 17: Testing — **In Progress**
- 📄 Final academic report & viva preparation — **In Progress**

---

## 📄 License

This project was built for academic purposes as a final year submission. Add a license of your choice (e.g., MIT) if open-sourcing.

---

<p align="center">Made with 💚 by the GyaanSetu Team</p>
Thank You 
