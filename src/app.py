from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def input_interests():
    return render_template('input.html')

@app.route('/display', methods=['POST'])
def display_interests():
    interests = [request.form['interest1'], request.form['interest2'], request.form['interest3']]
    return render_template('display.html', interests=interests)

if __name__ == '__main__':
    app.run(debug=True)