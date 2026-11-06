from marshmallow import Schema, fields, validates, validates_schema, ValidationError, validate


# A simple exercise representation.
# We use this when displaying exercises inside other schemas.
class ExerciseSummarySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    category = fields.Str()
    equipment_needed = fields.Bool()


# A simple workout representation.
# We use this when displaying workouts inside other schemas.
class WorkoutSummarySchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date()
    duration_minutes = fields.Int()
    notes = fields.Str(allow_none=True)


# Schema for creating and displaying exercises.
class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )

    category = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50)
    )

    equipment_needed = fields.Bool(required=True)

    # Show the workouts that contain this exercise.
    workouts = fields.List(
        fields.Nested(WorkoutSummarySchema),
        dump_only=True
    )

    @validates("name")
    def validate_name(self, value):
        if not value.strip():
            raise ValidationError("Exercise name cannot be empty.")

    @validates("category")
    def validate_category(self, value):
        if not value.strip():
            raise ValidationError("Exercise category cannot be empty.")


# Schema for displaying an exercise inside a workout exercise record.
class WorkoutExerciseDetailSchema(Schema):
    id = fields.Int(dump_only=True)
    reps = fields.Int(allow_none=True)
    sets = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)

    exercise = fields.Nested(ExerciseSummarySchema, dump_only=True)


# Schema for creating and displaying workouts.
class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)

    date = fields.Date(required=True)

    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )

    notes = fields.Str(allow_none=True)

    # Show the exercises included in this workout.
    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseDetailSchema),
        dump_only=True
    )


# Schema for adding an exercise to a workout.
class WorkoutExerciseSchema(Schema):
    reps = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1)
    )

    sets = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1)
    )

    duration_seconds = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1)
    )

    @validates_schema
    def validate_measurements(self, data, **kwargs):
        if data.get("reps") is None and data.get("duration_seconds") is None:
            raise ValidationError(
                "You must provide either reps or duration_seconds."
            )