from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "wahaha"
app.config['DEBUG'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
responses = []

@app.route("/")
def show_survey_start():
    return render_template("start_survey.html", survey=survey)

@app.route("/begin", methods = ["POST"])
def start_survey():
    return redirect("/questions/0")

@app.route("/questions/<int:qid>")
def show_question(qid):
    if qid != len(responses):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    if len(responses) == 4:
        return redirect("/complete")

    question = survey.questions[qid]
    return render_template("questions.html", questions = question)

@app.route("/answer", methods = ["POST"])
def handle_question():
    answer = request.form['answer']
    responses.append(answer)
    if len(responses) < 4:
        return redirect(f"/questions/{len(responses)}")
    else:
        return redirect("/complete")
    
@app.route("/complete")
def completion():
    return render_template("completion.html")
