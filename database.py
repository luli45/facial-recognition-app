import sqlite3
import json
import os
from datetime import datetime

DB_NAME = 'missing_persons.db'

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS missing_persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age TEXT,
            description TEXT,
            date_missing TEXT,
            contact TEXT,
            photo_path TEXT NOT NULL,
            face_encoding TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def add_missing_person(name, age, description, date_missing, contact, photo_path, face_encoding):
    """Add a new missing person to the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Convert face encoding (numpy array) to JSON string
    encoding_json = json.dumps(face_encoding.tolist())
    
    cursor.execute('''
        INSERT INTO missing_persons (name, age, description, date_missing, contact, photo_path, face_encoding)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, age, description, date_missing, contact, photo_path, encoding_json))
    
    person_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return person_id

def get_all_missing_persons():
    """Get all missing persons from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM missing_persons ORDER BY created_at DESC')
    persons = cursor.fetchall()
    
    conn.close()
    
    return [dict(person) for person in persons]

def get_missing_person_by_id(person_id):
    """Get a missing person by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM missing_persons WHERE id = ?', (person_id,))
    person = cursor.fetchone()
    
    conn.close()
    
    return dict(person) if person else None

def get_all_face_encodings():
    """Get all face encodings for matching"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, face_encoding FROM missing_persons')
    results = cursor.fetchall()
    
    conn.close()
    
    encodings = []
    for row in results:
        encoding = json.loads(row['face_encoding'])
        encodings.append({
            'person_id': row['id'],
            'encoding': encoding
        })
    
    return encodings

