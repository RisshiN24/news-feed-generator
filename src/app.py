from flask import Flask, request, render_template
from openai import OpenAI
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
    story = generate_story(interests)
    return render_template('display.html', story=story)

def generate_story(interests):
    
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {"role": "system", "content": "You are a helpful assistant. You generate short stories based on the keywords given to you. You can only write stories up to 200 words."},
            {"role": "user", "content": f"Create a short story that includes the following interests: {', '.join(interests)}."}
        ],
        max_tokens=300
    )

    story = response.choices[0].message.content
    return story

if __name__ == '__main__':
    app.run(debug=True)