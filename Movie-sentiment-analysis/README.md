Here's how it works:

The user enters the name of a movie on the home page, and this information is sent to the Flask web application via a form on the home page.

The Flask web application receives the movie name via a POST request to the /analyze endpoint.

The application then uses the TMDb API to search for the movie based on the name entered by the user. It extracts the ID of the first result from the search.

Using this ID, the application sends a GET request to the TMDb API to retrieve the movie reviews for the movie.

If the GET request is successful (i.e. returns a status code of 200), the application extracts the content of each review from the response JSON.

The application then uses the VADER (Valence Aware Dictionary and sEntiment Reasoner) lexicon from the NLTK (Natural Language Toolkit) library to perform sentiment analysis on each review. VADER is a rule-based sentiment analysis tool that uses a lexicon of words and phrases with positive and negative sentiment scores.

The application classifies each review as positive or negative based on the compound sentiment score returned by VADER. The compound score is a value between -1 and 1 that represents the overall sentiment of the text. Scores greater than or equal to 0.05 are considered positive, scores less than or equal to -0.05 are considered negative, and scores between -0.05 and 0.05 are considered neutral.

The application combines all the positive reviews into one document and tokenizes it into sentences. It then summarizes the positive sentences into one sentence.

The application repeats this process for the negative reviews, combining them into one document, tokenizing them into sentences, and summarizing them into one sentence.

The application calculates the percentages of positive and negative reviews and returns these, along with the movie name and the positive and negative summaries, to the results page. The results page displays the movie name, positive and negative summaries, and pie chart with the percentages of positive and negative reviews.