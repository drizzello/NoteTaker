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
        try:
      
            return YouTubeTranscriptManager.get_captions_other_api(video_id, video_link=video_link)
        
        except Exception as e:
            print(f"❌ youtube-transcript-api failed: {str(e)}")
            # Attempt to use YouTube Data API v3 if youtube-transcript-api fails
            #return YouTubeTranscriptManager.get_captions_other_api(video_id, video_link)

    @staticmethod
    def get_captions_other_api(video_id, video_link: str, lang='it') -> Optional[VideoInfo]:
        """Fetch available captions for the video using YouTube Data API v3."""
        try:
            command = [
            'yt-dlp', '--write-auto-subs', '--skip-download',
            '--sub-lang', lang, '--output', '-', video_link
            ]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode != 0 or not result.stdout.strip():
                print(f"Warning: Captions saved as .vtt file, attempting to process it...")

                vtt_file = f"-.{lang}.vtt"
                if os.path.exists(vtt_file):
                    formatted_text = vtt_to_clean_text(vtt_file)
                    os.remove(vtt_file)
                    return VideoInfo(video_id=video_id, transcript="", formatted_text=formatted_text)
                else:
                    print("No .vtt file found.")    
                    return None

            # If captions were streamed successfully, clean them
            formatted_text = vtt_to_clean_text_from_string(result.stdout)
            return VideoInfo(video_id=video_id, transcript="", formatted_text=formatted_text)


        except Exception as e:
            print(f"❌ Error retrieving captions using YouTube API: {str(e)}")
            return None

@staticmethod
def vtt_to_clean_text(file_path):
    """
    Convert .vtt file to plain text, remove repetitions and tags.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = clean_repetitions(lines)
    return '\n'.join(cleaned_lines)

@staticmethod
def vtt_to_clean_text_from_string(vtt_content: str):
    """
    Convert VTT content (string format) to plain text, remove repetitions and tags.
    """
    lines = vtt_content.split('\n')
    cleaned_lines = clean_repetitions(lines)
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
