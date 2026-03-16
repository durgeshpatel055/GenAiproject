@@ -65,5 +65,6 @@ def update_workout_plan(original_plan: dict, feedback: str) -> dict:
            if "429" in str(exc) and delay is not None:
                time.sleep(delay)
                continue
            raise RuntimeError(f"Gemini Pro error during plan update: {exc}") from exc
    raise RuntimeError(f"Gemini Pro error during plan update: {last_exc}") from last_exc
            break  # Non-429 — fall through to fallback
    # Quota exhausted — return the original plan unchanged rather than a 502
    return original_plan
