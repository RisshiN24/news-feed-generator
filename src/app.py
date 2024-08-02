from flask import Flask, request, render_template
from openai import OpenAI
import requests
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)


@app.route('/')
def input_interests():
    return render_template('input.html')


@app.route('/display', methods=['POST'])
def display_interests():
    interests = [request.form['interest1'], request.form['interest2'], request.form['interest3']]
    news_feed = get_news_feed(os.getenv("NEWS_API_KEY"), interests)
    return render_template('display.html', news_feed=news_feed)

def get_news_feed(api_key, interests):
    articles = []
    for interest in interests:
        url = f"https://newsapi.org/v2/everything?q={interest}&sortBy=popularity&apiKey={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            articles.extend(data.get('articles', [])[:3])  # Get only the top 3 articles for each interest
    return articles

if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)