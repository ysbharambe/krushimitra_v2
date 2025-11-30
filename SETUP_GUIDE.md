# 🚀 KrushiMitra - Quick Setup Guide

## Step-by-Step Installation

### 1️⃣ Prerequisites

Before starting, ensure you have:
- [ ] Python 3.8 or higher installed
- [ ] Node.js 16 or higher installed
- [ ] Git installed
- [ ] A Cloudinary account (free tier)

Check versions:
```bash
python --version
node --version
npm --version
```

### 2️⃣ Clone or Download Project

If you have the project folder, navigate to it:
```bash
cd sample_v2
```

### 3️⃣ Backend Setup (10 minutes)

#### Step 1: Navigate to backend
```bash
cd backend
```

#### Step 2: Create virtual environment
**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal.

#### Step 3: Install Python packages
```bash
pip install -r requirements.txt
```

This will take 3-5 minutes. Wait for completion.

#### Step 4: Setup Cloudinary

1. Go to [https://cloudinary.com/users/register/free](https://cloudinary.com/users/register/free)
2. Sign up for free account
3. Go to Dashboard
4. Copy these values:
   - Cloud Name
   - API Key
   - API Secret

#### Step 5: Configure environment
```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Open `.env` file and add your Cloudinary credentials:
```env
CLOUDINARY_CLOUD_NAME=your_cloud_name_here
CLOUDINARY_API_KEY=your_api_key_here
CLOUDINARY_API_SECRET=your_api_secret_here
```

#### Step 6: Download YOLOv8 Model

The app will automatically download the pretrained YOLOv8 model on first run.

Alternatively, download manually:
```bash
pip install ultralytics
python -c "from ultralytics import YOLO; YOLO('yolov8s.pt')"
```

#### Step 7: Start backend server
```bash
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

✅ **Backend is now running!**

Open http://localhost:8000 to verify. Keep this terminal open.

---

### 4️⃣ Frontend Setup (5 minutes)

#### Step 1: Open NEW terminal
Keep backend terminal running. Open a new terminal window.

#### Step 2: Navigate to frontend
```bash
cd sample_v2/frontend
```

#### Step 3: Install Node packages
```bash
npm install
```

This will take 2-4 minutes.

#### Step 4: Setup Cloudinary Upload Preset

1. Go to Cloudinary Dashboard
2. Click Settings (gear icon)
3. Go to "Upload" tab
4. Scroll to "Upload presets"
5. Click "Add upload preset"
6. Configure:
   - **Preset name**: `krushimitra`
   - **Signing mode**: `Unsigned`
   - **Folder**: `krushimitra` (optional)
7. Click "Save"

#### Step 5: Configure environment
```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Open `.env` file and update:
```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_CLOUDINARY_UPLOAD_URL=https://api.cloudinary.com/v1_1/YOUR_CLOUD_NAME/image/upload
REACT_APP_CLOUDINARY_UPLOAD_PRESET=krushimitra
```

Replace `YOUR_CLOUD_NAME` with your actual Cloudinary cloud name.

#### Step 6: Start frontend server
```bash
npm start
```

Browser will automatically open at http://localhost:3000

✅ **Frontend is now running!**

---

### 5️⃣ Test the Application

1. **Open browser**: http://localhost:3000
2. **Upload test image**:
   - Drag and drop any plant leaf image
   - Or click to browse and select image
3. **Wait for results** (2-5 seconds)
4. **View detection**:
   - Disease name
   - Confidence score
   - Treatment recommendations
5. **Test features**:
   - Click "Listen to Result" for audio
   - Try changing language
   - Upload another image

---

## 🎯 Quick Commands Reference

### Start Application

**Terminal 1 - Backend:**
```bash
cd sample_v2/backend
venv\Scripts\activate     # Windows
source venv/bin/activate  # macOS/Linux
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd sample_v2/frontend
npm start
```

### Stop Application

Press `Ctrl + C` in both terminals.

---

## 🐛 Common Issues & Solutions

### Issue 1: Port already in use
**Backend (8000):**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

**Frontend (3000):**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:3000 | xargs kill -9
```

### Issue 2: Module not found (Python)
```bash
cd backend
pip install --upgrade -r requirements.txt
```

### Issue 3: Module not found (Node)
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Issue 4: Cloudinary upload fails
- Check upload preset is "Unsigned"
- Verify cloud name in .env
- Check internet connection

### Issue 5: CORS error
Backend .env should have:
```env
CORS_ORIGINS=http://localhost:3000
```

---

## 📦 Production Deployment

### Backend (Railway/Render/Heroku)

1. Create `Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

2. Set environment variables in dashboard
3. Deploy from GitHub or CLI

### Frontend (Vercel/Netlify)

1. Build:
```bash
npm run build
```

2. Deploy `build/` folder
3. Set environment variables

---

## 📞 Need Help?

- Check README.md for detailed documentation
- Open GitHub issue
- Check terminal error messages
- Verify all environment variables

---

## ✅ Checklist

Before running the app, ensure:
- [ ] Python installed and working
- [ ] Node.js installed and working
- [ ] Virtual environment activated
- [ ] All Python packages installed
- [ ] All Node packages installed
- [ ] Cloudinary credentials configured
- [ ] Upload preset created
- [ ] Both .env files configured
- [ ] Backend server running
- [ ] Frontend server running

---

**🎉 Congratulations! KrushiMitra is now ready to help farmers detect plant diseases!**
