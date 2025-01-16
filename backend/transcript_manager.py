# backend/transcript_manager.py
from dataclasses import dataclass
from typing import Optional, Dict, List
import urllib.parse as parser
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from googleapiclient.discovery import build
import subprocess
import os
import re
import streamlit as st
import yt_dlp
import requests
import glob

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
        
         # Caso classico con 'v' nella query
         if "v" in query:
            return query["v"][0]
         
         # URL youtu.be/<video_id>
         if url_data.netloc == "youtu.be":
            return url_data.path.lstrip("/")  # Restituisce l'ID del video dalla path
         
         # URL /shorts/<video_id> o /live/<video_id>
         path_parts = url_data.path.split("/")
         if "shorts" in path_parts or "live" in path_parts:
            return path_parts[-1]  # Ultima parte della path come ID del video

    @staticmethod
    def get_transcript(video_link, video_id: str, languages: List[str] = ["it", "en"]) -> Optional[VideoInfo]:
        """Fetch and format transcript for a given video ID using youtube-transcript-api."""
        # Free proxy list
        proxy_list = {
                '170.78.94.200': '5678',
                '208.109.229.141': '54557'
                }
        for proxy in proxy_list:
            try:    
                proxies = {'https': proxy, 'http': proxy}

                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['it', 'en'], proxies=proxies)
                formatter = TextFormatter()
                text_formatted = formatter.format_transcript(transcript=transcript)
                #return YouTubeTranscriptManager.get_captions_other_api(video_id, video_link=video_link)
                return VideoInfo(video_id=video_id, transcript="", formatted_text=text_formatted)

            except Exception as e:
                st.write(f"❌ youtube-transcript-api failed: {str(e)}")
                st.write(f"❌ proxy: {proxy}")

                # Attempt to use YouTube Data API v3 if youtube-transcript-api fails
                #return YouTubeTranscriptManager.get_captions_other_api(video_id, video_link)


    @staticmethod
    def get_captions_other_api(video_id, video_link: str, lang='it') -> Optional[VideoInfo]:
        try:
            # Create a temporary directory if it doesn't exist
            os.makedirs('./tmp', exist_ok=True)
            # Updated yt-dlp command
            command = [
                'yt-dlp', '--write-auto-subs', '--skip-download',
                '--sub-lang', lang, '--sub-format', 'vtt', '--output', f'./tmp/{video_id}.%(ext)s', video_link
            ]
            response = requests.get(f"https://www.youtube.com/watch?v={video}")
            size_in_bytes = len(response.content)
            size_in_kb = size_in_bytes / 1024

            st.write(f"HTTP response size: {size_in_kb:.2f} KB")

            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
          

            # If captions were written to a file, read and clean them
            vtt_file = f"./tmp/{video_id}.{lang}.vtt"
            if os.path.exists(vtt_file):
                #files = glob.glob('/tmp/*')
                #st.write("Files in /tmp directory:", files)

                formatted_text = YouTubeTranscriptManager.vtt_to_clean_text(vtt_file)  # Read the .vtt file
                #os.remove(vtt_file)  # Optionally delete the file after reading
                return VideoInfo(video_id=video_id, transcript="", formatted_text=formatted_text)
            else:
                #st.write("No .vtt file found.")
                return None


        except Exception as e:
            print(f"❌ Error retrieving captions using API: {str(e)}")
            return 
    

    @staticmethod
    def vtt_to_clean_text(file_path):
        """
        Convert .vtt file to plain text, remove repetitions and tags.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        cleaned_lines = YouTubeTranscriptManager.clean_repetitions(lines)
        return '\n'.join(cleaned_lines)

    @staticmethod
    def vtt_to_clean_text_from_string(vtt_content: str):
        """
        Convert VTT content (string format) to plain text, remove repetitions and tags.
        """
        lines = vtt_content.split('\n')
        cleaned_lines = YouTubeTranscriptManager.clean_repetitions(lines)
        return '\n'.join(cleaned_lines)

    @staticmethod
    def clean_repetitions(lines):
        """
        Remove timestamps, HTML-like tags, and repeated consecutive lines.
        """
        cleaned_lines = []
        last_line = None

        for line in lines:
            line = line.strip()

            # Skip timestamps and empty lines
            if '-->' in line or line.isdigit() or not line:
                continue

            # Remove tags (like <c>, <b>, etc.)
            clean_line = re.sub(r'<[^>]+>', '', line)

            # Avoid consecutive duplicates
            if clean_line != last_line:
                cleaned_lines.append(clean_line)
                last_line = clean_line

        return cleaned_lines
