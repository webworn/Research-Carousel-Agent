# AGENT: Deep Research + Visual Carousel Creator (Corrected Professional Flow)

import openai
import streamlit as st
from streamlit_extras.colored_header import colored_header

# Secure API key using Streamlit Secrets Manager
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Set up OpenAI configuration
openai.api_key = OPENAI_API_KEY

# Helper: Deep research and structured slide creation
def deep_research_and_create_slides(topic, audience_profile, tone_style):
    master_prompt = f"""
    You are a health researcher and Instagram content creator for the brand Cure Naturals.

    Research deeply about: {topic}.
    - Only use credible sources: PubMed, Mayo Clinic, NIH, Healthline.
    - Summarize 3–5 key scientific findings in simple, friendly, motivational language.
    - Lightly cite studies at the end of major points.

    Then structure this into a 9-slide Instagram carousel:
    - Slide 1: Big emotional hook (max 8 words)
    - Slide 2: One clear idea per slide.
    - Slide 3: One clear idea per slide.
    - Slide 4: One clear idea per slide.
    - Slide 5: One clear idea per slide.
    - Slide 6: One clear idea per slide.
    - Slide 7: One clear idea per slide.
    - Slide 8: One clear idea per slide.
    - Slide 9: Positive CTA (e.g., "Share this healing tip 🌱")

    Each slide should have:
    - Title (max 8 words)
    - Body Text (1–2 motivational, educational sentences)

    After each slide, create a DALL-E 3 visual generation prompt:
    Visual Prompt Rules:
    - 1:1 aspect ratio
    - Soft mint green or pastel background
    - Minimalist, flat design
    - Wellness, healing, and positivity vibe
    - Icons or metaphors if appropriate

    Target Audience: {audience_profile}
    Tone Style: {tone_style}

    Output Format:
    Slide 1:
    Title: ""
    Body Text: ""
    DALL-E Prompt: ""
    Slide 2:
    Title: ""
    Body Text: ""
    DALL-E Prompt: ""
    ...(continue till Slide 9)
    """

    gpt_response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": master_prompt}]
    )
    return gpt_response['choices'][0]['message']['content']

# Streamlit UI Setup
st.set_page_config(
    page_title="Cure Naturals Carousel Creator",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed",
)

colored_header("Deep Research + Professional Carousel Generator", description="✨ Create beautiful health carousels from credible research", color_name="green-70")

user_topic = st.text_input("Enter a health topic (e.g., Benefits of Turmeric)")
audience_profile = st.text_input("Describe your audience (e.g., Women 25-45, gut health conscious)")
tone_style = st.selectbox("Choose the tone style", ["Scientific Warm", "Inspirational Motivational", "Myth-Busting Direct"])

if st.button("🚀 Generate Carousel Slides") and user_topic and audience_profile:
    with st.spinner("🔎 Researching and structuring beautiful slides..."):
        full_slides_output = deep_research_and_create_slides(user_topic, audience_profile, tone_style)

    st.success("🎉 Done! Review your slides below:")
    st.markdown(full_slides_output)

st.markdown("---")
st.caption("🚀 Powered by OpenAI | Crafted with ❤️ by Cure Naturals")
