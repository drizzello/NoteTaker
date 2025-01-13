import os
import urllib.parse as parser
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import google.generativeai as genai
from typing import Optional, Dict, List
from dataclasses import dataclass

@dataclass
class VideoInfo:
    video_id: str
    transcript: List[Dict]
    formatted_text: str

class YouTubeTranscriptManager:
    @staticmethod
    def extract_video_id(video_link: str) -> Optional[str]:
        """Extract video ID from various YouTube URL formats."""
        url_data = parser.urlparse(video_link)
        query = parser.parse_qs(url_data.query)
        
        if "v" in query:
            return query["v"][0]
        
        path_parts = url_data.path.split("/")
        if "live" in path_parts or "shorts" in path_parts:
            return path_parts[-1]
        return None

    @staticmethod
    def get_transcript(video_id: str, languages: List[str] = ["en", "it"]) -> VideoInfo:
        """Fetch and format transcript for a given video ID."""
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        formatted_text = TextFormatter().format_transcript(transcript)
        return VideoInfo(video_id, transcript, formatted_text)

class StreamlitUI:
    def __init__(self):
        self.setup_page_config()
        self.setup_styles()
        self.init_session_state()
        self.setup_gemini_ai()

    def setup_page_config(self):
        st.set_page_config(
            page_title="YouTube Notes Taker",
            page_icon="📚",
            layout="centered"
        )

    def setup_styles(self):
        st.markdown("""
            <style>
            .main { padding: 2rem; max-width: 1200px; margin: 0 auto; }
            .stButton button {
                width: 100%;
                border-radius: 4px;
                padding: 0.5rem 1rem;
                background-color: #FF0000;
                color: white;
                border: none;
                margin-top: 1rem;
            }
            .stButton button:hover { background-color: #CC0000; }
            .message { 
                padding: 1rem;
                border-radius: 4px;
                margin: 1rem 0;
            }
            .success-message {
                background-color: #E8F5E9;
                border: 1px solid #4CAF50;
            }
            .error-message {
                background-color: #FFEBEE;
                border: 1px solid #EF5350;
            }
            </style>
        """, unsafe_allow_html=True)

    def init_session_state(self):
        for key in ['summarize', 'response', 'text_formatted', 'transcript_ready']:
            if key not in st.session_state:
                st.session_state[key] = False if key != 'response' else ""

    def setup_gemini_ai(self):
        genai.configure(api_key="AIzaSyAFq4p_PxK9F0X7uu0GILhvO53MAd5FJpY")
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config={
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            },
            system_instruction="""
                Act as a professional note-taking assistant. Analyze the YouTube video transcript and provide:
                1. A concise summary of main points
                2. Key concepts and ideas
                3. Important details and relevant examples
                4. Main conclusions and takeaways
                Present the result in a clear, organized manner using bullet points and readable structure.
            """
        )

    def render_header(self):
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("# 📚")
        with col2:
            st.markdown("""
                <h1 style='margin-bottom: 0;'>YouTube Notes Taker</h1>
                <p style='color: #666; margin-top: 0;'>Transform video content into organized notes</p>
            """, unsafe_allow_html=True)

    def process_video(self, video_link: str):
        try:
            video_id = YouTubeTranscriptManager.extract_video_id(video_link)
            if not video_id:
                st.error("❌ Invalid YouTube link")
                return

            video_info = YouTubeTranscriptManager.get_transcript(video_id)
            st.session_state.update({
                'text_formatted': video_info.formatted_text,
                'transcript_ready': True
            })
            st.success("✅ Transcript retrieved successfully!")
            return video_info

        except Exception as e:
            st.error(f"❌ Error retrieving transcript: {str(e)}")
            return None

    def generate_summary(self, text: str):
        try:
            response = self.model.generate_content(text)
            st.session_state['response'] = response
            st.success("✨ Summary generated successfully!")
            
            with st.container():
                st.markdown("### 📋 Summary")
                st.markdown(response.text)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "📥 Download as TXT",
                        response.text,
                        file_name="summary.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
        except Exception as e:
            st.error(f"❌ Error generating summary: {str(e)}")

    def render(self):
        self.render_header()
        
        with st.container():
            st.markdown("### 🎥 Enter Video URL")
            video_link = st.text_input(
                "",
                placeholder="Paste your YouTube video URL here...",
                help="Works with regular YouTube videos, shorts, and live streams"
            )

            if st.button("📝 Get Transcript and Summarize it", use_container_width=True) and video_link:
                with st.spinner("Fetching transcript and summarizing..."):
                    if video_info := self.process_video(video_link):
                        self.generate_summary(video_info.formatted_text)

        st.markdown("""
            <div style='text-align: center; color: #666; padding: 2rem 0;'>
                <p>Made with ❤️ by Your Company Name</p>
            </div>
        """, unsafe_allow_html=True)

def main():
    app = StreamlitUI()
    app.render()

if __name__ == "__main__":
    main()



#    genai.configure(api_key="AIzaSyAFq4p_PxK9F0X7uu0GILhvO53MAd5FJpY")
