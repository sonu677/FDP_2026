from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory storage
tasks = []
next_id = 1


def find_student(student_id):
    return next((s for s in tasks if s["id"] == student_id), None)


# GET all tasks
@app.route("/students", methods=["GET"])
def get_tasks():
    return jsonify({"students": tasks, "total": len(tasks)}), 200


# GET single task
@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = find_student(student_id)
    if not student:
        abort(404, description=f"Student {student_id} not found")
    return jsonify(student), 200


# CREATE task
@app.route("/students", methods=["POST"])
def create_student():
    global next_id
    data = request.get_json()
    if not data or not data.get("name"):
        abort(400, description="'name' field is required")

    student = {
        "id": next_id,
        "name": data["name"],
        "age": data.get("age", 0),
        "email": data.get("email", ""),
    }
    tasks.append(student)
    next_id += 1
    return jsonify(student), 201


# UPDATE student (full or partial)
@app.route("/students/<int:student_id>", methods=["PUT", "PATCH"])
def update_student(student_id):
    student = find_student(student_id)
    if not student:
        abort(404, description=f"Student {student_id} not found")

    data = request.get_json()
    if not data:
        abort(400, description="JSON body required")

    if "name" in data:
        student["name"] = data["name"]
    if "age" in data:
        student["age"] = data["age"]
    if "email" in data:
        student["email"] = data["email"]

    return jsonify(student), 200


# DELETE student
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = find_student(student_id)
    if not student:
        abort(404, description=f"Student {student_id} not found")

    tasks.remove(student)
    return jsonify({"message": f"Student {student_id} deleted successfully"}), 200


# DELETE all students
@app.route("/students", methods=["DELETE"])
def delete_all_students():
    tasks.clear()
    return jsonify({"message": "All students deleted"}), 200


@app.errorhandler(400)
@app.errorhandler(404)
def handle_error(e):
    return jsonify({"error": str(e.description)}), e.code


if __name__ == "__main__":
    app.run(debug=True, port=5000)