from flask import Flask, request, render_template, jsonify
import requests
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import ChatOpenAI
import bs4
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Set your API keys
news_api_key = os.getenv("NEWS_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def input_interests():
    return render_template('input.html')

@app.route('/display', methods=['POST'])
def display_interests():
    interests = [request.form['interest1'], request.form['interest2'], request.form['interest3']]
    news_feed = get_news_feed(news_api_key, interests)
    return render_template('display.html', news_feed=news_feed)

def get_news_feed(api_key, interests):
    news_feed = {}
    for interest in interests:
        url = f"https://newsapi.org/v2/everything?q={interest}&sortBy=popularity&apiKey={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            valid_articles = []
            for article in data.get('articles', [])[:6]:
                title = article.get('title')
                url = article.get('url')
                if title and '[Removed]' not in title and url and not url.startswith('https://consent.yahoo.com'):
                    valid_articles.append(article)
            news_feed[interest] = valid_articles
    return news_feed

@app.route('/summarize', methods=['POST'])
def summarize_article():
    url = request.form['url']
    title = request.form['title']
    summary = generate_summary(url)
    return render_template('summary.html', title=title, summary=summary, url=url)

def generate_summary(url):
    loader = WebBaseLoader(url)
    docs = loader.load()
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    chain = load_summarize_chain(llm, chain_type="stuff")
    result = chain.invoke(docs)
    summary = result["output_text"]
    return summary

if __name__ == '__main__':
    app.run(debug=True)
