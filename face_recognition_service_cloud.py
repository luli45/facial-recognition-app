"""
Cloud-compatible face recognition service using deepface.
This version works on Streamlit Cloud without requiring dlib/cmake.
"""
import numpy as np
from database import get_all_face_encodings

try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except ImportError:
    DEEPFACE_AVAILABLE = False
    print("Warning: deepface not available. Install with: pip install deepface")

class FaceRecognitionService:
    """Service for face recognition operations using DeepFace"""
    
    def __init__(self):
        self.tolerance = 0.6  # Lower = more strict matching
        if not DEEPFACE_AVAILABLE:
            raise ImportError("deepface is required. Install with: pip install deepface")
    
    def encode_face(self, image_path):
        """
        Encode a face from an image file using DeepFace.
        Returns the face encoding as a list, or None if no face is found.
        """
        try:
            # Use DeepFace to get face embedding
            # Using VGG-Face model which is good for face recognition
            embedding = DeepFace.represent(
                img_path=image_path,
                model_name='VGG-Face',
                enforce_detection=True,
                detector_backend='opencv'  # OpenCV doesn't require dlib
            )
            
            if embedding and len(embedding) > 0:
                # Get the first face's embedding
                encoding = embedding[0]['embedding']
                return encoding
            else:
                return None
                
        except Exception as e:
            error_msg = str(e).lower()
            # If face detection fails, return None (don't raise error)
            if any(phrase in error_msg for phrase in [
                "no face detected", 
                "face could not be detected",
                "could not detect a face",
                "no face found"
            ]):
                return None
            # For other errors, log and return None
            print(f"Error encoding face: {e}")
            return None
    
    def find_matches(self, query_encoding, threshold=0.6):
        """
        Find matches for a query face encoding in the database.
        
        Args:
            query_encoding: list or numpy array of the face encoding to search for
            threshold: distance threshold for matching (lower = more strict)
        
        Returns:
            List of matches with person_id, distance, and confidence
        """
        matches = []
        
        # Get all encodings from database
        stored_encodings = get_all_face_encodings()
        
        if not stored_encodings:
            return matches
        
        # Convert query encoding to numpy array if needed
        if isinstance(query_encoding, list):
            query_encoding = np.array(query_encoding)
        
        for stored in stored_encodings:
            # Convert stored encoding to numpy array
            stored_encoding = np.array(stored['encoding'])
            
            # Calculate cosine similarity (better for normalized vectors)
            dot_product = np.dot(query_encoding, stored_encoding)
            norm_product = np.linalg.norm(query_encoding) * np.linalg.norm(stored_encoding)
            
            if norm_product == 0:
                continue
                
            cosine_similarity = dot_product / norm_product
            cosine_distance = 1 - cosine_similarity
            
            # Check if distance is below threshold
            if cosine_distance <= threshold:
                # Convert distance to confidence (0-1 scale, inverted)
                confidence = 1 - (cosine_distance / threshold)
                confidence = max(0, min(1, confidence))  # Clamp between 0 and 1
                
                matches.append({
                    'person_id': stored['person_id'],
                    'distance': float(cosine_distance),
                    'confidence': float(confidence)
                })
        
        # Sort by distance (closest first)
        matches.sort(key=lambda x: x['distance'])
        
        return matches
    
    def compare_faces(self, encoding1, encoding2, threshold=0.6):
        """
        Compare two face encodings.
        Returns True if faces match, False otherwise.
        """
        if isinstance(encoding1, list):
            encoding1 = np.array(encoding1)
        if isinstance(encoding2, list):
            encoding2 = np.array(encoding2)
        
        # Calculate cosine distance
        dot_product = np.dot(encoding1, encoding2)
        norm_product = np.linalg.norm(encoding1) * np.linalg.norm(encoding2)
        
        if norm_product == 0:
            return False, 1.0
        
        cosine_similarity = dot_product / norm_product
        cosine_distance = 1 - cosine_similarity
        
        return cosine_distance <= threshold, float(cosine_distance)

