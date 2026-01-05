import streamlit as st
import google.generativeai as genai
import time

# This looks for your secret API key safely
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Please add your API Key to the Streamlit Secrets.")

model = genai.GenerativeModel('gemini-2.0-flash')

st.title("📚 One-Click eBook Creator")
st.info("Follow the phases below to generate your 80,000-word book.")

# Phase 1: Topic
topic = st.text_input("What is your book about?", "The History of Space Travel")

if st.button("Step 1: Generate Book Roadmap"):
    with st.spinner("Creating 20-chapter outline..."):
        prompt = f"Create a detailed 20-chapter roadmap for a book about {topic}. Provide a title for each chapter."
        roadmap = model.generate_content(prompt)
        st.session_state['roadmap'] = roadmap.text
        st.success("Roadmap Created!")

if 'roadmap' in st.session_state:
    st.text_area("Your Roadmap", st.session_state['roadmap'], height=200)
    
    if st.button("Step 2: Start Auto-Pilot Writing"):
        st.write("🚀 Starting the writing process. This will take a while. Please keep this tab open.")
        full_book = ""
        progress_bar = st.progress(0)
        
        # We simulate writing 20 chapters
        for i in range(1, 21):
            with st.status(f"Writing Chapter {i}...", expanded=False):
                chapter_prompt = f"Write a deep-dive 4,000 word chapter for Chapter {i} of this roadmap: {st.session_state['roadmap']}. Use professional tone."
                chunk = model.generate_content(chapter_prompt)
                full_book += f"\n\n# Chapter {i}\n\n" + chunk.text
            progress_bar.progress(i / 20)
        
        st.success("✅ Book Complete!")
        st.download_button("Download Manuscript", full_book, file_name="ebook.md")
