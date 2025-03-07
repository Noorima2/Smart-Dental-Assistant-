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
    layout="wide",  
)

# Set up Google Gemini-Pro AI model
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
gen_ai.configure(api_key=GOOGLE_API_KEY)

model = gen_ai.GenerativeModel('gemini-2.0-flash')

# Define a system prompt for guiding the AI responses
SYSTEM_PROMPT= os.getenv("SYSTEM_PROMPT")
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

# Display the chatbot's description on the page
with st.expander("💡 How to Use this Bot"):
    st.markdown(
        """
     Enter Your Symptoms: 
        Describe your symptoms in detail, such as "I feel pain in my molar when eating" or "I have gum bleeding".\n
                 إدخال الأعراض: اكتب وصفًا لحالتك الصحية الفموية
     Upload an Image (Optional) 📸: 
        If you want the bot to analyze a picture of your teeth or gums, you can upload a clear image.The bot will examine the image and provide observations about your condition.\n
                    رفع صورة (اختياري) : يمكنك رفع صورة واضحة للأسنان أو اللثة
     Receive Diagnosis & Recommendations 🩺:
        After submitting your details, the bot will analyze them and provide a preliminary diagnosis, along with immediate care advice and whether you should visit a dentist.\n
                    تلقي التشخيص والنصائح : سيقدم لك البوت تشخيصًا مبدئيًا ونصائح للعناية
     💡 Tip: If you have any special medical conditions, mention them in your message for a more accurate diagnosis.\n
                   نصيحة:إذا كانت لديك حالة طبية خاصة، يُفضل ذكرها
     👩‍⚕️ Note: This bot provides guidance only and does not replace a professional dental consultation.\n
                 ملاحظة:هذا البوت يقدم نصائح استرشادية فقط ولا يُغني عن استشارة الطبيب
    """, unsafe_allow_html=True

    )

# Custom CSS for improved chat alignment
st.markdown(
    """
    <style>
        .main {
            background-color:!important;
        }
        .chat-container {
            border-color: #0077B6 !important;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .stChatMessage {
            padding: 10px;
            margin: 8px 0;
            border-radius: 10px;
            max-width: 75%; 
        }
        .stChatMessage div {
            font-size: 16px;
            line-height: 1.5;
        }
        .stChatMessage[data-testid="stMessage-user"] {
            background-color: #DCF8C6; /* لون مشابه لتطبيقات الدردشة */
            align-self: flex-end;
        }
        .stChatMessage[data-testid="stMessage-bot"] {
            background-color: #F1F0F0;
            align-self: flex-start;
        }
        .chat-row {
            display: flex;
            justify-content: space-between;
            width: 100%;
        }
        .chat-message {
           padding: 10px;
           border-radius: 10px;
           max-width: 80%;
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
                        margin-bottom: 15px !important;

            text-align: left;
        }
        @media screen and (max-width: 600px) {
            .chat-message {
                max-width: 90%;
                font-size: 14px;
            }
        }
        input[type="text"]:focus {
            border-color: #0077B6 !important;
            outline: none !important;
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
