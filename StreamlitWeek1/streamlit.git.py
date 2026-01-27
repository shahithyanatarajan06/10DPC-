import streamlit as st
import random
from openai import OpenAI

# =========================================================
# Load OpenAI API key from secrets
# =========================================================
if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ OpenAI API key not found in secrets.toml")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# =========================================================
# Page configuration
# =========================================================
st.set_page_config(
    page_title="🌈 Magical Story Bot",
    page_icon="📚",
    layout="centered"
)

# =========================================================
# Colorful Kid-Friendly CSS
# =========================================================
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #ffecd2, #fcb69f);
    }
    h1 {
        color: #ff4b4b;
        text-align: center;
        font-family: "Comic Sans MS", cursive;
    }
    h2, h3 {
        color: #ff6f61;
        font-family: "Comic Sans MS", cursive;
    }
    .stChatMessage {
        border-radius: 20px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .stChatMessage.user {
        background-color: #cce7ff;
    }
    .stChatMessage.assistant {
        background-color: #e8ffe8;
    }
    button {
        background-color: #ff6f61 !important;
        color: white !important;
        border-radius: 14px !important;
        font-size: 16px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# App Title
# =========================================================
st.title("📚✨ Magical Story Bot for Kids")
st.write("Create fun, safe, and colorful stories just for you! 🌈")

# =========================================================
# System Prompt (Kids Safety)
# =========================================================
SYSTEM_PROMPT = """
You are a storytelling assistant for children aged 6–10.

Rules:
- Stories must be safe, friendly, and positive
- No violence, fear, death, romance, or adult themes
- Use simple words and playful imagination
- Always include a positive moral or lesson
- Keep stories under 300 words
"""

# =========================================================
# Session State Initialization
# =========================================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# =========================================================
# Story Controls
# =========================================================
st.subheader("🎨 Choose Your Story")

col1, col2, col3 = st.columns(3)

with col1:
    character = st.selectbox(
        "🧸 Character",
        ["Dragon 🐉", "Unicorn 🦄", "Robot 🤖", "Panda 🐼", "Fairy 🧚"]
    )

with col2:
    place = st.selectbox(
        "🌍 Place",
        ["Forest 🌳", "Space 🚀", "Castle 🏰", "Ocean 🌊", "School 🏫"]
    )

with col3:
    mood = st.selectbox(
        "🎭 Mood",
        ["Funny 😂", "Magical ✨", "Adventurous 🧭", "Calm 🌙"]
    )


# =========================================================
# Chat Input
# =========================================================
user_text = st.chat_input("✍️ Type your own story idea or press Enter")

if user_text:
    prompt = user_text
else:
    prompt = f"Create a {mood.lower()} story about a {character} in the {place}."

if user_text:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("✨ Writing your story..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                temperature=0.8,
                max_tokens=500
            )

            story = response.choices[0].message.content
            st.markdown(story)

    st.session_state.messages.append(
        {"role": "assistant", "content": story}
    )

# =========================================================
# Interactive Story Continuation
# =========================================================
if len(st.session_state.messages) > 1:
    st.subheader("🤔 What should happen next?")

    next_step = st.radio(
        "",
        [
            "Make a new friend 🤝",
            "Learn an important lesson 🌟",
            "Go on another adventure 🚀"
        ]
    )

    if st.button("➡️ Continue Story"):
        follow_up = f"Continue the story and let the character {next_step.lower()}."
        st.session_state.messages.append(
            {"role": "user", "content": follow_up}
        )
        st.rerun()

# =========================================================
# Clear Chat Button
# =========================================================
st.divider()
if st.button("🧹 Start a New Story"):
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    st.rerun()
