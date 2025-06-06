from flask import Blueprint, current_app, render_template, request, redirect, url_for
import uuid
import datetime

pages = Blueprint("habits", __name__, template_folder="templates", static_folder="static")

@pages.context_processor
def add_calc_daterange():
    def daterange(start: datetime.datetime):
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]
        return dates
    return {"date_range": daterange}

def today_at_midnight():
    today = datetime.datetime.today()
    return datetime.datetime(today.year, today.month, today.day)
    
@pages.route("/")
def index():
    date_str = request.args.get("date")
    if date_str:
        selected_date = datetime.datetime.fromisoformat(date_str)
    else:
        selected_date = today_at_midnight()
        
    habits_on_date = current_app.db.habits.find({"added": {"$lte": selected_date}})
    completions = [
        habit["habit"]
        for habit in current_app.db.completions.find({'date': selected_date})
    ]
    return render_template("index.html", 
        habits=habits_on_date, 
        title="Habit Tracker - Home", 
        completions = completions,
        selected_date = selected_date)


@pages.route("/add", methods=["GET", "POST"])
def add_habit():
    today = today_at_midnight()
    if request.form:
        current_app.db.habits.inset_one(
            {"_id": uuid.uuid4().hex, "added": today, "name": request.form.get("habit")}
        )
            
    
    return render_template("add_habit.html", 
        title="Habit Tracker - Add Habit", 
        selected_date = today)

@pages.post("/complete")
def complete():
    date_str = request.form.get("date")
    habit = request.form.get("habitId")
    date = datetime.datetime.fromisoformat(date_str)
    current_app.db.completion.inset_one({"date": date, "habit": habit})    
    return redirt(url_for("habits.index", date=date_str))