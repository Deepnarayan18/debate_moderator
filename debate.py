import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# UI Setup
st.set_page_config(page_title="🤝 AI Debate Moderator", layout="wide")
st.title("🤝 AI Debate Moderator")
st.subheader("Argue your case, and let AI keep it fair!")

# Sidebar Settings
st.sidebar.header("Debate Settings")
topic = st.sidebar.text_input("Debate Topic", "Should AI replace teachers?")
tone = st.sidebar.selectbox("Moderator Tone", ["Neutral", "Sarcastic", "Encouraging"])

# Function to moderate debate
def moderate_debate(topic, argument, tone):
    prompt = f"As a {tone.lower()} debate moderator for the topic '{topic}', evaluate this argument: '{argument}'. Check its logic, coherence, and relevance. Provide a score (1-10) and a brief comment."
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_tokens=10000,
            stream=False
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"⚠️ Groq Error: {str(e)}")
        return None

# Debate Input
st.write(f"Debate Topic: {topic}")
argument = st.text_area("Your Argument", "Enter your stance here...")
if st.button("Submit Argument"):
    if argument:
        moderation = moderate_debate(topic, argument, tone)
        if moderation:
            st.markdown(f"### AI Moderator Says:\n{moderation}")
    else:
        st.warning("⚠️ Enter an argument!")

st.sidebar.markdown("<p style='text-align: center; color: #AAB7B8;'>🔮 Powered by Groq AI</p>", unsafe_allow_html=True)