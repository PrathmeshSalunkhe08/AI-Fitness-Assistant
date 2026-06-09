
from flask import (
    Flask, render_template, request,
    redirect, session, url_for,
    send_file, flash, jsonify, Response
)

from exercise_module.exercise_suggester import ExerciseSuggester
from diet_module.diet_recommender import DietRecommender
from diet_module.pdf_generator import generate_diet_pdf


from module_posture.posture_stream import generate_frames
from module_posture.posture_state import posture_state
from nutrition_module.nutrition_tracker import NutritionTracker



import db

app = Flask(__name__)
app.secret_key = "ai_fitness_secret"

# ================= POSTURE STATUS API =================
@app.route('/posture_status')
def posture_status_api():
    return jsonify(posture_state)

# ================= DASHBOARD =================
@app.route('/')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    return redirect(url_for('login'))

# ================= REGISTER =================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if db.email_exists(email):
            flash("Email already exists", "error")
            return redirect('/register')

        db.register_user(name, email, password)
        flash("Registration successful. Please login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

# ================= LOGIN =================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = db.login_user(email, password)
        if user:
            session['user'] = user[1]
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password.", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

# ================= LOGOUT =================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ================= DIET =================
# @app.route('/diet', methods=['GET', 'POST'])
# def diet():
#     if 'user' not in session:
#         return redirect('/login')

#     daily = weekly = calories = explanation = None

#     if request.method == 'POST':
#         user_data = {
#             "age": int(request.form['age']),
#             "gender": request.form['gender'],
#             "height": int(request.form['height']),
#             "weight": int(request.form['weight']),
#             "activity": request.form['activity'],
#             "goal": request.form['goal']
#         }

#         mode = request.form['mode']
#         rec = DietRecommender()

#         if mode == "daily":
#             calories, daily, explanation = rec.daily_plan(user_data)
#             session['diet_pdf_data'] = {"type": "daily", "user": user_data}

#         elif mode == "weekly":
#             weekly = rec.weekly_plan(user_data)
#             session['diet_pdf_data'] = {"type": "weekly", "user": user_data}

#     return render_template(
#         "diet.html",
#         daily=daily,
#         weekly=weekly,
#         calories=calories,
#         explanation=explanation
#     )






@app.route('/diet', methods=['GET', 'POST'])
def diet():
    if 'user' not in session:
        return redirect('/login')

    daily = weekly = calories = explanation = None

    if request.method == 'POST':
        try:
            user_data = {
                "age": int(request.form['age']),
                "gender": request.form['gender'],
                "height": int(request.form['height']),
                "weight": int(request.form['weight']),
                "activity": request.form['activity'],
                "goal": request.form['goal'],
                "diet_pref": request.form['diet_pref'],
                "health_condition": request.form.get('health_condition', 'none')
            }

            mode = request.form['mode']
            rec = DietRecommender()

            if mode == "daily":
                calories, daily, explanation = rec.daily_plan(user_data)
                session['diet_pdf_data'] = {"type": "daily", "user": user_data}

            elif mode == "weekly":
                weekly = rec.weekly_plan(user_data)
                session['diet_pdf_data'] = {"type": "weekly", "user": user_data}

        # except Exception as e:
        #     flash("Error generating diet plan. Please check inputs.", "error")
        except Exception as e:
            print("ERROR:", e)
            flash(f"Error: {str(e)}", "error")

    return render_template(
        "diet.html",
        daily=daily,
        weekly=weekly,
        calories=calories,
        explanation=explanation
    )





# ================= DIET PDF =================
@app.route('/diet/pdf')
def diet_pdf():
    if 'diet_pdf_data' not in session:
        return redirect('/diet')

    rec = DietRecommender()
    user = session['diet_pdf_data']['user']
    mode = session['diet_pdf_data']['type']

    lines = []

    if mode == "daily":
        calories, plan, _ = rec.daily_plan(user)
        lines.append(f"Daily Calories: {calories} kcal\n")
        for meal, foods in plan.items():
            lines.append(meal)
            for f in foods:
                lines.append(f"- {f['name']} ({f['calories']} kcal)")
            lines.append("")
    else:
        week = rec.weekly_plan(user)
        for day, meals in week.items():
            lines.append(day)
            for meal, foods in meals.items():
                lines.append(f"  {meal}:")
                for f in foods:
                    lines.append(f"   - {f['name']} ({f['calories']} kcal)")
            lines.append("")

    generate_diet_pdf(
        "diet_plan.pdf",
        "AI Fitness Assistant - Diet Plan",
        session['user'],
        lines
    )

    return send_file("diet_plan.pdf", as_attachment=True)

# ================= EXERCISE SUGGESTION =================
@app.route('/exercise', methods=['GET', 'POST'])
def exercise():
    if 'user' not in session:
        return redirect('/login')

    exercises = []

    if request.method == 'POST':
        body_part = request.form['body_part'].lower()
        difficulty = request.form['difficulty'].lower()
        suggester = ExerciseSuggester()
        exercises = suggester.suggest_exercises(body_part, difficulty)

    return render_template('exercise1.html', exercises=exercises)


# ================= POSTURE DETECTION =================
@app.route('/posture', methods=['GET', 'POST'])
def posture():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        posture_state["exercise"] = request.form["exercise"]
        posture_state["reps"] = 0
        posture_state["wrong"] = False
        posture_state["feedback"] = ""
        posture_state["active"] = True
        return redirect(url_for('posture_camera'))

    return render_template("posture_select.html")

@app.route('/posture/stop')
def stop_posture():
    posture_state["active"] = False
    posture_state["exercise"] = None
    posture_state["reps"] = 0
    posture_state["wrong"] = False
    posture_state["feedback"] = ""
    return redirect(url_for("posture"))

@app.route('/posture/camera')
def posture_camera():
    return render_template("posture_camera.html")

@app.route('/video_feed')
def video_feed():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

# ================= NUTRITION TRACKER =================
from flask import render_template, request, jsonify
from nutrition_module.nutrition_tracker import NutritionTracker
tracker = NutritionTracker()

@app.route("/nutrition")
def nutrition():
    return render_template("nutrition.html")

@app.route("/search_food", methods=["POST"])
def search_food():
    query = request.json.get("query")
    suggestions = tracker.get_suggestions(query)
    return jsonify(suggestions)


@app.route("/calculate_nutrition", methods=["POST"])
def calculate_nutrition():
    data = request.json
    food = data["food"]
    quantity = float(data["quantity"])

    result = tracker.calculate_nutrition(food, quantity)

    # if not result:
    #     return jsonify({"error": "Food not found"})
    
    if "error" in result:
        return jsonify(result)

    return jsonify(result)





# ====================== ChatBot ======================
# ====================== ChatBot (MySQL Version) ======================
from ai_module.hf_chat import ask_ai
from db import (
    get_or_create_session,
    save_message,
    get_user_sessions,
    get_session_messages,
    delete_session,
    delete_message,
    create_new_session
)
import markdown

# Main Chat Page (Sidebar)
@app.route("/chat")
def chat_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    sessions = get_user_sessions(session['user_id'])
    return render_template("ai_chat.html", sessions=sessions)


@app.route("/new_chat")
def new_chat():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    session_id = create_new_session(session['user_id'])
    return redirect(url_for("view_chat", session_id=session_id))


# Send Message
@app.route("/ai_chat", methods=["POST"])
def ai_chat():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user_message = request.form["message"]

    # Get or create today's session
    session_id = get_or_create_session(user_id)

    # Fetch previous messages for history
    previous_messages = get_session_messages(session_id)
    history = []
    for msg in previous_messages:
        # msg structure from db.py: (id, sender, message)
        role = "assistant" if msg[1] == "ai" else "user"
        history.append({"role": role, "content": msg[2]})

    # Get AI reply
    raw_response = ask_ai(user_message, history)
    ai_response = markdown.markdown(raw_response)

    # Save messages in DB
    save_message(session_id, "user", user_message)
    save_message(session_id, "ai", ai_response)

    return redirect(url_for("view_chat", session_id=session_id))


# View Specific Day Chat
@app.route("/chat/<int:session_id>")
def view_chat(session_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    messages = get_session_messages(session_id)
    return render_template("chat_view.html", messages=messages, session_id=session_id)


# Delete Full Day
@app.route("/delete_session/<int:session_id>")
def remove_session(session_id):
    delete_session(session_id)
    return redirect(url_for("chat_page"))


# Delete Single Message
@app.route("/delete_message/<int:message_id>")
def remove_message(message_id):
    delete_message(message_id)
    return redirect(request.referrer)
# ================about us and contact us =================
@app.route('/about')
def about():
    if 'user' not in session:
        return redirect('/login')
    return render_template('about.html')


@app.route('/contact')
def contact():
    if 'user' not in session:
        return redirect('/login')
    return render_template('contact.html')

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
