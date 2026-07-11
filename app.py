import streamlit as st
import pandas as pd
import subprocess
import json
import re
from textblob import TextBlob

# లింక్ నుండి వీడియో ID తీయడానికి ఫంక్షన్
def extract_video_id(url):
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_video_comments_free(video_url):
    video_id = extract_video_id(video_url)
    if not video_id:
        raise Exception("Invalid YouTube URL.")
        
    # yt-dlp కమాండ్: ఇది అఫీషియల్ గా కామెంట్స్ డౌన్లోడ్ చేస్తుంది
    cmd = ["yt-dlp", "--get-comments", "--skip-download", "--print-json", f"https://www.youtube.com/watch?v={video_id}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception("Could not fetch comments.")
    
    data = json.loads(result.stdout)
    comments = []
    if 'comments' in data:
        for c in data['comments']:
            comments.append(c['text'])
    return comments[:50]

# --- UI సెక్షన్ (పాత కోడ్ లాగే ఉంటుంది) ---
st.set_page_config(page_title="AI Video Analyst Pro", layout="centered")
# (ఇక్కడ మీ పాత CSS మరియు UI కోడ్ మొత్తాన్ని అలాగే ఉంచేయండి)
# ...
