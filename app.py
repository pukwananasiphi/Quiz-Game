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
        session['answered_correctly_this_q'] = False # Flag for the current question
        return redirect(url_for('game'))
    return render_template("index.html", total=len(ALL_QUESTIONS))

@app.route("/game")
def game():
    current = session.get('current', 0)
    questions = session.get('questions', [])
    if current >= len(questions):
        return redirect(url_for('results'))
    q = questions[current]
    # Pass whether this specific question has been answered correctly in this session
    answered_correctly_this_q = session.get('answered_correctly_this_q', False)
    return render_template("game.html",
                           q=q,
                           index=current+1,
                           total=len(questions),
                           score=session.get('score', 0),
                           answered_correctly_this_q=answered_correctly_this_q)

@app.route("/answer", methods=["POST"])
def answer():
    selected = request.form.get("option")
    current = session.get('current', 0)
    questions = session['questions']

    if current >= len(questions):
        return jsonify({"error": "No current question"}), 400

    q = questions[current]
    correct_answer = q['answer']
    explanation = q.get('explanation', 'No explanation provided for this question.')

    is_correct = (selected == correct_answer)

    # Only update score if the answer is correct AND it hasn't been scored for this question yet
    if is_correct and not session.get('answered_correctly_this_q', False):
        session['score'] += 1
        session['answered_correctly_this_q'] = True # Mark as correctly answered for this session

    return jsonify({
        "is_correct": is_correct,
        "correct_answer": correct_answer,
        "explanation": explanation,
        "current_score": session['score'],
        "Youtubeed_correctly_now": session.get('answered_correctly_this_q', False) # True if *this* submission made it correct or if already correct
    })

@app.route("/next_question", methods=["POST"])
def next_question():
    # This route is hit when the user explicitly clicks "Next Question" or "Skip"
    # It always advances the question.
    current = session.get('current', 0)
    questions = session.get('questions', [])

    if current < len(questions):
        session['current'] += 1
        session['answered_correctly_this_q'] = False # Reset flag for the new question

    if session['current'] >= len(questions):
        return redirect(url_for('results'))
    else:
        return redirect(url_for('game'))


@app.route("/results")
def results():
    score = session.get('score', 0)
    total = len(session.get('questions', []))
    return render_template("results.html", score=score, total=total)

if __name__ == "__main__":
    app.run(debug=True)