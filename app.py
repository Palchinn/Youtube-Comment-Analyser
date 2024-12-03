from flask import Flask, request, jsonify, render_template
from youtube_comment_downloader import YoutubeCommentDownloader
from textblob import TextBlob

app = Flask(__name__)

# Function to scrape comments from a YouTube video
def scrape_comments(video_url):
    downloader = YoutubeCommentDownloader()
    generator = downloader.get_comments_from_url(video_url)
    comments = []
    
    for comment in generator:
        comments.append(comment['text'])
    
    return comments

# Function to analyze sentiment using TextBlob
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity == 0:
        return "Neutral"
    else:
        return "Negative"

# API route to scrape comments and analyze sentiment
@app.route('/analyze_comments', methods=['POST'])
def analyze_comments():
    data = request.json
    video_url = data.get('video_url', '')
    
    comments = scrape_comments(video_url)  # Scrape comments
    analyzed_comments = [{'comment': comment, 'sentiment': analyze_sentiment(comment)} for comment in comments]

    return jsonify(analyzed_comments)

# Route to serve the HTML frontend
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
