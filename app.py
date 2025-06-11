from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import random

app = Flask(__name__)
app.secret_key = 'flashcard-secret'

# Load questions from JSON file once
with open('questions.json', 'r') as f:
    ALL_QUESTIONS = json.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        num_questions = int(request.form.get("num_questions", 10))
        # Shuffle and pick the requested number of questions
        session['questions'] = random.sample(ALL_QUESTIONS, min(num_questions, len(ALL_QUESTIONS)))
        session['current'] = 0
        session['score'] = 0
        return redirect(url_for('game'))
    return render_template("index.html", total=len(ALL_QUESTIONS))

@app.route("/game")
def game():
    current = session.get('current', 0)
    questions = session.get('questions', [])
    if current >= len(questions):
        return redirect(url_for('results'))
    q = questions[current]
    return render_template("game.html", q=q, index=current+1, total=len(questions), score=session.get('score', 0))

@app.route("/answer", methods=["POST"])
def answer():
    selected = request.form.get("option")
    current = session.get('current', 0)
    questions = session['questions']
    correct = questions[current]['answer']
    if selected == correct:
        session['score'] += 1
    session['current'] += 1
    return redirect(url_for('game'))

@app.route("/results")
def results():
    score = session.get('score', 0)
    total = len(session.get('questions', []))
    return render_template("results.html", score=score, total=total)

if __name__ == "__main__":
    app.run(debug=True)