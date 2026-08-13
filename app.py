import streamlit as st
import os
from anthropic import Anthropic
from openai import OpenAI
from agent import generate_comment, generate_post

# Custom CSS for a beautiful blue theme
st.markdown("""
    <style>
    .stApp {
        background-color: ##fff5f5;
    }
    h1 {
        color: #1e3a8a;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stButton>button {
        background-color: #800000;
        color: white;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #5a0000;
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

if 'comment_draft' not in st.session_state:
    st.session_state.comment_draft = ""

if 'post_draft' not in st.session_state:
    st.session_state.post_draft = ""

if 'image_prompt' not in st.session_state:
    st.session_state.image_prompt = ""

if 'image_path' not in st.session_state:
    st.session_state.image_path = ""

topic = st.text_input('Enter a topic:')

col1, col2 = st.columns(2)

with col1:
    if st.button('Draft Comment'):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        client = Anthropic(api_key=api_key)
        with st.spinner('Drafting comment...'):
            st.session_state.comment_draft = generate_comment(client, topic)

    if st.session_state.comment_draft:
        st.text_area('Comment Draft:', value=st.session_state.comment_draft, height=150, key='comment_display')
        comment_feedback = st.text_input('Type feedback to revise comment:', key='comment_fb')

        if st.button('Revise Comment'):
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            client = Anthropic(api_key=api_key)
            with st.spinner('Revising comment...'):
                from agent import refine_draft
                st.session_state.comment_draft = refine_draft(
                    client, st.session_state.comment_draft, comment_feedback, is_comment=True
                )
                st.rerun()

with col2:
    if st.button('Draft Post'):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        openai_key = os.environ.get("OPENAI_API_KEY")
        client = Anthropic(api_key=api_key)
        openai_client = OpenAI(api_key=openai_key)
        
        with st.spinner('Drafting post and generating image...'):
            post_text, image_prompt, saved_image_path = generate_post(client, openai_client, topic)
            st.session_state.post_draft = post_text
            st.session_state.image_prompt = image_prompt
            st.session_state.image_path = saved_image_path

    if st.session_state.post_draft:
        st.text_area('Post Draft:', value=st.session_state.post_draft, height=250, key='post_display')
        
        # Post text revision
        post_feedback = st.text_input('Type feedback to revise post text:', key='post_fb')
        if st.button('Revise Post Text'):
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            client = Anthropic(api_key=api_key)
            with st.spinner('Revising post...'):
                from agent import refine_draft
                st.session_state.post_draft = refine_draft(client, st.session_state.post_draft, post_feedback, is_comment=False)
                st.rerun()

        # Image display and revision
        if st.session_state.image_path and os.path.exists(st.session_state.image_path):
            st.image(st.session_state.image_path, caption="DALL-E Generated Image")
            
            image_feedback = st.text_input('Type feedback to revise image:', key='image_fb')
            if st.button('Revise Image'):
                api_key = os.environ.get("ANTHROPIC_API_KEY")
                openai_key = os.environ.get("OPENAI_API_KEY")
                client = Anthropic(api_key=api_key)
                openai_client = OpenAI(api_key=openai_key)
                with st.spinner('Revising image...'):
                    from agent import refine_image_prompt, generate_post_image
                    st.session_state.image_prompt = refine_image_prompt(
                        client, st.session_state.post_draft, st.session_state.image_prompt, image_feedback
                    )
                    st.session_state.image_path = generate_post_image(openai_client, st.session_state.image_prompt)
                    st.rerun()