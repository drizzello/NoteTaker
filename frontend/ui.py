# frontend/ui.py
import streamlit as st
from backend.transcript_manager import YouTubeTranscriptManager
from backend.ai_manager import AIManager
from frontend.styles import STYLES

class StreamlitUI:
    def __init__(self):
        self.setup_page_config()
        self.setup_styles()
        self.init_session_state()
        self.ai_manager = AIManager(st.secrets["api_key"])
    def setup_page_config(self):
        st.set_page_config(
            page_title="YouTube Notes Taker",
            page_icon="📚",
            layout="centered"
        )

    def setup_styles(self):
        st.markdown(STYLES, unsafe_allow_html=True)

    def init_session_state(self):
        for key in ['summarize', 'response', 'text_formatted', 'transcript_ready']:
            if key not in st.session_state:
                st.session_state[key] = False if key != 'response' else ""

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
            summary = self.ai_manager.generate_summary(text)
            st.session_state['response'] = summary
            st.success("✨ Summary generated successfully!")
            
            with st.container():
                st.markdown("### 📋 Summary")
                st.markdown(summary)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "📥 Download as TXT",
                        summary,
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
                <p>Made with ❤️ by Your 🐯 Company </p>
            </div>
        """, unsafe_allow_html=True)