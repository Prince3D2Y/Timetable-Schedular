from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = "secret-key"
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
timetable = {day: [] for day in weekdays}

def is_clash(day, slot):
    return any(c["slot"] == slot for c in timetable.get(day, []))

@app.route("/")
def index():
    return render_template("index.html", timetable=timetable, weekdays=weekdays)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        subject = request.form.get("subject", "").strip()
        teacher = request.form.get("teacher", "").strip()
        slot = request.form.get("slot", "").strip()
        day = request.form.get("day", "").strip()
        if not (subject and teacher and slot and day):
            flash("Please fill all fields")
            return redirect(url_for('add'))
        if day not in weekdays:
            flash("Invalid day selected")
            return redirect(url_for('add'))
        if is_clash(day, slot):
            flash(f"Timeslot '{slot}' on {day} is already booked!")
            return redirect(url_for('add'))
        timetable[day].append({
            "subject": subject,
            "teacher": teacher,
            "slot": slot
        })
        flash("Class added successfully!")
        return redirect(url_for('index'))
    return render_template("add.html", weekdays=weekdays)

@app.route("/remove/<day>/<slot>", methods=["POST"])
def remove(day, slot):
    if day in timetable:
        timetable[day] = [c for c in timetable[day] if c['slot'] != slot]
        flash(f"Removed class on {day} at {slot}")
    return redirect(url_for('index'))

@app.route("/bot")
def bot():
    return render_template("bot.html")

@app.route("/chat_api", methods=["POST"])
def chat_api():
    data = request.get_json(force=True)
    user_msg = data.get("message", "").lower()
    if "hello" in user_msg:
        reply = "Hello! How can I assist you with your timetable today?"
    elif "help" in user_msg:
        reply = "You can ask me about your schedule, adding/removing classes, or how to use this app."
    elif "add class" in user_msg:
        reply = "Go to 'Add Class', fill in details, and submit!"
    else:
        reply = "Sorry, I am still learning. Could you please rephrase your question?"
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)