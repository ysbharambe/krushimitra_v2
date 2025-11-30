# KrushiMitra Frontend

AI-Powered Plant Disease Detection for Farmers - React Frontend

## Features

- 🖼️ Drag & drop image upload
- 🤖 Real-time disease detection
- 💊 Chemical and organic treatment recommendations
- 🌍 Multilingual support (10+ languages)
- 🔊 Text-to-speech accessibility
- 📱 Mobile-responsive design
- 🎨 Beautiful UI with Tailwind CSS

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and update with your values:

```bash
cp .env.example .env
```

Update the following values:
- `REACT_APP_API_URL`: Your backend API URL (default: http://localhost:8000/api)
- `REACT_APP_CLOUDINARY_UPLOAD_URL`: Your Cloudinary upload URL
- `REACT_APP_CLOUDINARY_UPLOAD_PRESET`: Your Cloudinary upload preset

### 3. Start Development Server

```bash
npm start
```

The app will open at `http://localhost:3000`

### 4. Build for Production

```bash
npm run build
```

## Project Structure

```
src/
├── components/
│   ├── HomePage.js              # Main upload interface
│   ├── PredictionScreen.js      # Results display
│   ├── LanguageSelector.js      # Language switcher
│   └── AdminPanel.js            # Admin dashboard
├── services/
│   └── api.js                   # API integration
├── App.js                       # Main app component
├── i18n.js                      # Internationalization setup
└── index.js                     # Entry point
```

## Technologies Used

- **React 18**: Modern UI framework
- **Tailwind CSS**: Utility-first styling
- **Framer Motion**: Smooth animations
- **Axios**: HTTP client
- **React Dropzone**: File upload
- **React i18next**: Internationalization
- **Lucide React**: Beautiful icons

## Usage

1. **Upload Image**: Drag & drop or click to upload a crop/leaf image
2. **View Results**: See detected disease with confidence score
3. **Get Recommendations**: View chemical and organic treatment options
4. **Listen to Results**: Use text-to-speech feature
5. **Change Language**: Select from 10+ supported languages

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Contributing

Feel free to submit issues and enhancement requests!
