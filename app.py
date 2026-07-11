import streamlit as st
import pandas as pd
import re
from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR
from textblob import TextBlob

def extract_video_id(url):
    """
    యూట్యూబ్ లింక్ ఏ ఫార్మాట్‌లో ఉన్నా (Shorts, Mobile, Web, Playlist) 
    దాని నుండి కేవలం 11 అక్షరాల వీడియో ID ని మాత్రమే వేరు చేస్తుంది.
    """
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_video_comments_free(video_url):
    video_id = extract_video_id(video_url)
    if not video_id:
        raise Exception("Invalid YouTube URL. Please check the link.")
        
    downloader = YoutubeCommentDownloader()
    # ఇక్కడ url కి బదులు కేవలం video_id ని పంపుతున్నాం
    generator = downloader.get_comments(video_id, sort_by=SORT_BY_POPULAR)
    comments = []
    count = 0
    for comment in generator:
        comments.append(comment['text'])
        count += 1
        if count >= 50:
            break
    return comments

# Page Config & Beautiful UI Theme
st.set_page_config(page_title="AI Video Analyst Pro", layout="centered")

# Custom CSS for Premium Moody Look & Download Button
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    .stTextInput input {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #475569 !important;
        border-radius: 10px !important;
        padding: 12px !important;
    }
    .stButton>button, .stDownloadButton>button {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important;
        font-weight: bold !important;
        padding: 12px 30px !important;
        border-radius: 25px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.6) !important;
    }
    .metric-container {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin-top: 25px;
        margin-bottom: 25px;
    }
    .card {
        background: rgba(30, 41, 59, 0.7);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        flex: 1;
        backdrop-filter: blur(10px);
    }
    .card-title { font-size: 14px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }
    .card-value { font-size: 28px; font-weight: bold; margin-top: 5px; }
    .val-total { color: #38bdf8; }
    .val-pos { color: #4ade80; }
    .val-neg { color: #f87171; }
    
    /* Comment list section */
    .comment-box {
        background: rgba(30, 41, 59, 0.4);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 5px solid #475569;
    }
    .pos-border { border-left-color: #4ade80; }
    .neg-border { border-left-color: #f87171; }
    </style>
""", unsafe_allow_html=True)

# Main Title Header
st.markdown("<h1 style='text-align: center; color: #ffffff; font-size: 42px; font-weight: 800; margin-bottom: 5px;'>📊 AI Video Analyst <span style='color: #a855f7;'>Pro</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 16px; margin-bottom: 30px;'>Unlock audience sentiments instantly without API constraints.</p>", unsafe_allow_html=True)

# Input field
video_url = st.text_input("YouTube Video URL", placeholder="Paste your link here and watch the magic...")

if st.button("Analyze Sentiment"):
    if video_url:
        with st.spinner("🔄 Deep analyzing comments... Please hold on."):
            try:
                raw_comments = get_video_comments_free(video_url)
                
                data_list = []
                positive_examples = []
                negative_examples = []
                
                positive = 0
                negative = 0
                
                for comment in raw_comments:
                    analysis = TextBlob(comment)
                    polarity = analysis.sentiment.polarity
                    
                    if polarity > 0:
                        sentiment_label = "Positive"
                        positive += 1
                        if len(positive_examples) < 3:
                            positive_examples.append(comment)
                    elif polarity < 0:
                        sentiment_label = "Negative"
                        negative += 1
                        if len(negative_examples) < 3:
                            negative_examples.append(comment)
                    else:
                        sentiment_label = "Neutral"
                        
                    data_list.append({"Comment": comment, "Sentiment": sentiment_label, "Score": round(polarity, 2)})
                
                # Create DataFrame for downloading
                df = pd.DataFrame(data_list)
                
                st.markdown("<h3 style='margin-top:30px; color:#4ade80;'>✅ Analysis Complete!</h3>", unsafe_allow_html=True)
                
                # HTML Dashboard Cards
                st.markdown(f"""
                    <div class="metric-container">
                        <div class="card">
                            <div class="card-title">My apps</div>
                            <div class="card-value val-total">{len(raw_comments)}</div>
                        </div>
                        <div class="card">
                            <div class="card-title">Positive</div>
                            <div class="card-value val-pos">😊 {positive}</div>
                        </div>
                        <div class="card">
                            <div class="card-title">Negative</div>
                            <div class="card-value val-neg">😡 {negative}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Feature 1: Advanced Download Button
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Excel/CSV Report",
                    data=csv,
                    file_name="youtube_sentiment_report.csv",
                    mime="text/csv"
                )
                
                # Feature 2: Highlights of top comments
                st.markdown("<h2 style='margin-top:40px; color:#ffffff;'>💬 Sentiment Highlights</h2>", unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("<h4 style='color:#4ade80;'>⭐ Top Positive Vibes</h4>", unsafe_allow_html=True)
                    if positive_examples:
                        for pc in positive_examples:
                            st.markdown(f'<div class="comment-box pos-border">{pc}</div>', unsafe_allow_html=True)
                    else:
                        st.write("No strong positive comments found.")
                        
                with col2:
                    st.markdown("<h4 style='color:#f87171;'>⚠️ Critical Feedback</h4>", unsafe_allow_html=True)
                    if negative_examples:
                        for nc in negative_examples:
                            st.markdown(f'<div class="comment-box neg-border">{nc}</div>', unsafe_allow_html=True)
                    else:
                        st.write("No negative comments found. Great video!")
                
            except Exception as e:
                st.error(f"Error occurred: {e}")
    else:
        st.warning("Please paste a valid YouTube URL first!")
