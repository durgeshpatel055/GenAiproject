@@ -22,6 +22,95 @@
_MAX_RETRIES = 3
_RETRY_DELAYS = [5, 15, 30]  # seconds between retries on 429

# ---------------------------------------------------------------------------
# Static fallback plans — returned when the API quota is exhausted so the
# page still loads instead of returning a 502.
# ---------------------------------------------------------------------------
_FALLBACK_PLAN_BASE = {
    "Day 1": {
        "focus": "Full-Body Strength",
        "warmup": "5 min brisk walk + arm circles and leg swings",
        "exercises": [
            {"name": "Bodyweight Squats", "sets": 3, "reps": "15"},
            {"name": "Push-Ups", "sets": 3, "reps": "12"},
            {"name": "Dumbbell Rows", "sets": 3, "reps": "12 each side"},
            {"name": "Plank Hold", "sets": 3, "reps": "30 seconds"},
        ],
        "cooldown": "5 min full-body stretch focusing on quads, chest and shoulders",
    },
    "Day 2": {
        "focus": "Active Recovery & Mobility",
        "warmup": "5 min easy walk",
        "exercises": [
            {"name": "Cat-Cow Stretch", "sets": 2, "reps": "10"},
            {"name": "Hip Circle Rotations", "sets": 2, "reps": "10 each side"},
            {"name": "Child's Pose", "sets": 3, "reps": "30 seconds"},
            {"name": "Seated Hamstring Stretch", "sets": 2, "reps": "30 seconds each"},
        ],
        "cooldown": "Deep breathing and foam rolling if available",
    },
    "Day 3": {
        "focus": "Lower Body",
        "warmup": "5 min jumping jacks + hip flexor stretch",
        "exercises": [
            {"name": "Lunges", "sets": 3, "reps": "12 each leg"},
            {"name": "Glute Bridges", "sets": 3, "reps": "15"},
            {"name": "Wall Sit", "sets": 3, "reps": "45 seconds"},
            {"name": "Calf Raises", "sets": 3, "reps": "20"},
        ],
        "cooldown": "5 min standing and seated leg stretches",
    },
    "Day 4": {
        "focus": "Upper Body Push",
        "warmup": "5 min shoulder rolls + light band pull-aparts",
        "exercises": [
            {"name": "Incline Push-Ups", "sets": 3, "reps": "15"},
            {"name": "Dumbbell Shoulder Press", "sets": 3, "reps": "12"},
            {"name": "Tricep Dips", "sets": 3, "reps": "12"},
            {"name": "Lateral Raises", "sets": 3, "reps": "15"},
        ],
        "cooldown": "Chest opener stretch — clasp hands behind back and lift arms",
    },
    "Day 5": {
        "focus": "Cardio & Core",
        "warmup": "3 min march in place + dynamic stretches",
        "exercises": [
            {"name": "High Knees", "sets": 3, "reps": "30 seconds"},
            {"name": "Mountain Climbers", "sets": 3, "reps": "30 seconds"},
            {"name": "Bicycle Crunches", "sets": 3, "reps": "20"},
            {"name": "Burpees", "sets": 3, "reps": "10"},
        ],
        "cooldown": "5 min walking cool-down + deep abdominal breathing",
    },
    "Day 6": {
        "focus": "Upper Body Pull",
        "warmup": "5 min arm swings + scapular squeezes",
        "exercises": [
            {"name": "Dumbbell Bicep Curls", "sets": 3, "reps": "12"},
            {"name": "Bent-Over Rows", "sets": 3, "reps": "12"},
            {"name": "Resistance Band Pull-Aparts", "sets": 3, "reps": "15"},
            {"name": "Superman Hold", "sets": 3, "reps": "30 seconds"},
        ],
        "cooldown": "Doorway chest stretch and lat side stretch",
    },
    "Day 7": {
        "focus": "Rest & Light Activity",
        "warmup": "Gentle 10 min walk outdoors",
        "exercises": [
            {"name": "Yoga Sun Salutation", "sets": 2, "reps": "5 flows"},
            {"name": "Standing Hip Flexor Stretch", "sets": 2, "reps": "30 seconds each"},
            {"name": "Thoracic Spine Rotation", "sets": 2, "reps": "10 each side"},
        ],
        "cooldown": "10 min guided meditation or relaxed breathing",
    },
}


def _get_fallback_plan(name: str, goal: str, intensity: str) -> dict:
    """Return a copy of the static fallback plan (quota-safe)."""
    import copy
    return copy.deepcopy(_FALLBACK_PLAN_BASE)


def _extract_json(text: str) -> dict:
    """Strip markdown fences and parse the first JSON object in the response."""
@@ -88,5 +177,8 @@ def generate_workout_gemini(name: str, age: int, weight: float, goal: str, inten
            if "429" in str(exc) and delay is not None:
                time.sleep(delay)
                continue
            raise RuntimeError(f"Gemini Pro error during plan generation: {exc}") from exc
    raise RuntimeError(f"Gemini Pro error during plan generation: {last_exc}") from last_exc
            # Non-429 error — fall through to static plan
            break
    # Quota exhausted or unrecoverable error — return static fallback so the
    # page still loads instead of returning a 502.
    return _get_fallback_plan(name, goal, intensity)
