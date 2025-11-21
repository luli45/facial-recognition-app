# Missing Persons Facial Recognition System

A web-based facial recognition application designed for public safety purposes to help identify missing persons, particularly children.
Link https://facial-recognition-app-arnggta8dt2xus5ml6kobw.streamlit.app/
## Available Versions

- **Flask Version** (`app.py`) - Traditional web app with custom HTML/CSS
- **Streamlit Version** (`streamlit_app.py`) - Interactive dashboard, ready for Streamlit Cloud deployment ⭐

## Features

- **Face Recognition**: Advanced facial recognition using deep learning models
- **Database Management**: Store and manage missing persons records with photos
- **Search Functionality**: Upload a photo to search against the database
- **Match Confidence**: Get confidence scores for potential matches
- **Modern UI**: Clean, intuitive web interface

## Requirements

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Note: The `face-recognition` library requires `dlib`, which may need additional system dependencies:
   - **macOS**: `brew install cmake dlib`
   - **Linux**: `sudo apt-get install cmake libopenblas-dev liblapack-dev`
   - **Windows**: Install Visual Studio Build Tools

2. **Set up environment variables** (optional):
   ```bash
   # Copy the example file
   cp .env.example .env
   # Edit .env and add your Hugging Face API key
   ```
   (Note: This app currently uses the `face-recognition` library directly, but the API key is available for future enhancements)

3. **Create necessary directories:**
   The app will automatically create the `uploads` directory when you first run it.

## Usage

### Option 1: Streamlit (Recommended for Deployment)

1. **Start the Streamlit app:**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Open your browser:**
   The app will automatically open at `http://localhost:8501`

### Option 2: Flask

1. **Start the Flask application:**
   ```bash
   python app.py
   ```

2. **Open your browser:**
   Navigate to `http://localhost:8080`

3. **Add Missing Persons:**
   - Click on the "Add Missing Person" tab
   - Fill in the person's information (name is required)
   - Upload a clear photo showing the person's face
   - Click "Add to Database"

4. **Search for Matches:**
   - Click on the "Search" tab
   - Upload a photo containing a face
   - The system will search the database and show potential matches with confidence scores

5. **View All Records:**
   - Click on the "View All" tab to see all missing persons in the database

## How It Works

1. **Face Encoding**: When you add a person, the system extracts a unique face encoding (128-dimensional vector) from their photo
2. **Database Storage**: The encoding is stored in a SQLite database along with the person's information
3. **Face Matching**: When searching, the system compares the uploaded face encoding against all stored encodings
4. **Confidence Scoring**: Matches are ranked by distance, with confidence scores calculated based on similarity

## Technical Details

- **Backend**: Flask (Python web framework)
- **Face Recognition**: `face-recognition` library (built on dlib)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript

## Important Notes

- **Photo Quality**: For best results, use clear, front-facing photos with good lighting
- **Privacy**: This application stores photos locally. Ensure proper security measures for production use
- **Accuracy**: Facial recognition accuracy depends on photo quality, angle, and lighting conditions
- **Ethical Use**: This tool is designed for legitimate public safety purposes. Use responsibly and in accordance with applicable laws and regulations

## File Structure

```
facialrecognition_app/
├── app.py                      # Main Flask application
├── database.py                 # Database operations
├── face_recognition_service.py  # Face recognition logic
├── templates/
│   └── index.html              # Web interface
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
├── .gitignore                  # Git ignore file
├── missing_persons.db          # SQLite database (auto-created)
└── uploads/                    # Uploaded photos (auto-created)
```

## Troubleshooting

- **"No face detected"**: Ensure the photo clearly shows a face, is front-facing, and has good lighting
- **Installation issues**: Make sure you have all system dependencies for `dlib` installed
- **Port already in use**: The app uses port 8080 by default. If needed, change the port in `app.py` (line with `app.run()`)
- **403 Forbidden Error**: On macOS, port 5000 is often used by AirPlay Receiver. The app now uses port 8080 to avoid this conflict.

## Future Enhancements

- Video input support
- Batch photo processing
- Export/import database functionality
- Advanced filtering and search options
- Integration with external databases
- Mobile app support

## Deployment

### Streamlit Cloud (Recommended)
For deploying the Streamlit version to Streamlit Cloud, see [STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md).

**Quick start:**
1. Push your code to GitHub
2. Go to https://share.streamlit.io/
3. Connect your repository
4. Set main file to: `streamlit_app.py`
5. Deploy!

### GitHub
For detailed instructions on deploying to GitHub while protecting sensitive information, see [DEPLOYMENT.md](DEPLOYMENT.md).

**Quick checklist before pushing to GitHub:**
- ✅ `.env` file is in `.gitignore` (contains your API keys)
- ✅ Database files (`*.db`) are in `.gitignore`
- ✅ `uploads/` folder is in `.gitignore`
- ✅ No hardcoded API keys in source code
- ✅ Use `.env.example` as a template for others

## License

This project is intended for public safety and humanitarian purposes.

