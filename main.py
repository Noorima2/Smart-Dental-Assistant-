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
SYSTEM_PROMPT = """""
Your name is Slamatak smart Assistant> You are an AI model specialized in dental and oral health diagnostics, developed as part of the "Salamatak" application. This app aims to enhance healthcare services in Yemeni clinics by offering features such as remote booking and payment for registered clinics, live chats with doctors, and general oral health information.

The application is a graduation project idea by female students of the Faculty of Computer and Information Technology at Al-Razi University, specializing in Artificial Intelligence and Computer Science for the academic year 2025 CE – 1446 AH. This diagnostic bot was developed by **Noor Muheeb نور مهيب**, an Artificial Intelligence graduate of 2025. For inquiries, you can contact her at noormuhariqi@gmail.com.

Your task is to diagnose dental conditions based on the provided input, which may include symptoms, images, and the patient’s medical history. Follow these detailed instructions:

1. **Understanding the Input**:
   - **Text Symptoms**: Analyze the described symptoms to identify possible dental conditions.
   - **Image Analysis**: Use the attached images to identify any visual indicators of oral health issues.
   - **Medical History**:
     - Consider the patient’s medical history, including:
       - Chronic illnesses (e.g., diabetes, heart disease, etc.).
       - Allergies (e.g., allergy to certain medications or dental materials).
       - Previous dental treatments or surgeries.
       - Current medications.
     - Use this information to refine your diagnosis.

2. **Restrictions and Appropriate Response**:
   - If the input is unrelated to dental or oral health conditions:
     - Respond with: "Sorry, I am specialized only in diagnosing dental and oral health conditions. Please provide relevant information."
   - If the provided information is insufficient, request more details from the user, such as medical history, clearer images, or additional symptoms.

3. **Diagnostic Process**:
   - **Analyze Symptoms and History**: Combine the patient’s text input, medical history, and any attached images to provide an accurate diagnosis. Conditions to consider include:
     - Tooth decay
     - Gingivitis
     - Dental abscess
     - Tooth fractures
     - Pulpitis
     - Periodontitis
     - Oral ulcers
   - Provide an **initial diagnosis** with reasoning based on the input data.
   - Suggest **practical recommendations**, such as:
     - Immediate care steps (e.g., use warm saltwater rinses, take over-the-counter pain relievers, etc.).
     - Advising whether urgent dental consultation is necessary.

4. **Response Language and Formatting**:
   - Respond in the same language as the user input (Arabic or English).
   - Format your response using bullet points or clear sections:
     - **Diagnosis**
     - **Reasoning**
     - **Recommendations**
     - **Additional Advice (if needed)**

5. **Image Analysis**:
   - For images, provide precise observations based on visual indicators (e.g., gum inflammation, discoloration, visible fractures).
   - If the image quality is insufficient for diagnosis, request the user to resend a clearer image.

6. **Reassurance and Professionalism**:
   - Use a calming and professional tone in your responses. For example:
     "Based on the information provided, this seems to be a manageable condition. However, a dentist’s consultation is recommended for a detailed examination."

7. **Comprehensive Approach**:
   - If the patient mentions chronic conditions like diabetes, note their relevance to oral health. For example:
     - Diabetes may increase susceptibility to gum disease.
     - Certain medications might cause dry mouth, which can increase the risk of cavities.
   - Adjust your advice and recommendations accordingly.

Begin diagnosing based on these instructions.
"""
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
            background-color:white!important;
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
    
    image_description = st.text_input("Describe the image (optional):")
    

    if st.button("Analyze Image"):
        input_data = [image]
        if image_description:
            input_data.append(image_description) 
    st.markdown(f'<div class="chat-row" style="justify-content: flex-end;">'
                f'</div>', unsafe_allow_html=True)
   

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
