import requests
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
import matplotlib.pyplot as plt
from flask import Flask, request, render_template

# Download the VADER lexicon for sentiment analysis
nltk.download('vader_lexicon')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Get the name of the movie from the form data
    movie_name = request.form['movie_name']

    api_key = "e0a0015ede8a824fab642d5d1660255e"
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"
    search_response = requests.get(search_url)
    search_results = search_response.json()

    # Get the ID of the first result from the search
    movie_id = search_results["results"][0]["id"]

    # Define the base URL for the TMDB API
    BASE_URL = "https://api.themoviedb.org/3/"

    # Define the URL for the movie reviews endpoint
    reviews_url = BASE_URL + f"movie/{movie_id}/reviews?api_key={api_key}&language=en-US&page=1"

    # Send a GET request to the movie reviews endpoint
    response = requests.get(reviews_url)

    # Check if the request was successful
    if response.status_code != 200:
        return render_template('error.html')

    # Parse the response JSON and extract the review content
    reviews = [review["content"] for review in response.json()["results"]]

    # Perform sentiment analysis on each review
    sid = SentimentIntensityAnalyzer()
    positive_reviews = []
    negative_reviews = []
    for review in reviews:
        scores = sid.polarity_scores(review)

        # Check if the review is positive or negative
        if scores["compound"] >= 0.05:
            positive_reviews.append(review)
        elif scores["compound"] <= -0.05:
            negative_reviews.append(review)

    # Combine all the positive reviews into one document
    positive_doc = " ".join(positive_reviews)

    # Tokenize the positive document into sentences
    positive_sentences = sent_tokenize(positive_doc)

    # Summarize the positive sentences into one sentence
    positive_summary = " ".join(positive_sentences[:1])

    # Combine all the negative reviews into one document
    negative_doc = " ".join(negative_reviews)

    # Tokenize the negative document into sentences
    negative_sentences = sent_tokenize(negative_doc)

    # Summarize the negative sentences into one sentence
    negative_summary = " ".join(negative_sentences[:1])

    # Calculate the percentages of positive and negative reviews
    total_reviews = len(reviews)
    num_positive_reviews = len(positive_reviews)
    num_negative_reviews = len(negative_reviews)
    percent_positive_reviews = num_positive_reviews / total_reviews * 100
    percent_negative_reviews = num_negative_reviews / total_reviews * 100

    # Return the results to the results page
    return render_template('results.html', movie_name=movie_name, positive_summary=positive_summary, negative_summary=negative_summary, percent_positive_reviews=percent_positive_reviews, percent_negative_reviews=percent_negative_reviews)

if __name__ == '__main__':
    app.run(debug=True)

