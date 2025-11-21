from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from database import init_db, add_missing_person, get_all_missing_persons, get_missing_person_by_id
from face_recognition_service import FaceRecognitionService

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Initialize database
init_db()

# Initialize face recognition service
face_service = FaceRecognitionService()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/missing-persons', methods=['GET'])
def get_missing_persons():
    """Get all missing persons from database"""
    persons = get_all_missing_persons()
    return jsonify([{
        'id': p['id'],
        'name': p['name'],
        'age': p['age'],
        'description': p['description'],
        'date_missing': p['date_missing'],
        'contact': p['contact']
    } for p in persons])

@app.route('/api/missing-persons', methods=['POST'])
def add_person():
    """Add a new missing person to the database"""
    try:
        if 'photo' not in request.files:
            return jsonify({'error': 'No photo provided'}), 400
        
        file = request.files['photo']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Get form data
        name = request.form.get('name', '').strip()
        age = request.form.get('age', '').strip()
        description = request.form.get('description', '').strip()
        date_missing = request.form.get('date_missing', '').strip()
        contact = request.form.get('contact', '').strip()
        
        if not name:
            return jsonify({'error': 'Name is required'}), 400
        
        # Save uploaded file
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process face encoding
        encoding = face_service.encode_face(filepath)
        if encoding is None:
            os.remove(filepath)
            return jsonify({'error': 'No face detected in image. Please upload a clear photo with a visible face.'}), 400
        
        # Add to database
        person_id = add_missing_person(
            name=name,
            age=age,
            description=description,
            date_missing=date_missing,
            contact=contact,
            photo_path=filepath,
            face_encoding=encoding
        )
        
        return jsonify({
            'success': True,
            'id': person_id,
            'message': 'Missing person added successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['POST'])
def search_face():
    """Search for a face in the missing persons database"""
    try:
        if 'photo' not in request.files:
            return jsonify({'error': 'No photo provided'}), 400
        
        file = request.files['photo']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save uploaded file temporarily
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f'temp_{filename}')
        file.save(filepath)
        
        # Encode the face
        encoding = face_service.encode_face(filepath)
        if encoding is None:
            os.remove(filepath)
            return jsonify({'error': 'No face detected in image. Please upload a clear photo with a visible face.'}), 400
        
        # Search for matches
        matches = face_service.find_matches(encoding, threshold=0.6)
        
        # Clean up temp file
        os.remove(filepath)
        
        # Format results
        results = []
        for match in matches:
            person = get_missing_person_by_id(match['person_id'])
            if person:
                results.append({
                    'person_id': match['person_id'],
                    'name': person['name'],
                    'age': person['age'],
                    'description': person['description'],
                    'date_missing': person['date_missing'],
                    'contact': person['contact'],
                    'confidence': round(match['confidence'] * 100, 2),
                    'distance': round(match['distance'], 4)
                })
        
        return jsonify({
            'success': True,
            'matches': results,
            'match_count': len(results)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)

