import os
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
import io
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with سلامتك!",
    page_icon=":tooth:", 
    layout="centered",  
)

# Set up Google Gemini-Pro AI model
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
gen_ai.configure(api_key=GOOGLE_API_KEY)

model = gen_ai.GenerativeModel('gemini-2.0-flash')

# Define a system prompt for guiding the AI responses
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")
print(SYSTEM_PROMPT)

# Function to translate roles between Gemini and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    st.session_state.chat_session.send_message(SYSTEM_PROMPT)

# Display the chatbot's title on the page
st.title("🦷 Salamatk - ChatBot")

# Custom CSS for improved chat alignment
st.markdown(

    """
    <style>
        .main {
            background-color:!important;
        }
        .chat-container {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .chat-row {
            display: flex;
            justify-content: space-between;
            width: 100%;
        }
        .chat-message {
            padding: 10px;
            border-radius: 10px;
            max-width: 45%;
            word-wrap: break-word;
            display: inline-block;
        }
        .user-message {
            background-color: #0077B6;
            color: white;
            text-align: right;
        }
        .bot-message {
            background-color: #0077B6;
            color: white;
            text-align: left;
        }
        div.stButton > button {
            background-color: #0077B6 !important;
            color: white !important;
            border-radius: 8px;
            padding: 8px 16px;
            border: none;
            font-size: 16px;
            font-weight: bold;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            background-color: #005f87 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Chat history container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.chat_session.history[1:1]:
    role = translate_role_for_streamlit(message.role)
    css_class = "user-message" if role == "user" else "bot-message"
    position = "flex-end" if role == "user" else "flex-start"
    
    st.markdown(f'<div class="chat-row" style="justify-content: {position};">'
                f'<div class="chat-message {css_class}">{message.parts[0].text}</div>'
                f'</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# File uploader for images
uploaded_file = st.file_uploader("Upload an image for analysis", type=["jpg", "png"])
if uploaded_file:
    image = Image.open(io.BytesIO(uploaded_file.getvalue()))
    st.image(image, width=200, caption="Uploaded Image")
        
    gemini_response = st.session_state.chat_session.send_message([image])
    st.markdown(f'<div class="chat-row" style="justify-content: flex-start;">'
                f'<div class="chat-message bot-message">{gemini_response.text}</div>'
                f'</div>', unsafe_allow_html=True)
    
    uploaded_file = None


# Input field for user's message
user_prompt = st.chat_input("Ask Salamatk...")
if user_prompt:
    st.markdown(f'<div class="chat-row" style="justify-content: flex-end;">'
                f'<div class="chat-message user-message">{user_prompt}</div>'
                f'</div>', unsafe_allow_html=True)
    
    gemini_response = st.session_state.chat_session.send_message(user_prompt)
    
    st.markdown(f'<div class="chat-row" style="justify-content: flex-start;">'
                f'<div class="chat-message bot-message">{gemini_response.text}</div>'
                f'</div>', unsafe_allow_html=True)
