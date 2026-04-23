# 🛒 Grocery Store V2 - Modernized

A premium, high-performance grocery store application built with **Flask (Python 3.14)** and **Vue.js 3**, featuring a state-of-the-art **Glassmorphism** design system and optimized backend architecture.

![Grocery Store Banner](https://img.shields.io/badge/Modern-Glassmorphism-blueviolet?style=for-the-badge)
![Python 3.14](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python)
![Vue.js](https://img.shields.io/badge/Vue.js-3-green?style=for-the-badge&logo=vuedotjs)

---

## ✨ Key Features

### 💎 Premium UI/UX
- **Glassmorphism Design**: A sleek, transparent interface with vibrant gradients and subtle micro-animations.
- **Responsive Layout**: Fully optimized for mobile, tablet, and desktop viewing.
- **Enhanced Navigation**: Intuitive navbar with guest mode support.

### ⚡ Optimized Backend
- **N+1 Query Resolution**: Uses SQLAlchemy `joinedload` for lightning-fast data fetching.
- **Database Indexing**: Optimized search performance with indexed product and category fields.
- **Efficient Transactions**: Batch commits for order processing to ensure data integrity and speed.
- **Caching**: Integrated Redis caching for frequent API requests.

### 🛠 Professional Architecture
- **Directory Structure**: Clean separation of `backend/` and `frontend/` concerns.
- **Service Management**: Automated startup and shutdown scripts for all background services.
- **Compatibility**: Custom patches for SQLAlchemy and Billiard to support Python 3.14+.

---

## 🏗 Project Structure

```text
Grocery-Store-V2/
├── backend/            # Flask API, SQLAlchemy Models, Celery Tasks
│   ├── application/    # Core logic, models, and resources
│   ├── static/         # Generated reports and exports
│   └── .venv/          # Python virtual environment
├── frontend/           # Vue.js 3 Application
│   ├── src/            # Components, Views, and Assets (theme.css)
│   └── public/         # Static entry points
├── run.sh              # Unified startup script
└── stop.sh             # Unified shutdown script
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.14**
- **Node.js & npm**
- **Redis Server** (for caching and task broker)
- **Mailhog** (for email testing)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd Grocery-Store-V2
   ```

2. **Setup Backend**:
   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Setup Frontend**:
   ```bash
   cd ../frontend
   npm install
   ```

---

## 🏃 How to Run

Use the professional scripts provided in the root directory to manage all services:

### 1. Start all services
```bash
./run.sh
```
This script will start Redis, Mailhog, the Backend server, Celery worker, Celery beat, and the Vue development server in the background.

### 2. Stop all services
```bash
./stop.sh
```
This script safely terminates all running background processes.

---

## 📊 Dashboard Access
- **Frontend**: [http://localhost:8080](http://localhost:8080)
- **Backend API**: [http://localhost:5000](http://localhost:5000)
- **Email (Mailhog)**: [http://localhost:8025](http://localhost:8025)

---

## 🛠 Troubleshooting

- **Frontend Compilation Error**: If you see "Module not found" errors related to old paths, clear the cache:
  ```bash
  rm -rf frontend/node_modules/.cache
  ```
- **Port Already in Use**: Run `./stop.sh` before running `./run.sh` to ensure a clean slate.