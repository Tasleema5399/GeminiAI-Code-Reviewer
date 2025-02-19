import streamlit as st
import google.generativeai as genai
from PIL import Image

# Set Streamlit page config with a custom title & icon
st.set_page_config(page_title="AI Code Reviewer", page_icon="🤖", layout="wide")

# Retrieve API Key from Streamlit secrets
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")

# Handle missing API key
if not GOOGLE_API_KEY:
    st.error("⚠️ Google API Key not found! Set it in the .streamlit/secrets.toml file.")
    st.stop()

# Configure Google Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Load and display the AI Code Reviewer image
image_path = "image.png"
try:
    banner_image = Image.open(image_path)
    st.image(banner_image, use_column_width=True)
except Exception as e:
    st.warning(f"⚠️ Could not load image: {str(e)}")

# Apply custom CSS styles
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        color: white;
    }
    .main-title {
        font-size: 42px;
        font-weight: bold;
        text-align: center;
        color: #00c3ff;
        margin-bottom: 10px;
    }
    .sub-title {
        text-align: center;
        font-size: 20px;
        margin-bottom: 20px;
        color: #ff6b6b;
    }
    .stTextArea textarea {
        background-color: #1E1E1E;
        color: #E0E0E0;
        border-radius: 10px;
        font-size: 16px;
    }
    .stButton button {
        background: linear-gradient(90deg, #ff6b6b, #ff8e53);
        color: white;
        border-radius: 10px;
        font-size: 18px;
        padding: 10px;
        transition: 0.3s;
    }
    .stButton button:hover {
        background: linear-gradient(90deg, #ff8e53, #ff6b6b);
    }
    .stMarkdown {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown('<h1 class="main-title">🔍 AI Code Reviewer</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">🚀 Get instant AI-powered feedback on your code</p>', unsafe_allow_html=True)

# Code Input Area
code_input = st.text_area("📌 Paste your Python code here:", height=200, placeholder="Write or paste your code...")

# Review Button
if st.button("🚀 Review Code"):
    if code_input.strip():
        st.info("🤖 AI is reviewing your code... Please wait ⏳")

        # AI Prompt for analysis
        prompt = f"""
        Review the following Python code:
        1. Identify syntax errors, logical errors, and inefficiencies.
        2. Suggest security improvements.
        3. Optimize for performance and best practices.
        4. Provide a corrected and improved version.
        
        ```python
        {code_input}
        ```
        """

        try:
            # Get AI response
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            feedback = response.text  # Extract AI's feedback

            # Display AI Response with styling
            st.subheader("🔍 AI Feedback & Fixes")
            st.markdown(f'<div class="stMarkdown">{feedback}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

    else:
        st.warning("⚠️ Please enter some Python code before reviewing.")

# Footer
st.markdown("---")
st.write("📌 Developed with ❤️ using Google Gemini & Streamlit")
