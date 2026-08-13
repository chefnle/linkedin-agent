import streamlit as st
import os
from anthropic import Anthropic
from openai import OpenAI
from agent import (
    generate_comment,
    generate_post,
    refine_draft,
    refine_image_prompt,
    generate_post_image,
    schedule_post_to_buffer,
    save_idea,
    get_ideas,
    delete_idea,
)

# --- Page styling ---------------------------------------------------------

st.markdown(
    """
    <style>
    .stApp { background-color: #ffffff; }
    h1 { color: #0052cc !important; font-family: 'Helvetica Neue', sans-serif; }
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
    """,
    unsafe_allow_html=True,
)

st.title('LinkedIn Agent 🎯')

# --- Session state defaults ------------------------------------------------

default_session_state = {
    "comment_draft": "",
    "post_draft": "",
    "image_prompt": "",
    "image_path": "",
    "topic": "",
}

for key, default_value in default_session_state.items():
    if key not in st.session_state:
        st.session_state[key] = default_value

# --- Shared API clients ------------------------------------------------

anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")
openai_api_key = os.environ.get("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

client = Anthropic(api_key=anthropic_api_key)
openai_client = OpenAI(api_key=openai_api_key)

# --- Topic input ------------------------------------------------

topic = st.text_input('Enter a topic:', value=st.session_state.topic)
st.session_state.topic = topic

col1, col2 = st.columns(2)

# --- Column 1: Comment flow ------------------------------------------------

with col1:
    if st.button('Draft Comment'):
        with st.spinner('Drafting comment...'):
            st.session_state.comment_draft = generate_comment(client, topic)

    if st.session_state.comment_draft:
        st.text_area('Comment Draft:', value=st.session_state.comment_draft, height=150, key='comment_display')
        comment_feedback = st.text_input('Type feedback to revise comment:', key='comment_fb')

        if st.button('Revise Comment'):
            with st.spinner('Revising comment...'):
                st.session_state.comment_draft = refine_draft(
                    client, st.session_state.comment_draft, comment_feedback, is_comment=True
                )
                st.rerun()

# --- Column 2: Post + image flow ------------------------------------------------

with col2:
    if st.button('Draft Post'):
        with st.spinner('Drafting post and generating image...'):
            post_text, image_prompt, saved_image_path = generate_post(client, openai_client, topic)
            st.session_state.post_draft = post_text
            st.session_state.image_prompt = image_prompt
            st.session_state.image_path = saved_image_path

    if st.session_state.post_draft:
        st.text_area('Post Draft:', value=st.session_state.post_draft, height=250, key='post_display')

        post_feedback = st.text_input('Type feedback to revise post text:', key='post_fb')
        if st.button('Revise Post Text'):
            with st.spinner('Revising post...'):
                st.session_state.post_draft = refine_draft(
                    client, st.session_state.post_draft, post_feedback, is_comment=False
                )
                st.rerun()

        if st.session_state.image_path and os.path.exists(st.session_state.image_path):
            st.image(st.session_state.image_path, caption="AI-Generated Image")

            image_feedback = st.text_input('Type feedback to revise image:', key='image_fb')
            if st.button('Revise Image'):
                with st.spinner('Revising image...'):
                    st.session_state.image_prompt = refine_image_prompt(
                        client, st.session_state.post_draft, st.session_state.image_prompt, image_feedback
                    )
                    st.session_state.image_path = generate_post_image(
                        openai_client, st.session_state.image_prompt
                    )
                    st.rerun()

# --- Send to Buffer ------------------------------------------------

if st.session_state.post_draft:
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

# --- Sidebar: saved content ideas ------------------------------------------------

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
        st.write('Select or delete a saved idea:')

        for idx, idea in enumerate(saved_ideas):
            col_select, col_delete = st.columns([4, 1])
            with col_select:
                if st.button(idea, key=f"idea_{idx}"):
                    st.session_state.topic = idea
                    st.rerun()
            with col_delete:
                if st.button("🗑️", key=f"del_{idx}"):
                    delete_idea(idea)
                    st.rerun()

