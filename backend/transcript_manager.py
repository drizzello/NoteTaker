# backend/transcript_manager.py
from dataclasses import dataclass
from typing import Optional, Dict, List
import urllib.parse as parser
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

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
    def get_transcript(video_id: str, languages: List[str] = ["it", "en"]) -> VideoInfo:
        """Fetch and format transcript for a given video ID."""
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        formatted_text = TextFormatter().format_transcript(transcript)
        return VideoInfo(video_id, transcript, formatted_text)
