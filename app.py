import streamlit as st
import pandas as pd
import subprocess
import json
import re
from textblob import TextBlob

def get_video_comments_free(video_url):
    # yt-dlp ఉపయోగించి నేరుగా కామెంట్లు డౌన్‌లోడ్ చేస్తుంది
    cmd = [
        "yt-dlp", "--get-comments", "--skip-download", 
        "--print-json", video_url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception("Could not fetch comments. The video might not have comments enabled.")
    
    data = json.loads(result.stdout)
    comments = []
    if 'comments' in data:
        for c in data['comments']:
            comments.append(c['text'])
    return comments[:50] # మొదటి 50 కామెంట్లు

# పైన ఉన్న కోడ్ అలాగే ఉంచి, కింది సెక్షన్ లో get_video_comments_free ఫంక్షన్ ని వాడుకోండి.
# (మిగతా UI కోడ్ అంతా పాతదే ఉంచవచ్చు)
