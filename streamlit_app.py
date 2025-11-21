import streamlit as st
import os
from PIL import Image
import io
from database import init_db, add_missing_person, get_all_missing_persons, get_missing_person_by_id

# Use simple Hugging Face-based service (works on Streamlit Cloud without TensorFlow)
try:
    from face_recognition_service_simple import FaceRecognitionService
except ImportError:
    # Fallback to cloud service if simple version not available
    try:
        from face_recognition_service_cloud import FaceRecognitionService
    except ImportError:
        st.error("""
        ⚠️ Face recognition service not available. 
        
        Please ensure:
        1. HUGGINGFACE_API_KEY is set in Streamlit Cloud secrets
        2. All dependencies are installed
        """)
        st.stop()

# Page configuration
st.set_page_config(
    page_title="Missing Persons Recognition System",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_db()

# Initialize face recognition service
if 'face_service' not in st.session_state:
    st.session_state.face_service = FaceRecognitionService()

face_service = st.session_state.face_service

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .match-card {
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        background-color: #f8f9ff;
        margin: 1rem 0;
    }
    .person-card {
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🔍 Missing Persons Recognition System</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Public Safety Facial Recognition for Identifying Missing Persons</p>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose a page", ["Search", "Add Missing Person", "View All"])

# Search Page
if page == "Search":
    st.header("Search for a Person")
    st.write("Upload a photo to search against the missing persons database")
    
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['png', 'jpg', 'jpeg', 'gif', 'webp'],
        help="Upload a clear photo with a visible face"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        if st.button("🔍 Search Database", type="primary"):
            with st.spinner("Analyzing face and searching database..."):
                # Save uploaded file temporarily
                os.makedirs('uploads', exist_ok=True)
                temp_path = os.path.join('uploads', f'temp_{uploaded_file.name}')
                
                # Save PIL image to file
                image.save(temp_path)
                
                # Encode the face
                encoding = face_service.encode_face(temp_path)
                
                if encoding is None:
                    st.error("❌ No face detected in image. Please upload a clear photo with a visible face.")
                    os.remove(temp_path)
                else:
                    # Search for matches
                    matches = face_service.find_matches(encoding, threshold=0.6)
                    
                    # Clean up temp file
                    os.remove(temp_path)
                    
                    if len(matches) == 0:
                        st.success("✅ No matches found. The person in the photo does not match anyone in the database.")
                    else:
                        st.success(f"✅ Found {len(matches)} match(es):")
                        
                        for match in matches:
                            person = get_missing_person_by_id(match['person_id'])
                            if person:
                                confidence = round(match['confidence'] * 100, 2)
                                
                                # Determine confidence color
                                if confidence >= 80:
                                    conf_color = "🟢"
                                elif confidence >= 60:
                                    conf_color = "🟡"
                                else:
                                    conf_color = "🟠"
                                
                                with st.container():
                                    st.markdown(f"""
                                    <div class="match-card">
                                        <h3>{person['name']} {conf_color} {confidence}% match</h3>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    col1, col2 = st.columns(2)
                                    
                                    with col1:
                                        if person['age']:
                                            st.write(f"**Age:** {person['age']}")
                                        if person['description']:
                                            st.write(f"**Description:** {person['description']}")
                                    
                                    with col2:
                                        if person['date_missing']:
                                            st.write(f"**Missing since:** {person['date_missing']}")
                                        if person['contact']:
                                            st.write(f"**Contact:** {person['contact']}")
                                    
                                    st.divider()

# Add Missing Person Page
elif page == "Add Missing Person":
    st.header("Add Missing Person")
    st.write("Add a new missing person to the database")
    
    with st.form("add_person_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name *", help="Full name of the missing person")
            age = st.text_input("Age", help="e.g., 15, 25-30")
            date_missing = st.date_input("Date Missing")
        
        with col2:
            contact = st.text_input("Contact Information", help="Phone number or email for reporting")
            description = st.text_area("Description", help="Physical description, clothing, last seen location, etc.")
        
        photo = st.file_uploader(
            "Upload Photo *",
            type=['png', 'jpg', 'jpeg', 'gif', 'webp'],
            help="Upload a clear photo of the person's face"
        )
        
        if photo:
            image = Image.open(photo)
            st.image(image, caption="Preview", width=300)
        
        submitted = st.form_submit_button("➕ Add to Database", type="primary")
        
        if submitted:
            if not name:
                st.error("❌ Name is required")
            elif not photo:
                st.error("❌ Photo is required")
            else:
                with st.spinner("Processing image and adding to database..."):
                    # Save uploaded file
                    os.makedirs('uploads', exist_ok=True)
                    filepath = os.path.join('uploads', photo.name)
                    
                    # Save PIL image to file
                    image = Image.open(photo)
                    image.save(filepath)
                    
                    # Process face encoding
                    encoding = face_service.encode_face(filepath)
                    
                    if encoding is None:
                        st.error("❌ No face detected in image. Please upload a clear photo with a visible face.")
                        os.remove(filepath)
                    else:
                        # Add to database
                        person_id = add_missing_person(
                            name=name,
                            age=age if age else None,
                            description=description if description else None,
                            date_missing=str(date_missing) if date_missing else None,
                            contact=contact if contact else None,
                            photo_path=filepath,
                            face_encoding=encoding
                        )
                        
                        st.success(f"✅ Missing person added successfully! (ID: {person_id})")
                        st.balloons()

# View All Page
elif page == "View All":
    st.header("All Missing Persons")
    st.write("View all persons in the database")
    
    persons = get_all_missing_persons()
    
    if len(persons) == 0:
        st.info("ℹ️ No missing persons in database yet.")
    else:
        st.write(f"**Total:** {len(persons)} person(s)")
        
        # Display in a grid
        cols = st.columns(3)
        
        for idx, person in enumerate(persons):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="person-card">
                    <h4>{person['name']}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                if person['age']:
                    st.write(f"**Age:** {person['age']}")
                if person['description']:
                    st.write(f"**Description:** {person['description']}")
                if person['date_missing']:
                    st.write(f"**Missing since:** {person['date_missing']}")
                if person['contact']:
                    st.write(f"**Contact:** {person['contact']}")
                
                # Display photo if available
                if person['photo_path'] and os.path.exists(person['photo_path']):
                    try:
                        photo_img = Image.open(person['photo_path'])
                        st.image(photo_img, use_container_width=True)
                    except:
                        st.write("Photo unavailable")
                
                st.divider()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "This application is designed for public safety purposes "
    "to help identify missing persons, particularly children."
)

