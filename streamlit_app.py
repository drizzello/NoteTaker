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

#video_id = video_link.split("=")[1]
#st.write(video_id)

if st.button("Get transcript"):
  url_data = parser.urlparse(video_link)
  query = parser.parse_qs(url_data.query)
  video = query["v"][0]
  transcript = YouTubeTranscriptApi.get_transcript(video, languages=("en", "it"))
  text_formatted = formatter.format_transcript(transcript)

  # .format_transcript(transcript) turns the transcript into a JSON string.
  # Initialization
  if 'text_formatted' not in st.session_state:
      st.session_state['text_formatted'] = text_formatted
  else:
      st.session_state['text_formatted'] = text_formatted


  st.write(text_formatted)

genai.configure(st.secrets["api_key"])

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

