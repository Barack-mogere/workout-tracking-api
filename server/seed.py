
#!/usr/bin/env python3

from datetime import date

from server.app import app
from server.models import db, Exercise, Workout, WorkoutExercise


with app.app_context():

    # Clear existing records before inserting new seed data.
    db.session.execute(db.delete(WorkoutExercise))
    db.session.execute(db.delete(Workout))
    db.session.execute(db.delete(Exercise))
    db.session.commit()

    # Create reusable exercises.
    pushups = Exercise(
        name="Push-ups",
        category="Strength",
        equipment_needed=False
    )

    squats = Exercise(
        name="Squats",
        category="Strength",
        equipment_needed=False
    )

    bench_press = Exercise(
        name="Bench Press",
        category="Strength",
        equipment_needed=True
    )

    running = Exercise(
        name="Running",
        category="Cardio",
        equipment_needed=False
    )

    db.session.add_all([
        pushups,
        squats,
        bench_press,
        running
    ])

    db.session.commit()

    # Create sample workouts.
    workout1 = Workout(
        date=date(2026, 11, 6),
        duration_minutes=60,
        notes="Upper body strength training"
    )

    workout2 = Workout(
        date=date(2026, 11, 5),
        duration_minutes=45,
        notes="Lower body and cardio training"
    )

    db.session.add_all([workout1, workout2])
    db.session.commit()

    # Connect exercises to workouts.
    workout_exercises = [
        WorkoutExercise(
            workout=workout1,
            exercise=pushups,
            sets=3,
            reps=15
        ),
        WorkoutExercise(
            workout=workout1,
            exercise=bench_press,
            sets=4,
            reps=10
        ),
        WorkoutExercise(
            workout=workout2,
            exercise=squats,
            sets=3,
            reps=12
        ),
        WorkoutExercise(
            workout=workout2,
            exercise=running,
            duration_seconds=1200
        ),
        WorkoutExercise(
            workout=workout1,
            exercise=squats,
            sets=3,
            reps=15
        )
    ]

    db.session.add_all(workout_exercises)
    db.session.commit()

    print("Database successfully seeded!")
