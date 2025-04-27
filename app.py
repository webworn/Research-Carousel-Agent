# AGENT: Deep Research + Visual Carousel Creator with Streamlit UI (Premium Theme and Secure for Streamlit Cloud)

import openai
import requests
import streamlit as st
from streamlit_extras.colored_header import colored_header

# Secure API keys using Streamlit Secrets Manager
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
PERPLEXITY_API_KEY = st.secrets["PERPLEXITY_API_KEY"]

# Set up OpenAI configuration
openai.api_key = OPENAI_API_KEY

# Helper: Use Perplexity or similar to search deeply
def deep_search(topic):
    url = "https://api.perplexity.ai/search"
    headers = {"Authorization": f"Bearer {PERPLEXITY_API_KEY}"}
    params = {"query": topic}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()['summary']
    else:
        research_prompt = f"""
        Research deeply about: {topic}
        Extract key insights in a way that can be shared visually in a carousel format.
        Keep it simple and structured for Instagram-like storytelling.
        """
        gpt_response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": research_prompt}]
        )
        return gpt_response['choices'][0]['message']['content']

# Helper: Generate carousel image
def generate_carousel_slide(slide_text, slide_number):
    dalle_prompt = f"""
    Design a 1:1 aspect ratio Instagram carousel visual.
    Background: light teal/mint green.
    Bold Title: 'Slide {slide_number}'
    Content Text: "{slide_text}"
    Clean modern aesthetic, easy to read.
    """

    dalle_response = openai.Image.create(
        prompt=dalle_prompt,
        n=1,
        size="1024x1024"
    )

    return dalle_response['data'][0]['url']

# Main Agent Function
def research_and_create_carousel(user_input_topic):
    research_summary = deep_search(user_input_topic)
    slides = research_summary.split('\n')
    slides = [slide.strip() for slide in slides if slide.strip()]
    generated_slides = []

    for idx, slide_text in enumerate(slides, start=1):
        slide_image_url = generate_carousel_slide(slide_text, idx)
        generated_slides.append((idx, slide_text, slide_image_url))

    return generated_slides

# Streamlit UI Setup with Premium Theme
st.set_page_config(
    page_title="Deep Research + Carousel Designer",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

colored_header("Deep Research + Visual Carousel Creator", description="✨ Turn ideas into research-driven Instagram visuals", color_name="light-blue-70")

user_topic = st.text_input("Enter a topic or idea:", placeholder="e.g., Benefits of Green Tea for Skin Health")

if st.button("🚀 Generate Carousel") and user_topic:
    with st.spinner("🔎 Researching and designing beautiful slides..."):
        slides = research_and_create_carousel(user_topic)

    st.success("🎉 Done! Here are your carousel slides:")

    for slide in slides:
        with st.container():
            st.subheader(f"📖 Slide {slide[0]}")
            st.write(slide[1])
            st.image(slide[2], caption=f"Slide {slide[0]}", use_column_width=True)

st.markdown("---")
st.caption("🚀 Powered by OpenAI & Perplexity AI | Crafted with ❤️ in Streamlit")
