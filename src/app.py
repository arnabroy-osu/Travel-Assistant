from flask import Flask, render_template, request, jsonify
from config import app_config
import time
import json
import innsight_model
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)
app.config.from_object(app_config)

@app.route('/')
def home():
    return render_template('index.html', app_name=app.config['APP_NAME'])

@app.route('/search', methods=['POST'])
def search():
    search_option = request.form.get('option', 'hotel')
    search_string = request.form.get('search_string', '')
    min_rating = request.form.get('min_rating', 0)    
    
    search_results = innsight_model.search_places(search_string, search_option, min_rating)

    r_prompt = """
        Which of the hotels has the best reviews and why do you think that? You must make a choice
        and choose one hotel and provide reasoning behind it. 
    """

    r_prompt1 = """ what are the main key words used in the reviews? """

    r_prompt2 = """ Analyze the reiviews of the hotel, and tell which has the positive sentiment? Based on sentiment 
        analysis recommend top 3 hotels? And provide the sentiment scores for each hotel? """
    
    final_results = []

    for eachResult in search_results:
        if 'allReviews' in eachResult:
            eachResult['reviewWords'] = \
                innsight_model.analyze_reviews(eachResult['allReviews'], r_prompt1)
        
        sent_scores = review_scores(eachResult['reviews']) if eachResult['reviews'] != None else None
        eachResult['sentimentScores'] = sent_scores
        #eachResult['scoreChart'] = create_chart(sent_scores) if sent_scores != None else None
        final_results.append(eachResult)

    return jsonify(final_results)

def review_scores(reviews):
    ''' 
        return sentiment analysis scores for provided reviews.
    '''
    sid = SentimentIntensityAnalyzer()

    # List to store sentiments
    sentiment_scores = [] 

    for each_review in reviews: 
        try:
            sentiment_scores.append(sid.polarity_scores(each_review['text']['text']))
        except Exception as ex:
            print(f"Review: {each_review['text']['text']} Error: {ex}")
    
    # Calculate the combined sentiment score by averaging the individual scores
    if sentiment_scores:
        combined_score = {
            'Overall': round(sum(score['compound'] for score in sentiment_scores) / len(sentiment_scores), 5),
            'Negative': round(sum(score['neg'] for score in sentiment_scores) / len(sentiment_scores), 5),
            'Neutral': round(sum(score['neu'] for score in sentiment_scores) / len(sentiment_scores), 5),
            'Positive': round(sum(score['pos'] for score in sentiment_scores) / len(sentiment_scores), 5)
        }

        return combined_score

def create_chart(sentiment_scores, place_name):
    categories = list(sentiment_scores.keys())
    scores = list(sentiment_scores.values())

    plt.figure(figsize=(8, 6))
    plt.pie(scores, labels=categories, autopct='%1.1f%%', startangle=40)
    plt.axis('equal')
    plt.title(f'Reviews Disribution - {place_name}')
    plt.show()

    # Save the plot to a memory buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convert the plot to base64 string
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return plot_data

if __name__ == '__main__':
    app.run(debug=True)
