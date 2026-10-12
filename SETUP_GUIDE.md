# Learnify AI — Setup Guide

Complete step-by-step guide to set up and run Learnify AI on your local machine.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** 18 or higher ([Download](https://nodejs.org/))
- **Python** 3.9 or higher ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **Code Editor** (VS Code recommended)

### Verify Installation

Open terminal/command prompt and run:

```bash
node --version    # Should show v18.x.x or higher
python --version  # Should show Python 3.9.x or higher
git --version     # Should show git version x.x.x
```

---

## 🚀 Quick Start (Windows)

### Step 1: Clone the Project

```powershell
# Open PowerShell or Command Prompt
cd Desktop
git clone <repository-url>
cd AI-Micro-Project
```

### Step 2: Backend Setup

```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# You should see (venv) in your terminal prompt

# Install dependencies
pip install -r requirements.txt

# Copy environment template (optional)
copy .env.example .env
```

### Step 3: Frontend Setup

Open a **NEW terminal window** (keep backend terminal open):

```powershell
# Navigate to frontend from project root
cd frontend

# Install dependencies (this may take a few minutes)
npm install
```

### Step 4: Run the Application

#### Terminal 1 - Backend Server

```powershell
# Make sure you're in backend/ directory and venv is activated
cd backend
.\venv\Scripts\activate
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

#### Terminal 2 - Frontend Development Server

```powershell
# In a new terminal, navigate to frontend
cd frontend
npm run dev
```

You should see:
```
VITE v5.2.0  ready in 500 ms

➜  Local:   http://localhost:3000/
➜  Network: use --host to expose
➜  press h + enter to show help
```

### Step 5: Access the Application

Open your browser and go to:
```
http://localhost:3000
```

You should see the Learnify AI chat interface!

---

## 🚀 Quick Start (macOS/Linux)

### Step 1: Clone the Project

```bash
cd ~/Desktop
git clone <repository-url>
cd AI-Micro-Project
```

### Step 2: Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template (optional)
cp .env.example .env
```

### Step 3: Frontend Setup

Open a new terminal window:

```bash
cd ~/Desktop/AI-Micro-Project/frontend
npm install
```

### Step 4: Run the Application

#### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate
python main.py
```

#### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

### Step 5: Access the Application

Open browser: `http://localhost:3000`

---

## 🧪 Verify Installation

### 1. Check Backend Health

Open a new terminal and run:

```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{"status":"healthy","service":"Learnify AI Backend"}
```

### 2. Test Chat API

```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Hello\"}"
```

You should receive a JSON response with the AI's reply.

### 3. Test Frontend

1. Open `http://localhost:3000` in your browser
2. You should see "Learnify AI" header
3. Type "Hello" in the chat input
4. Click Send or press Enter
5. You should receive a response from the AI

---

## 🛠️ Troubleshooting

### Backend Issues

#### Problem: "python: command not found"
**Solution:** Use `python3` instead of `python`

#### Problem: "Module not found" errors
**Solution:** 
```bash
# Make sure virtual environment is activated
cd backend
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\activate   # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### Problem: "Port 8000 already in use"
**Solution:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### Frontend Issues

#### Problem: "npm: command not found"
**Solution:** Install Node.js from https://nodejs.org/

#### Problem: "Module not found" or dependency errors
**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json  # or del on Windows
npm install
```

#### Problem: "Port 3000 already in use"
**Solution:** The Vite dev server will automatically try port 3001, 3002, etc.

#### Problem: "Failed to fetch" or API connection errors
**Solution:**
1. Verify backend is running on port 8000
2. Check browser console for CORS errors
3. Ensure `http://localhost:8000` is accessible

### CORS Issues

If you see CORS errors in the browser console:

1. Check backend `app/core/config.py` has your frontend URL in `CORS_ORIGINS`
2. Restart the backend server
3. Clear browser cache and refresh

---

## 📁 Project Structure Quick Reference

```
AI-Micro-Project/
├── backend/          # Python FastAPI backend
│   ├── venv/        # Virtual environment (created by you)
│   ├── app/         # Application code
│   ├── main.py      # Entry point
│   └── requirements.txt
├── frontend/         # React TypeScript frontend
│   ├── node_modules/  # Dependencies (created by npm)
│   ├── src/         # Source code
│   ├── public/      # Static files
│   └── package.json
└── README.md         # Main documentation
```

---

## 🔧 Development Tips

### Using the Automatic API Documentation

FastAPI provides interactive documentation:

1. **Swagger UI:** http://localhost:8000/docs
   - Test API endpoints directly in the browser
   - See request/response schemas
   
2. **ReDoc:** http://localhost:8000/redoc
   - Alternative documentation format
   - Better for reading

### Hot Reload

Both servers support hot reload:
- **Backend:** Automatically reloads when you save `.py` files
- **Frontend:** Automatically updates browser when you save `.tsx` or `.ts` files

### Viewing Logs

- **Backend logs:** Visible in Terminal 1 where you ran `python main.py`
- **Frontend logs:** Check browser Developer Tools (F12) → Console tab

---

## 📚 Next Steps

After successful setup:

1. ✅ Read the [README.md](README.md) for project overview
2. 🧠 Review the AI Implementation Roadmap
3. 💻 Explore the codebase:
   - Frontend: `frontend/src/components/`
   - Backend: `backend/app/`
4. 🚀 Start implementing AI concepts from Unit 1

---

## 🆘 Getting Help

If you encounter issues:

1. Check this troubleshooting guide
2. Review error messages carefully
3. Search for the error online
4. Check project GitHub issues
5. Ask your project team/instructor

---

## ✅ Setup Checklist

Before you start development, ensure:

- [ ] Both backend and frontend servers are running
- [ ] No errors in backend terminal
- [ ] No errors in frontend terminal
- [ ] Browser shows Learnify AI interface at http://localhost:3000
- [ ] You can send a test message and receive a response
- [ ] API health check returns "healthy"
- [ ] You have a code editor open with the project

---

**You're all set! Happy coding! 🎉**
