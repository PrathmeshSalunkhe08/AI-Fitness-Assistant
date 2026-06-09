import json

class ExerciseSuggester:
    def __init__(self, json_path="exercise_module/exercise_list.json"):
        with open(json_path, "r", encoding="utf-8") as f:
            self.exercises = json.load(f)

    def _get_sets_reps(self, difficulty):
        """Personalized sets & reps logic"""
        difficulty = difficulty.lower()
        if difficulty == "beginner":
            return "3 sets × 10–12 reps"
        elif difficulty == "intermediate":
            return "4 sets × 12–15 reps"
        else:  # professional / advanced
            return "5 sets × 15–20 reps"

    def suggest_exercises(self, body_part, difficulty):
        """
        Filters exercises by body part and difficulty
        and adds personalized sets & reps.
        """
        body_part = body_part.lower()
        difficulty = difficulty.lower()

        if body_part not in self.exercises:
            return []

        results = []

        for ex in self.exercises[body_part]:
            if ex["intensity"].lower() == difficulty:
                ex_copy = ex.copy()
                ex_copy["sets_reps"] = self._get_sets_reps(difficulty)
                results.append(ex_copy)

        return results
