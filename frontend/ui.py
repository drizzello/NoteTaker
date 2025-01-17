# frontend/ui.py
import streamlit as st
from backend.transcript_manager import YouTubeTranscriptManager
from backend.ai_manager import AIManager
from frontend.styles import STYLES
import os
import glob
import time



class StreamlitUI:
    
    def __init__(self):
        self.setup_page_config()
        self.setup_styles()
        self.init_session_state()
        #self.ai_manager = AIManager(st.secrets["api_key"])
        self.ai_manager = AIManager("AIzaSyAFq4p_PxK9F0X7uu0GILhvO53MAd5FJpY")

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
                  <h1 style='margin-bottom: 0; color: #00000; font-size: 3em;'>ContentCrunch AI</h1>
                  <p style='color: #666; margin-top: 0.5em; font-size: 1.2em;'>Never Miss the Good Parts. Get Written Video Highlights in Seconds ⚡️ </p>
                  <p style='color: #888; font-size: 1em; font-style: italic;'>Powered by Gemini AI | Skip the Fluff • Catch Key Points • Save Time </p>
            """, unsafe_allow_html=True)
    

    @st.cache_data(show_spinner=False)
    def process_video(_self, video_link: str, max_retries: int = 5, retry_delay: float = 2.0):
        try:
            video_id = YouTubeTranscriptManager.extract_video_id(video_link)
            if not video_id:
                st.error("❌ Invalid YouTube link. If you think the link is valid, try pushing again the button.")
                return None

            attempt = 0
            video_info = None

            # Retry loop
            while attempt < max_retries:
                try:
                    st.write(f"Attempt {attempt + 1} to retrieve transcript...")
                    video_info = YouTubeTranscriptManager.get_transcript(video_id)

                    if video_info and video_info.formatted_text:
                        st.session_state.update({
                            'text_formatted': video_info.formatted_text,
                            'transcript_ready': True
                        })
                        st.success("✅ Transcript retrieved successfully!")
                        st.expander(video_info.formatted_text)

                        return video_info
                    else:
                        st.warning("No transcription found. Retrying...")

                except Exception as inner_e:
                    st.warning(f"Attempt {attempt + 1} failed: {str(inner_e)}")

                # Increment attempt and wait before retrying
                attempt += 1
                time.sleep(retry_delay)

            st.error("❌ Unable to retrieve the transcript after multiple attempts. I'm so sorry :(")
            return None

        except Exception as e:
            st.error(f"❌ Critical error: {str(e)}")
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

    def render_main(self):
        self.render_header()
        
        with st.container():
            st.markdown("### 🎥 Enter Video URL")
            video_link = st.text_input(
                "Youtube Video Url",
                placeholder="Paste your YouTube video URL here...",
                help="Works with regular YouTube videos, shorts, and live streams",
                label_visibility="hidden"
            )
                    # Informative message below the input field
            st.markdown(
                  """
                  <div class="message" style="
                     padding: 0.5rem 1rem;
                     background-color: #f9f9f9;
                     border-left: 4px solid #90D4B7;
                     color: #333;
                     font-size: 0.9rem;
                     margin-top: 0.5rem;
                     border-radius: 5px;
                  ">
                     ⚠️ **Note:** This system uses free APIs and may occasionally experience limitations or fail to retrieve data.
                  </div>
                  """,
                  unsafe_allow_html=True
            )

            if st.button("📝 Get Transcript and Summarize it", use_container_width=True) and video_link:
                with st.spinner("Fetching transcript and summarizing..."):
                    #st.write("Current working directory:", os.getcwd())
                    #st.write("Available files:", os.listdir())
                    #files = glob.glob('/tmp/*')
                    #st.write("Files in /tmp directory:", files)


                    if video_info := self.process_video(video_link):
                        #files = glob.glob('/tmp/*')
                        #st.write("Files in /tmp directory:", files)


                        #st.write(video_info.formatted_text)
                        self.generate_summary(video_info.formatted_text)


    def render_footer(self):
      st.markdown("""
        <div style='text-align: center; color: #666; padding: 2rem 0;'>
            <p>Made with ❤️ by Your 🐯 Company </p>
            <p>Support my work 👇 </p>
            <a href="https://www.buymeacoffee.com/daviderizz" target="_blank">
                <img src="https://cdn.buymeacoffee.com/buttons/v2/default-green.png" alt="Buy Me A Coffee" 
                style="height: 20px !important;width: 100px !important;">
            </a>
        </div>
    """, unsafe_allow_html=True)


