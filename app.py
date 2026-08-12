import streamlit as st
import os
from anthropic import Anthropic
from openai import OpenAI
from agent import generate_comment, generate_post

# Custom CSS for a beautiful blue theme
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f7ff;
    }
    h1 {
        color: #1e3a8a;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stButton>button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        color: white;
        border: none;
    }
    div[data-baseweb="textarea"] {
        border: 1px solid #bfdbfe;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title('LinkedIn Agent 🚀')

topic = st.text_input('Enter a topic:')

col1, col2 = st.columns(2)

with col1:
    if st.button('Draft Comment'):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        client = Anthropic(api_key=api_key)
        with st.spinner('Drafting comment...'):
            comment = generate_comment(client, topic)
        st.text_area('Comment Draft:', value=comment, height=150)

with col2:
    if st.button('Draft Post'):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        openai_key = os.environ.get("OPENAI_API_KEY")
        client = Anthropic(api_key=api_key)
        openai_client = OpenAI(api_key=openai_key)
        with st.spinner('Drafting post and generating image...'):
            post_text, image_prompt, saved_image_path = generate_post(client, openai_client, topic)
        st.text_area('Post Draft:', value=post_text, height=250)
        if os.path.exists(saved_image_path):
            st.image(saved_image_path, caption="DALL-E Generated Image")