# Deployment Guide

## Pre-Deployment Checklist

Before pushing to GitHub, ensure you've protected all sensitive information:

### ✅ Files Already Protected (in .gitignore):
- `.env` - Contains your API keys
- `*.db`, `*.sqlite`, `*.sqlite3` - Database files with personal data
- `uploads/` - Uploaded photos
- `__pycache__/` - Python cache files

### 🔒 Security Checklist:

1. **Environment Variables**: 
   - ✅ Your `.env` file is in `.gitignore`
   - ✅ Create `.env.example` as a template (already done)
   - ✅ Never commit your actual `.env` file

2. **Database Files**:
   - ✅ Database files are in `.gitignore`
   - ✅ If you have test data, remove it before committing

3. **Uploaded Files**:
   - ✅ The `uploads/` folder is in `.gitignore`
   - ✅ Never commit photos of real people

4. **Code Review**:
   - ✅ No hardcoded API keys in source code
   - ✅ All sensitive data uses environment variables

## Steps to Deploy to GitHub

### 1. Initialize Git Repository (if not already done)
```bash
cd /Users/luli/Documents/apps/facialrecognition_app
git init
```

### 2. Verify .gitignore is Working
```bash
# Check what will be ignored
git status

# Make sure these files are NOT listed:
# - .env
# - missing_persons.db
# - uploads/
```

### 3. Add Files to Git
```bash
git add .
git status  # Double-check that .env and .db files are NOT included
```

### 4. Create Initial Commit
```bash
git commit -m "Initial commit: Missing Persons Facial Recognition System"
```

### 5. Create GitHub Repository
1. Go to https://github.com/new
2. Create a new repository (don't initialize with README)
3. Copy the repository URL

### 6. Connect and Push
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## For Collaborators

When someone clones your repository:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```

2. **Set up environment:**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your API key
   # (The .env file is gitignored, so it won't be committed)
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # On macOS, also install dlib via conda:
   conda install -c conda-forge dlib -y
   ```

## Important Security Notes

⚠️ **Never:**
- Commit your `.env` file
- Commit database files with real data
- Commit photos of real people
- Share API keys in issues, pull requests, or code comments

✅ **Always:**
- Use `.env.example` as a template
- Review `git status` before committing
- Use environment variables for all sensitive data
- Keep your API keys private

## If You Accidentally Committed Sensitive Data

If you accidentally committed sensitive information:

1. **Remove the file from Git history:**
   ```bash
   git rm --cached .env
   git commit -m "Remove sensitive file"
   ```

2. **If already pushed, you need to:**
   - Rotate/regenerate your API keys immediately
   - Use `git filter-branch` or BFG Repo-Cleaner to remove from history
   - Force push (⚠️ warn collaborators first)

3. **For API keys:**
   - Go to Hugging Face settings and regenerate your API key
   - Update your local `.env` file with the new key

## Repository Structure

```
facialrecognition_app/
├── .gitignore          # ✅ Protects sensitive files
├── .env.example        # ✅ Template for environment variables
├── app.py              # Main application
├── database.py          # Database operations
├── face_recognition_service.py
├── requirements.txt
├── README.md
├── DEPLOYMENT.md        # This file
├── templates/
│   └── index.html
├── .env                # ❌ NOT committed (gitignored)
├── missing_persons.db   # ❌ NOT committed (gitignored)
└── uploads/            # ❌ NOT committed (gitignored)
```

