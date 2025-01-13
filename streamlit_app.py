import streamlit as st

# import 
import os
import urllib.parse as parser

import streamlit as st

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

import google.generativeai as genai

#-----------------------------



transcript = {}
formatter = TextFormatter()

st.header(":books: Youtube Notes Taker")
video_link = st.text_input("Insert video link")


if st.button("Get transcript"):
    url_data = parser.urlparse(video_link)
    query = parser.parse_qs(url_data.query)

    # Handle normal YouTube video links (e.g., https://www.youtube.com/watch?v=bQnrsK9tEUI)
    if "v" in query:
        video_id = query["v"][0]
    else:
        # Handle YouTube short and live links (e.g., https://youtu.be/bQnrsK9tEUI or /live)
        path_parts = url_data.path.split("/")
        if "live" in path_parts or "shorts" in path_parts:
            video_id = path_parts[-1]
        else:
            st.error("Invalid YouTube link")
            st.stop()

    try:
        # Recupero trascrizione (in inglese o italiano)
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en", "it"])
        text_formatted = formatter.format_transcript(transcript)

        # Salvataggio nello stato della sessione
        st.session_state['text_formatted'] = text_formatted

        st.success("Transcript retrieved successfully!")

    except Exception as e:
        st.error(f"Error retrieving transcript: {e}")


# Checkbox per mostrare il transcript
if "text_formatted" in st.session_state:
    if st.checkbox("Show Transcript"):
        st.text_area("Transcript", st.session_state['text_formatted'], height=300)

#genai.configure(api_key = st.secrets["api_key"])
genai.configure(api_key = "AIzaSyAFq4p_PxK9F0X7uu0GILhvO53MAd5FJpY")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
  system_instruction="Agisci come mio note taker. Ti darò una trascrizione di un video youtube e dovrai fornirmi il riassuno utilizzando un elenco puntato. Includi i dettagli importanti per capire il concetto",
)
if 'response' not in st.session_state:
  st.session_state['response'] = ""

if st.button("Sum It Up"):
  
  response = model.generate_content(st.session_state.text_formatted)
  
  
  st.session_state['response'] = response


  st.markdown(st.session_state['response'].text)

if st.session_state['response']:
  st.download_button("Download the Summary", st.session_state['response'].text, file_name="summary.txt", mime="text/plain")

