# ⚡ Learnify AI — Quick Start

Get up and running with Learnify AI in 5 minutes!

---

## 🎯 Prerequisites

You need:
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Python 3.9+** - [Download](https://www.python.org/downloads/)

---

## 🚀 Installation (3 Steps)

### Step 1: Clone & Navigate

```bash
git clone <your-repo-url>
cd AI-Micro-Project
```

### Step 2: Setup Backend

```bash
# Windows
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# macOS/Linux
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Setup Frontend

```bash
# Open new terminal
cd frontend
npm install
```

---

## ▶️ Run the Application

### Terminal 1: Start Backend

```bash
cd backend
# Activate venv if not active
python main.py
```

✅ Backend running at: `http://localhost:8000`

### Terminal 2: Start Frontend

```bash
cd frontend
npm run dev
```

✅ Frontend running at: `http://localhost:3000`

---

## 🎉 Access the App

Open your browser:
```
http://localhost:3000
```

Start chatting with Learnify AI!

---

## 🧪 Quick Test

Test the backend API:

```bash
curl http://localhost:8000/api/health
```

Expected: `{"status":"healthy","service":"Learnify AI Backend"}`

---

## ❓ Issues?

- **Backend won't start:** Check Python version (`python --version`)
- **Frontend won't start:** Check Node version (`node --version`)
- **Connection error:** Ensure backend is running on port 8000

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed troubleshooting.

---

## 📚 Next Steps

1. ✅ App is running
2. 📖 Read [README.md](README.md) for full documentation
3. 🧠 Check the AI Implementation Roadmap
4. 💻 Start coding!

---

**Need help?** Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions.
