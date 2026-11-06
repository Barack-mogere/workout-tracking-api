from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from server.models import db, Exercise, Workout, WorkoutExercise
from server.schemas import (
    ExerciseSchema,
    WorkoutSchema,
    WorkoutExerciseSchema,
    WorkoutExerciseDetailSchema
)

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database and migrations
db.init_app(app)
migrate = Migrate(app, db)


# Create schema objects for validating and serializing data.
exercise_schema = ExerciseSchema()
workout_schema = WorkoutSchema()
workout_exercise_schema = WorkoutExerciseSchema()
workout_exercise_detail_schema = WorkoutExerciseDetailSchema()


@app.route("/")
def home():
    return make_response(jsonify({
        "message": "Welcome to the Workout Tracking API"
    }), 200)


# --------------------------------------------------
# EXERCISE ROUTES
# --------------------------------------------------

@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()

    return make_response(jsonify(
        exercise_schema.dump(exercises, many=True)
    ), 200)


@app.route("/exercises", methods=["POST"])
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json(silent=True) or {})
    except ValidationError as error:
        return make_response(jsonify({
            "errors": error.messages
        }), 400)

    exercise = Exercise(**data)

    db.session.add(exercise)
    db.session.commit()

    return make_response(jsonify(
        exercise_schema.dump(exercise)
    ), 201)


@app.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return make_response(jsonify({
            "error": "Exercise not found"
        }), 404)

    return make_response(jsonify(
        exercise_schema.dump(exercise)
    ), 200)


@app.route("/exercises/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return make_response(jsonify({
            "error": "Exercise not found"
        }), 404)

    db.session.delete(exercise)
    db.session.commit()

    return make_response(jsonify({
        "message": "Exercise deleted successfully"
    }), 200)


# --------------------------------------------------
# WORKOUT ROUTES
# --------------------------------------------------

@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()

    return make_response(jsonify(
        workout_schema.dump(workouts, many=True)
    ), 200)


@app.route("/workouts", methods=["POST"])
def create_workout():
    try:
        data = workout_schema.load(request.get_json(silent=True) or {})
    except ValidationError as error:
        return make_response(jsonify({
            "errors": error.messages
        }), 400)

    workout = Workout(**data)

    db.session.add(workout)
    db.session.commit()

    return make_response(jsonify(
        workout_schema.dump(workout)
    ), 201)


@app.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return make_response(jsonify({
            "error": "Workout not found"
        }), 404)

    return make_response(jsonify(
        workout_schema.dump(workout)
    ), 200)


@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return make_response(jsonify({
            "error": "Workout not found"
        }), 404)

    db.session.delete(workout)
    db.session.commit()

    return make_response(jsonify({
        "message": "Workout deleted successfully"
    }), 200)


# --------------------------------------------------
# WORKOUT EXERCISE ROUTE
# --------------------------------------------------

@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"]
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)

    if workout is None:
        return make_response(jsonify({
            "error": "Workout not found"
        }), 404)

    if exercise is None:
        return make_response(jsonify({
            "error": "Exercise not found"
        }), 404)

    try:
        data = workout_exercise_schema.load(
            request.get_json(silent=True) or {}
        )
    except ValidationError as error:
        return make_response(jsonify({
            "errors": error.messages
        }), 400)

    workout_exercise = WorkoutExercise(
        workout=workout,
        exercise=exercise,
        **data
    )

    db.session.add(workout_exercise)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return make_response(jsonify({
            "error": "This exercise is already included in this workout."
        }), 400)

    return make_response(jsonify(
        workout_exercise_detail_schema.dump(workout_exercise)
    ), 201)


if __name__ == "__main__":
    app.run(port=5555, debug=True)