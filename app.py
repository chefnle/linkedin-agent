import streamlit as st
import os
from anthropic import Anthropic
from openai import OpenAI
from agent import generate_comment, generate_post, schedule_post_to_buffer, save_idea, get_ideas

# Custom CSS for a beautiful theme
st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
    }
    h1 {
        color: #0052cc !important;
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

st.title('LinkedIn Agent 🎯')

if 'comment_draft' not in st.session_state:
    st.session_state.comment_draft = ""

if 'post_draft' not in st.session_state:
    st.session_state.post_draft = ""

if 'image_prompt' not in st.session_state:
    st.session_state.image_prompt = ""

if 'image_path' not in st.session_state:
    st.session_state.image_path = ""

if 'topic' not in st.session_state: st.session_state.topic = ""

topic = st.text_input('Enter a topic:', value=st.session_state.topic)

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

                    st.write('---')

buffer_option = st.radio('Buffer Action:', ['Schedule to Queue', 'Save as Draft'])

if st.button('Send to Buffer'):
    save_to_draft = (buffer_option == 'Save as Draft')

    with st.spinner('Sending...'):
        result = schedule_post_to_buffer(st.session_state.post_draft, save_to_draft)

        if 'errors' in result:
            st.error(f'Error: {result["errors"]}')
        elif 'data' in result and result['data'].get('createPost', {}).get('message'):
            st.error(f'Buffer Error: {result["data"]["createPost"]["message"]}')
        else:
            st.success('Success!')

with st.sidebar:
    st.header("Content Ideas 💡")
    new_idea = st.text_input("Save an idea:", key="new_idea_input")
    if st.button("Save Idea"):
        if new_idea:
            save_idea(new_idea)
            st.success("Idea saved!")
            st.rerun()

saved_ideas = get_ideas()

if saved_ideas:
    st.write('---')
    st.write('Select a saved idea:')

    for idx, idea in enumerate(saved_ideas):
        if st.button(idea, key=f"idea_{idx}"):
            st.session_state.topic = idea
            st.rerun()       