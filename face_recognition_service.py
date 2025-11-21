import face_recognition
import numpy as np
from database import get_all_face_encodings

class FaceRecognitionService:
    """Service for face recognition operations"""
    
    def __init__(self):
        self.tolerance = 0.6  # Lower = more strict matching
    
    def encode_face(self, image_path):
        """
        Encode a face from an image file.
        Returns the face encoding as a numpy array, or None if no face is found.
        """
        try:
            # Load image
            image = face_recognition.load_image_file(image_path)
            
            # Find face locations
            face_locations = face_recognition.face_locations(image)
            
            if len(face_locations) == 0:
                return None
            
            # If multiple faces, use the largest one
            if len(face_locations) > 1:
                # Calculate face sizes and pick the largest
                face_sizes = [(bottom - top) * (right - left) 
                             for (top, right, bottom, left) in face_locations]
                largest_face_idx = face_sizes.index(max(face_sizes))
                face_locations = [face_locations[largest_face_idx]]
            
            # Get face encodings
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            if len(face_encodings) == 0:
                return None
            
            return face_encodings[0]
            
        except Exception as e:
            print(f"Error encoding face: {e}")
            return None
    
    def find_matches(self, query_encoding, threshold=0.6):
        """
        Find matches for a query face encoding in the database.
        
        Args:
            query_encoding: numpy array of the face encoding to search for
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
            
            # Calculate face distance
            distance = face_recognition.face_distance([stored_encoding], query_encoding)[0]
            
            # Check if distance is below threshold
            if distance <= threshold:
                # Convert distance to confidence (0-1 scale, inverted)
                # Lower distance = higher confidence
                confidence = 1 - (distance / threshold)
                confidence = max(0, min(1, confidence))  # Clamp between 0 and 1
                
                matches.append({
                    'person_id': stored['person_id'],
                    'distance': float(distance),
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
        
        distance = face_recognition.face_distance([encoding1], encoding2)[0]
        return distance <= threshold, float(distance)

