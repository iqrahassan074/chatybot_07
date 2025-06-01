import streamlit as st
from datetime import datetime
import time

st.set_page_config(
    page_title="🤖 ChatyBot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="auto",
)

with st.sidebar:
    st.title("Settings ⚙️")

    if "personality" not in st.session_state:
        st.session_state.personality = "Friendly 🤗"
    personality = st.selectbox("Choose ChatyBot's Personality", ["Friendly 🤗", "Formal 🧐", "Funny 😂"])
    st.session_state.personality = personality


    if st.button("🧹 Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    if st.session_state.get("messages"):
        export_text = "\n".join([f"{msg['role'].capitalize()} ({msg['time']}): {msg['content']}" for msg in st.session_state.messages])
        st.download_button("⬇️ Export Chat History", export_text, file_name="chat_history.txt", mime="text/plain")


css = """
@import url('https://fonts.googleapis.com/css2?family=Inter&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap');

:root {
    --bg-color: #d2b48c;
    --text-color: #3e2f1c;
    --user-bubble-bg: linear-gradient(135deg, #8b5cf6, #f472b6);
    --bot-bubble-bg: #fdf6e3;
    --button-bg: #6b4226;
    --button-text: #fff;
    --input-bg: #fffaf0;
    --input-text: #3e2f1c;
    --scrollbar-track: #ecdcc6;
    --scrollbar-thumb: #b08968;
}

body, .stApp {
    background: var(--bg-color);
    color: var(--text-color);
    font-family: 'Inter', sans-serif;
}

.chat-container {
    max-height: 500px;
    overflow-y: auto;
    padding: 15px 25px;
    border-radius: 18px;
    background: #fdf6e3;
    box-shadow: 0 10px 30px rgb(59 130 246 / 0.15);
    margin-bottom: 18px;
}

.user-bubble, .bot-bubble {
    padding: 14px 20px;
    border-radius: 22px;
    font-size: 16px;
    line-height: 1.5;
    max-width: 70%;
    margin: 10px 0;
    word-wrap: break-word;
    box-shadow: 0 4px 12px rgb(59 130 246 / 0.1);
}

.user-bubble {
    background: var(--user-bubble-bg);
    color: var(--button-text);
    margin-left: auto;
    border-bottom-right-radius: 6px;
    text-align: right;
    box-shadow: 0 6px 18px rgb(14 165 233 / 0.5);
}

.bot-bubble {
    background: var(--bot-bubble-bg);
    color: var(--text-color);
    margin-right: auto;
    border-bottom-left-radius: 6px;
    text-align: left;
    box-shadow: 0 6px 18px rgb(134 25 143 / 0.3);
}

.timestamp {
    font-size: 12px;
    color: #5b4636;
    margin-top: 4px;
}

.footer {
    text-align: center;
    margin-top: 48px;
    font-family: 'Great Vibes', cursive;
    font-weight: 400;
    letter-spacing: 0.04em;
    font-size: 24px;
    color: var(--text-color);
}

.footer span.name {
    font-weight: 700;
    font-size: 28px;
    letter-spacing: 0.06em;
}

.typing-indicator {
    font-style: italic;
    color: #6b4c3b;
    margin: 10px 0 16px 0;
    font-size: 15px;
}

.chat-container::-webkit-scrollbar {
    width: 9px;
}

.chat-container::-webkit-scrollbar-track {
    background: var(--scrollbar-track);
    border-radius: 20px;
}

.chat-container::-webkit-scrollbar-thumb {
    background: var(--scrollbar-thumb);
    border-radius: 20px;
}
"""

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

def current_time():
    return datetime.now().strftime("%H:%M")

qa_pairs = {
    "hello": "Hi there! 👋 How can I help you today?",
    "how are you": "I'm just Python code, but I'm feeling great! 😄",
    "what is your name": "You can call me ChatyBot 🤖",
    "who made you": "I was created using Streamlit with love! 💻✨",
    "what is python": "🐍 Python is a popular programming language known for simplicity and power.",
    "tell me a joke": "Why did the programmer quit his job? Because he didn't get arrays! 😂",
    "bye": "Goodbye! 👋 Have a great day!",
    "thank you": "You're welcome! 😊",
    "what can you do": "I can answer questions and brighten your day with emojis! 🌟",
    "what is ai": "AI stands for Artificial Intelligence 🤖 — machines that can learn and think!",
    "what is streamlit": "Streamlit is a Python framework for building beautiful web apps easily! 🚀",
    "who are you": "I'm ChatyBot 🤖, your friendly Q&A assistant!",
    "what's your purpose": "To chat, help, and sprinkle some emoji magic! ✨",
}

st.markdown(
    "<h1 style='text-align: center; margin-bottom: 15px; color:#5b4226;'>🤖 Chat with ChatyBot </h1>",
    unsafe_allow_html=True,
)

st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    bubble_class = "user-bubble" if msg["role"] == "user" else "bot-bubble"
    st.markdown(
        f"""
        <div style="position: relative;">
            <div class="{bubble_class}" title="Sent at {msg.get('time', '')}">
                {msg['content']}
            </div>
            <div class="timestamp">{msg.get('time', '')}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.get("typing", False):
    st.markdown('<div class="typing-indicator">ChatyBot is typing...</div>', unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([8, 1])
    user_input = col1.text_input(
        "Type your message...", placeholder="Ask me anything...", label_visibility="collapsed"
    )
    submit = col2.form_submit_button("Send")

if submit and user_input.strip():
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "time": current_time(),
    })
    st.session_state["typing"] = True
    st.rerun()

    time.sleep(0.7)

    reply = "🤔 I'm not sure how to answer that. Try asking something else!"
    for question, answer in qa_pairs.items():
        if question in user_input.lower():
            base_reply = answer
            if st.session_state.personality == "Friendly 🤗":
                reply = f"{base_reply} Let me know if there's more I can do! 😊"
            elif st.session_state.personality == "Formal 🧐":
                reply = f"{base_reply} Please feel free to continue our discussion."
            elif st.session_state.personality == "Funny 😂":
                reply = f"{base_reply} LOL! I crack myself up sometimes. 🤣"
            break

    st.session_state.messages.append({
        "role": "bot",
        "content": reply,
        "time": current_time(),
    })
    st.session_state["typing"] = False
    st.rerun()

st.markdown(
    f'<div class="footer">Made by <span class="name">Iqra Hassan</span> 💖</div>',
    unsafe_allow_html=True,
)
