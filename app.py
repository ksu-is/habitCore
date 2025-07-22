
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__, static_folder="public", static_url_path="")
CORS(app)

habits = []

@app.route("/")
def serve_index():
    return send_from_directory("public", "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("public", path)

@app.route("/api/habits", methods=["GET"])
def get_habits():
    return jsonify(habits)

@app.route("/api/habits", methods=["POST"])
def add_habit():
    data = request.get_json()
    new_habit = {
        "id": int(datetime.now().timestamp() * 1000),
        "name": data.get("name"),
        "category": data.get("category", "Uncategorized"),
        "streak": 0,
        "completedToday": False,
        "badge": "",
        "message": "",
        "calendar": [False] * 7  
    }
    habits.append(new_habit)
    return jsonify(new_habit), 201

@app.route("/api/habits/<int:habit_id>/complete", methods=["POST"])
def complete_habit(habit_id):
    today_index = (datetime.today().isoweekday() % 7)
   
    for habit in habits:
        if habit["id"] == habit_id:
            if not habit["completedToday"]:
                habit["streak"] += 1
                habit["completedToday"] = True

               
                habit["calendar"][today_index] = True

            
                if habit["streak"] >= 14:
                    habit["badge"] = "🏅 Champion"
                    habit["message"] = "Unstoppable! 14-day streak!"
                elif habit["streak"] >= 7:
                    habit["badge"] = "💪 Consistent"
                    habit["message"] = "Nice! You’ve hit 7 days straight!"
                elif habit["streak"] >= 3:
                    habit["badge"] = "🔥 On Fire"
                    habit["message"] = "Keep the momentum going!"
                elif habit["streak"] >= 1:
                    habit["badge"] = "🔥 Starter Flame"
                    habit["message"] = "Great Start!"
                else:
                    habit["badge"] = ""
                    habit["message"] = "Great job! Keep it up!"
            return jsonify(habit)
    return "Habit not found", 404


@app.route("/api/reset", methods=["POST"])
def reset_habits():
    for habit in habits:
        habit["completedToday"] = False
    return "Reset complete", 200

@app.route("/api/stats", methods=["GET"])
def get_stats():
    total = len(habits)
    completed = sum(1 for h in habits if h["completedToday"])
    return jsonify({
        "completedToday": completed,
        "totalHabits": total
    })

if __name__ == "__main__":
    app.run(debug=True, port=3000)
