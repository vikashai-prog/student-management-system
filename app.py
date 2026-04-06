from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("database.db")
    return conn


# ✅ HOME
@app.route("/")
def home():
    db = get_db()
    students = db.execute("SELECT * FROM students").fetchall()
    db.close()
    return render_template("index.html", students=students)


# ✅ ADD
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        roll = request.form["roll"]
        name = request.form["name"]
        age = request.form["age"]

        db = get_db()

        # duplicate check
        exist = db.execute("SELECT * FROM students WHERE roll=?", (roll,)).fetchone()
        if exist:
            db.close()
            return "Roll already exists ❌"

        db.execute("INSERT INTO students VALUES (?, ?, ?)", (roll, name, age))
        db.commit()
        db.close()

        return redirect("/")

    return render_template("add.html")


# ✅ DELETE
@app.route("/delete/<roll>")
def delete(roll):
    db = get_db()
    db.execute("DELETE FROM students WHERE roll=?", (roll,))
    db.commit()
    db.close()
    return redirect("/")


# ✅ EDIT
@app.route("/edit/<roll>", methods=["GET", "POST"])
def edit(roll):
    db = get_db()

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]

        db.execute("UPDATE students SET name=?, age=? WHERE roll=?", (name, age, roll))
        db.commit()
        db.close()
        return redirect("/")

    student = db.execute("SELECT * FROM students WHERE roll=?", (roll,)).fetchone()
    db.close()
    return render_template("edit.html", student=student)

from flask import jsonify

# 🤖 CHATBOT
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data["message"].lower()

    db = get_db()

    # 🔹 Total students
    if "total" in msg:
        count = db.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        db.close()
        return jsonify({"reply": f"Total students are {count}"})

    # 🔹 Show all students
    elif "show" in msg or "list" in msg:
        students = db.execute("SELECT name FROM students").fetchall()
        db.close()
        names = [s[0] for s in students]
        return jsonify({"reply": "Students: " + ", ".join(names)})

    # 🔹 Find student
    elif "find" in msg:
        name = msg.split("find")[-1].strip()
        student = db.execute("SELECT * FROM students WHERE name LIKE ?", (f"%{name}%",)).fetchone()
        db.close()

        if student:
            return jsonify({"reply": f"{student[1]} is {student[2]} years old"})
        else:
            return jsonify({"reply": "Student not found"})

    # 🔹 Default
    db.close()
    return jsonify({"reply": "Try: total students / show students / find name"})


app.run(debug=True)