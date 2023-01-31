from flask import Flask, request, render_template
import tweepy
from textblob import TextBlob

app = Flask(__name__)

# Twitter API credentials
consumer_key = "vrXfWLAq7N68NLRpGlIbyxI88"
consumer_secret = "E6vdhoM8YdcaVlB7Q0pF8rDcpaSazJqun1Lhy16HiE1nkg4PbH"
access_token = "70369388-9Z3sdeSFEnxCSiXkrjpgfcPSF00nYYNTZlCm1nuEj"
access_token_secret = "gSINiTLf05Atq5HxtLItWaOaWRFkSJs0f0cd6C3VOCYbh"

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sentiment", methods=["POST"])
def sentiment():
    # Get the hashtag from the form
    hashtag = request.form["hashtag"]

     # Retrieve the latest 200 tweets for the given hashtag
    tweets = api.search_tweets(q="#" + hashtag, count=200)

    # Perform sentiment analysis on each tweet
    sentiments = []
    for tweet in tweets:
        analysis = TextBlob(tweet.text)
        sentiment = analysis.sentiment.polarity
        sentiments.append(sentiment)

    # Determine the overall sentiment for the tweets
    overall_sentiment = sum(sentiments) / len(sentiments)
    if overall_sentiment > 0:
        sentiment = "positive"
    elif overall_sentiment < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    # Render the result in the template
    return render_template("sentiment.html", sentiment=sentiment, hashtag="#" + hashtag)


if __name__ == "__main__":
    app.run()
