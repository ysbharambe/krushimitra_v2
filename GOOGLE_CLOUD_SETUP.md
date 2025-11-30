# Google Cloud Setup Guide for KrushiMitra

This guide will help you set up Google Cloud Translation and Text-to-Speech APIs for high-quality Indian language support.

## Prerequisites
- Google Cloud account
- Billing enabled (Both APIs have generous free tiers)

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Create Project"** or select existing project
3. Note your **Project ID**

## Step 2: Enable Required APIs

1. In Google Cloud Console, go to **APIs & Services** > **Library**
2. Search and enable:
   - **Cloud Translation API**
   - **Cloud Text-to-Speech API**

## Step 3: Create Service Account

1. Go to **IAM & Admin** > **Service Accounts**
2. Click **"Create Service Account"**
3. Enter details:
   - Name: `krushimitra-service`
   - Description: `Service account for translation and TTS`
4. Click **"Create and Continue"**
5. Grant roles:
   - **Cloud Translation API User**
   - **Cloud Text-to-Speech User**
6. Click **"Done"**

## Step 4: Create Service Account Key

1. Click on the service account you just created
2. Go to **Keys** tab
3. Click **"Add Key"** > **"Create new key"**
4. Select **JSON** format
5. Click **"Create"**
6. A JSON file will be downloaded - **KEEP THIS SAFE!**

## Step 5: Configure Backend

1. Copy the downloaded JSON file to your backend folder:
   ```
   backend/google-cloud-key.json
   ```

2. Update your `backend/.env` file:
   ```env
   GOOGLE_APPLICATION_CREDENTIALS=google-cloud-key.json
   GOOGLE_CLOUD_PROJECT_ID=your-project-id
   ```

3. **Add to .gitignore** (IMPORTANT - Don't commit credentials!):
   ```
   backend/google-cloud-key.json
   ```

## Step 6: Test the Setup

1. Restart your backend:
   ```bash
   cd backend
   python main.py
   ```

2. You should see:
   ```
   ✅ Google Cloud services initialized successfully
   ```

3. Test translation:
   - Upload a plant image
   - Change language to Marathi/Hindi
   - Disease name and recommendations should translate

4. Test TTS:
   - Click the speaker icon 🔊
   - Should hear clear Marathi/Hindi voice

## Free Tier Limits

### Cloud Translation API
- **Free**: First 500,000 characters/month
- **After**: $20 per million characters

### Cloud Text-to-Speech API
- **Free**: First 1 million characters/month (WaveNet voices)
- **After**: $16 per million characters

**For your use case**: These limits are more than enough for thousands of farmers using the app!

## Troubleshooting

### "Google Cloud services not initialized"
- Check if JSON key file path is correct in `.env`
- Ensure APIs are enabled in Google Cloud Console
- Verify service account has correct permissions

### "Permission denied" errors
- Make sure service account has required roles
- Check if APIs are enabled

### Translation not working
- Verify GOOGLE_APPLICATION_CREDENTIALS path
- Check internet connection
- Falls back to deep-translator if Google Cloud unavailable

### TTS not working
- Check browser console for errors
- Ensure text is not too long (max ~5000 characters)
- Falls back to browser TTS if Google Cloud unavailable

## Features After Setup

### ✅ Better Translation Quality
- More accurate for Indian languages
- Better handling of technical agricultural terms
- Context-aware translations

### ✅ High-Quality TTS
- Natural sounding Marathi/Hindi voices
- Clear pronunciation
- Professional quality audio

### ✅ Supported Languages
- Hindi (हिन्दी)
- Marathi (मराठी)
- Gujarati (ગુજરાતી)
- Tamil (தமிழ்)
- Telugu (తెలుగు)
- Kannada (ಕನ್ನಡ)
- Bengali (বাংলা)
- Punjabi (ਪੰਜਾਬੀ)
- Malayalam (മലയാളം)

## Security Notes

⚠️ **NEVER commit your Google Cloud credentials to Git!**
⚠️ **Always add key files to .gitignore**
⚠️ **Use environment variables for sensitive data**

## Cost Optimization

- Translation cached on frontend (no redundant API calls)
- TTS generates audio on-demand
- Falls back to free alternatives if quota exceeded

---

**Need help?** Check the [Google Cloud Documentation](https://cloud.google.com/docs)
