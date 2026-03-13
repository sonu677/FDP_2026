from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500))
    done = db.Column(db.Boolean, default=False)

# Create Database
with app.app_context():
    db.create_all()

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# GET all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()

    result = []
    for t in tasks:
        result.append({
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "done": t.done
        })

    return jsonify(result)

# CREATE task
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    task = Task(
        title=data["title"],
        description=data.get("description", ""),
        done=data.get("done", False)
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({"message": "Task created"}), 201

# UPDATE task
@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):

    task = Task.query.get_or_404(id)
    data = request.get_json()

    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.done = data.get("done", task.done)

    db.session.commit()

    return jsonify({"message": "Task updated"})

# DELETE task
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):

    task = Task.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted"})


if __name__ == "__main__":
    app.run(debug=True)