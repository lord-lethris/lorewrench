# 🛠️ LoreWrench

**LoreWrench** is an AI-powered storytelling and worldbuilding tool designed to help writers create, manage, and generate rich narrative content.

It combines structured story elements (characters, relationships) with AI generation and creative controls to reduce writer’s block and enhance creativity.

---

## ✨ Features

### 👤 Character Management

* Create and store characters with name and bio
* Persistent storage using SQLite

### 🔗 Character Relationships

* Link characters together (ally, enemy, family, etc.)
* Supports multiple relationships between the same characters
* Enables complex storytelling dynamics

### 🤖 AI Character Generation

* Generate characters using local AI (Ollama)
* Automatically fills name and bio fields

### 🎛️ Creative Sliders

* Control **drama level**
* Control **tone (dark ↔ light)**
* Dynamically influences AI output

### 📖 Scene Generation

* Generate scenes between characters
* Uses:

  * Character bios
  * Relationships
  * Slider settings
* Outputs **novel-style prose** (not script format)

---

## 🧠 Tech Stack

* **Backend:** Python + FastAPI
* **Frontend:** HTML + JavaScript
* **Database:** SQLite
* **AI:** Ollama (local LLM runtime)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/lord-lethris/lorewrench.git
cd lorewrench
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Install and run Ollama

Download and install Ollama, then run:

```bash
ollama pull llama3.2
ollama run llama3.2
```

---

### 4. Start the backend

```bash
uvicorn backend.main:app --reload
```

---

### 5. Open the app

Open:

```bash
frontend/index.html
```

---

## 🔌 API Endpoints

* `POST /character` → Create character
* `GET /characters` → List characters
* `POST /relationship` → Create relationship
* `GET /relationships` → List relationships
* `POST /generate_character` → AI character generation
* `POST /generate_scene` → AI scene generation

---

## 🧭 Roadmap

* [ ] Project / Story management system
* [ ] Save generated scenes
* [ ] Genre system
* [ ] Visual relationship graph
* [ ] Advanced AI memory (story context)
* [ ] UI improvements

---

## 💡 Vision

LoreWrench aims to become a **universal writing tool** that combines:

* structured storytelling
* AI-assisted creativity
* intuitive controls (sliders, relationships, etc.)

---

## ⚖️ License

MIT License

---

## 👑 Author

Created by **Lord Lethris**
