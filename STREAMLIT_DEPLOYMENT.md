# Deploying to Streamlit Cloud

This guide will help you deploy your Missing Persons Facial Recognition System to Streamlit Cloud.

## Prerequisites

1. A GitHub account
2. Your code pushed to a GitHub repository
3. A Streamlit Cloud account (free at https://streamlit.io/cloud)

## Step 1: Prepare Your Repository

### 1.1 Ensure `streamlit_app.py` is in your repository
The main file for Streamlit deployment is `streamlit_app.py` (not `app.py` which is for Flask).

### 1.2 Update requirements.txt
Make sure your `requirements.txt` includes:
```
streamlit
face-recognition
numpy
Pillow
python-dotenv
```

### 1.3 Create a `.streamlit/config.toml` (optional)
You can create a config file for Streamlit settings:
```bash
mkdir -p .streamlit
```

Create `.streamlit/config.toml`:
```toml
[server]
port = 8501
enableCORS = false
enableXsrfProtection = false

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

## Step 2: Push to GitHub

1. Make sure all your code is committed:
   ```bash
   git add .
   git commit -m "Add Streamlit app for deployment"
   git push origin main
   ```

2. Verify your repository is public (Streamlit Cloud requires public repos for free tier)

## Step 3: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud:**
   - Visit https://share.streamlit.io/
   - Sign in with your GitHub account

2. **Create a New App:**
   - Click "New app"
   - Select your repository
   - Set the **Main file path** to: `streamlit_app.py`
   - Set the **Python version** to: 3.9 or higher
   - Click "Deploy!"

3. **Configure Environment Variables (if needed):**
   - In the app settings, go to "Secrets"
   - Add your Hugging Face API key:
     ```
     HUGGINGFACE_API_KEY=your_api_key_here
     ```
   - Note: Currently the app uses `face-recognition` library directly, but this is available for future use

## Step 4: Important Notes for Streamlit Cloud

### Database Storage
⚠️ **Important:** Streamlit Cloud uses ephemeral file systems. Your database will be reset when the app restarts.

**Solutions:**
1. **Use Streamlit Secrets for small data** (not recommended for large databases)
2. **Use external database** (SQLite on cloud storage, PostgreSQL, etc.)
3. **Use Streamlit's built-in session state** for temporary storage during a session

### File Uploads
- Uploaded files are stored temporarily in the `uploads/` folder
- These will be cleared when the app restarts
- For production, consider using cloud storage (AWS S3, Google Cloud Storage, etc.)

### Dependencies
- Streamlit Cloud will automatically install packages from `requirements.txt`
- The `face-recognition` library requires `dlib`, which should install automatically
- If you encounter issues, you may need to add `dlib` explicitly to requirements.txt

## Step 5: Update Your App

After deployment, any changes you push to your GitHub repository will automatically trigger a redeployment.

## Troubleshooting

### "Module not found" errors
- Make sure all dependencies are in `requirements.txt`
- Check that `dlib` is available (it may need to be added explicitly)

### Database issues
- Remember that Streamlit Cloud resets files on restart
- Consider using an external database service

### Face recognition not working
- Ensure `dlib` is properly installed
- Check that uploaded images are in supported formats
- Verify images contain clear, front-facing faces

## Alternative: Local Streamlit Testing

Before deploying, test locally:

```bash
# Install streamlit if not already installed
pip install streamlit

# Run the app
streamlit run streamlit_app.py
```

This will open the app at `http://localhost:8501`

## File Structure for Streamlit

```
facialrecognition_app/
├── streamlit_app.py          # ← Main file for Streamlit (use this!)
├── app.py                    # Flask version (not used for Streamlit)
├── database.py               # Shared database module
├── face_recognition_service.py  # Shared face recognition module
├── requirements.txt          # Dependencies
├── .streamlit/
│   └── config.toml          # Optional Streamlit config
└── .env.example             # Template for environment variables
```

## Differences: Flask vs Streamlit

| Feature | Flask (`app.py`) | Streamlit (`streamlit_app.py`) |
|---------|------------------|--------------------------------|
| Deployment | Heroku, Railway, etc. | Streamlit Cloud |
| UI Framework | HTML/CSS/JS | Python widgets |
| Interactivity | Manual JS | Automatic reactivity |
| Best for | Custom web apps | Data apps, dashboards |

For Streamlit Cloud deployment, use **`streamlit_app.py`**!

