import re
import subprocess
import os

def get_captions_text(video_url, lang='it'):
    """
    Retrieve captions as plain text using yt-dlp. Converts .vtt file to plain text if needed.
    """
    try:
        command = [
            'yt-dlp', '--write-auto-subs', '--skip-download',
            '--sub-lang', lang, '--output', '-', video_url
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0 or not result.stdout.strip():
            print(f"Warning: Captions saved as .vtt file, attempting to process it...")

            vtt_file = f"-.{lang}.vtt"
            if os.path.exists(vtt_file):
                plain_text = vtt_to_clean_text(vtt_file)
                os.remove(vtt_file)
                return plain_text
            else:
                print("No .vtt file found.")
                return None

        plain_text = vtt_to_clean_text_from_string(result.stdout)
        return plain_text

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def vtt_to_clean_text(file_path):
    """
    Convert .vtt file to plain text, remove repetitions and tags.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = clean_repetitions(lines)
    return '\n'.join(cleaned_lines)


def vtt_to_clean_text_from_string(vtt_content: str):
    """
    Convert VTT content (string format) to plain text, remove repetitions and tags.
    """
    lines = vtt_content.split('\n')
    cleaned_lines = clean_repetitions(lines)
    return '\n'.join(cleaned_lines)


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


# Example usage
video_url = "https://www.youtube.com/watch?v=a4MiNTZMtXE"
captions_text = get_captions_text(video_url, lang='it')  # 'it' for Italian, 'en' for English
if captions_text:
    print("Transcript Text:\n", captions_text)
else:
    print("No captions available.")
