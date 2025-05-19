from flask import Flask, render_template, request, redirt, url_for
from collections import defaultdict
import datetime
app = Flask(__name__)

habits = ["Test habit", "Test habit 2"]

completions = defaultdict(list)


@app.context_processor
def add_calc_daterange():
    def daterange(start: datetime.date):
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]
        return dates
    return {"date_range": daterange}

@app.route("/")
def index():
    date_str = request.args.get("date")
    if date_str:
        selected_date = datetime.date.fromisoformat(date_str)
    else:
        selected_date = datetime.date.today()
    return render_template("index.html", 
        habits=habits, 
        title="Habit Tracker - Home", 
        completions = completions[selected_date],
        selected_date = selected_date)


@app.route("/add", methods=["GET", "POST"])
def add_habit():
    if request.method == "POST":
        if request.form.get("habit") is not None:
            habits.append(request.form.get("habit"))
    return render_template("add_habit.html", 
        title="Habit Tracker - Add Habit", 
        selected_date = datetime.date.today())

@app.post("/complete"):
    date_str = request.form.get("date")
    habit = request.form.get("habitName")
    date = datetime.date.fromisoformat(date_str)
    completions[date].append(habit)
    
    return redirt(url_for("index", date=date_str))