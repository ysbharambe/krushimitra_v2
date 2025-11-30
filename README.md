# 🌾 KrushiMitra - AI-Powered Plant Disease Detection

A full-stack web application that helps farmers detect plant diseases using YOLOv8 AI model and provides detailed treatment recommendations.

![KrushiMitra](https://img.shields.io/badge/AI-YOLOv8-green) ![FastAPI](https://img.shields.io/badge/Backend-FastAPI-blue) ![React](https://img.shields.io/badge/Frontend-React-cyan)

## 🎯 Features

### Core Features
- 📸 **Image Upload**: Drag & drop or click to upload crop images
- 🤖 **AI Disease Detection**: YOLOv8-powered disease identification
- 💊 **Treatment Recommendations**: Both chemical and organic solutions
- 🌍 **Multilingual Support**: 10+ Indian languages
- 🔊 **Text-to-Speech**: Accessibility for all farmers
- 🔄 **Model Retraining**: Continuous improvement with user data
- ☁️ **Cloud Storage**: Cloudinary integration for image hosting
- 📱 **Mobile-Friendly**: Responsive design for all devices

### Disease Detection
The system can detect:
- Leaf Spot
- Leaf Blight
- Powdery Mildew
- Rust
- Bacterial Blight
- Early Blight
- Late Blight
- Anthracnose
- Mosaic Virus
- Healthy plants

## 🏗️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **YOLOv8 (Ultralytics)**: State-of-the-art object detection
- **Cloudinary**: Image hosting and management
- **SQLite**: Lightweight database for predictions
- **Google Translate API**: Multilingual support

### Frontend
- **React 18**: Modern UI library
- **Tailwind CSS**: Utility-first styling
- **Framer Motion**: Smooth animations
- **Axios**: HTTP client
- **React i18next**: Internationalization
- **Lucide React**: Icon library

## 📁 Project Structure

```
KrushiMitra/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── routes/
│   │   ├── predict.py          # Disease prediction endpoint
│   │   ├── retrain.py          # Model retraining endpoint
│   │   └── translate.py        # Translation endpoint
│   ├── models/
│   │   ├── best.pt             # Trained YOLOv8 model (add your own)
│   │   └── retrain_yolo.py     # Retraining script
│   ├── utils/
│   │   ├── pesticide_data.json # Treatment recommendations
│   │   ├── cloudinary_utils.py # Cloudinary integration
│   │   └── db_utils.py         # Database operations
│   ├── datasets/
│   │   ├── data.yaml           # Dataset configuration
│   │   └── user_collected/     # User-uploaded training data
│   ├── requirements.txt        # Python dependencies
│   └── .env.example            # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── HomePage.js
│   │   │   ├── PredictionScreen.js
│   │   │   ├── LanguageSelector.js
│   │   │   └── AdminPanel.js
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.js
│   │   ├── i18n.js
│   │   └── index.css
│   ├── package.json
│   ├── tailwind.config.js
│   └── .env.example
└── README.md
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- Cloudinary account (free tier works)
- YOLOv8 pretrained model or custom-trained model

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
```

Edit `.env` and add your Cloudinary credentials:
```env
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

5. **Add YOLOv8 Model**
Place your trained YOLOv8 model in `backend/models/best.pt` or download a pretrained model:
```bash
# The app will automatically download yolov8s.pt if best.pt is not found
```

6. **Start the backend server**
```bash
python main.py
```

Backend will run at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment variables**
```bash
cp .env.example .env
```

Edit `.env`:
```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_CLOUDINARY_UPLOAD_URL=https://api.cloudinary.com/v1_1/YOUR_CLOUD_NAME/image/upload
REACT_APP_CLOUDINARY_UPLOAD_PRESET=krushimitra
```

**Important**: Create an upload preset named "krushimitra" in your Cloudinary dashboard with "Unsigned" signing mode.

4. **Start the development server**
```bash
npm start
```

Frontend will run at `http://localhost:3000`

## 📖 Usage Guide

### For Farmers

1. **Open the Application**
   - Visit `http://localhost:3000` in your browser

2. **Select Language**
   - Click the language selector in the top-right corner
   - Choose your preferred language from the dropdown

3. **Upload Image**
   - Drag & drop a photo of your affected crop/leaf
   - Or click the upload area to browse files
   - Supported formats: JPG, PNG (Max 10MB)

4. **View Results**
   - Wait for AI analysis (usually 2-5 seconds)
   - See detected disease with confidence score
   - View treatment recommendations

5. **Get Treatment Details**
   - Click on "Chemical Treatment" or "Organic Treatment"
   - Read description and application steps
   - Click "Where to Buy" to purchase products

6. **Listen to Results**
   - Click "Listen to Result" for audio output
   - Helpful for farmers with reading difficulties

7. **Upload Another Photo**
   - Click "Upload Another Photo" to analyze more crops

### For Administrators

1. **Access Admin Panel**
   - Click "Admin" in the header

2. **View Model Statistics**
   - See current model version
   - Check accuracy metrics
   - View last update timestamp

3. **Trigger Retraining**
   - Click "Start Retraining" to fine-tune the model
   - Process runs in background
   - View retraining history

## 🔧 Configuration

### Cloudinary Setup

1. Sign up at [Cloudinary](https://cloudinary.com/)
2. Get your credentials from Dashboard
3. Create an upload preset:
   - Go to Settings → Upload
   - Scroll to "Upload presets"
   - Click "Add upload preset"
   - Set "Signing Mode" to "Unsigned"
   - Name it "krushimitra"
   - Save

### Model Training (Optional)

To train your own YOLOv8 model:

1. **Prepare Dataset**
```
datasets/user_collected/
├── images/
│   ├── train/
│   └── val/
└── labels/
    ├── train/
    └── val/
```

2. **Update data.yaml**
Modify `backend/datasets/data.yaml` with your class names

3. **Train Model**
```bash
cd backend/models
python retrain_yolo.py
```

## 🌐 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints

- `POST /api/predict/` - Predict disease from image URL
- `POST /api/retrain/` - Trigger model retraining
- `POST /api/translate/` - Translate text
- `GET /api/languages/` - Get supported languages
- `GET /api/model-info/` - Get current model information

## 🌍 Supported Languages

- English (en)
- Hindi (hi)
- Marathi (mr)
- Gujarati (gu)
- Tamil (ta)
- Telugu (te)
- Kannada (kn)
- Bengali (bn)
- Punjabi (pa)
- Malayalam (ml)

## 🔒 Security Notes

- Never commit `.env` files to version control
- Keep Cloudinary credentials secure
- Use CORS restrictions in production
- Implement rate limiting for API endpoints
- Validate all user inputs

## 📊 Performance

- **Prediction Time**: ~2-5 seconds
- **Supported Image Size**: Up to 10MB
- **Recommended Image Resolution**: 640x640 or higher
- **Concurrent Users**: Scalable with proper infrastructure

## 🐛 Troubleshooting

### Backend Issues

**Model not found error**
```bash
# Download YOLOv8 model manually
pip install ultralytics
yolo export model=yolov8s.pt format=onnx
```

**Import errors**
```bash
pip install --upgrade -r requirements.txt
```

### Frontend Issues

**Module not found**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Cloudinary upload fails**
- Check your upload preset is "Unsigned"
- Verify CLOUDINARY_UPLOAD_URL is correct
- Check network/firewall settings

## 🚀 Deployment

### Backend (Heroku/Railway/Render)
1. Add `Procfile`: `web: uvicorn main:app --host 0.0.0.0 --port $PORT`
2. Set environment variables
3. Deploy

### Frontend (Vercel/Netlify)
1. Build: `npm run build`
2. Deploy `build` folder
3. Set environment variables

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is developed for educational purposes and to help farmers. Feel free to use and modify as needed.

## 👥 Authors

**KrushiMitra Team**
- Developed with ❤️ for Indian Farmers

## 🙏 Acknowledgments

- Ultralytics for YOLOv8
- FastAPI community
- React and Tailwind CSS teams
- Indian farming community for inspiration

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Email: support@krushimitra.com (example)

---

**Made with 🌱 for sustainable farming**
