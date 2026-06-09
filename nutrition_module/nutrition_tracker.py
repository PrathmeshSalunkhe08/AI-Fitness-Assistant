# import pandas as pd
# from fuzzywuzzy import process

# class NutritionTracker:
#     def __init__(self, path="dataset/indian_food.csv"):
#         self.df = pd.read_csv(path)

#         # Rename columns (adjust if needed)
#         self.df.rename(columns={
#             "Dish Name": "name",
#             "Calories (kcal)": "calories",
#             "Protein (g)": "protein",
#             "Carbohydrates (g)": "carbs",
#             "Fats (g)": "fat"
#         }, inplace=True)

#         # Lowercase for matching
#         self.df["name"] = self.df["name"].astype(str).str.lower()

#     # 🔍 Live Suggestions
#     def get_suggestions(self, query):
#         query = query.lower()

#         if not query:
#             return []

#         matches = process.extract(query, self.df["name"], limit=5)

#         return [match[0] for match in matches]

#     # 🥗 Calculate Nutrition
#     def calculate_nutrition(self, food_name, quantity):
#         food_name = food_name.lower()

#         result = process.extractOne(food_name, self.df["name"])

#         if not result:
#             return None

#         # Works for both 2-value and 3-value returns
#         match = result[0]
#         score = result[1]

#         if score < 60:
#             return None

#         food_row = self.df[self.df["name"] == match]

#         if food_row.empty:
#             return None

#         food = food_row.iloc[0]

#         factor = float(quantity) / 100

#         return {
#             "food": match,
#             "calories": float(food.get("calories", 0)) * factor,
#             "protein": float(food.get("protein", 0)) * factor,
#             "carbs": float(food.get("carbs", 0)) * factor,
#             "fat": float(food.get("fat", 0)) * factor
#         }

# import pandas as pd

# class NutritionTracker:

#     def __init__(self, path="dataset/food.csv"):
#         self.df = pd.read_csv(path)

#         # Rename columns exactly as in your CSV
#         self.df.rename(columns={
#             "Dish Name": "name",
#             "Calories (kcal)": "calories",
#             "Carbohydrates (g)": "carbs",
#             "Protein (g)": "protein",
#             "Fats (g)": "fat",
#             "Free Sugar (g)": "sugar",
#             "Fibre (g)": "fiber",
#             "Sodium (mg)": "sodium",
#             "Calcium (mg)": "calcium",
#             "Iron (mg)": "iron",
#             "Vitamin C (mg)": "vitamin_c",
#             "Folate (µg)": "folate"
#         }, inplace=True)

#         self.df["name"] = self.df["name"].str.lower().str.strip()

#     # 🔍 Live search
#     def get_suggestions(self, query):
#         query = query.lower().strip()
#         results = self.df[self.df["name"].str.contains(query, na=False)]
#         return results["name"].head(10).tolist()

#     # 🥗 Nutrition calculation (values are per 100g)
#     def calculate_nutrition(self, food_name, quantity):

#         food_name = food_name.lower().strip()

#         result = self.df[self.df["name"] == food_name]

#         if result.empty:
#             return None

#         food = result.iloc[0]

#         factor = float(quantity) / 100  # since CSV is per 100g

#         return {
#             "food": food_name,
#             "calories": float(food["calories"]) * factor,
#             "carbs": float(food["carbs"]) * factor,
#             "protein": float(food["protein"]) * factor,
#             "fat": float(food["fat"]) * factor,
#             "sugar": float(food["sugar"]) * factor,
#             "fiber": float(food["fiber"]) * factor,
#             "sodium": float(food["sodium"]) * factor,
#             "calcium": float(food["calcium"]) * factor,
#             "iron": float(food["iron"]) * factor,
#             "vitamin_c": float(food["vitamin_c"]) * factor,
#             "folate": float(food["folate"]) * factor
#         }









# import pandas as pd
# from fuzzywuzzy import process

# class NutritionTracker:

#     def __init__(self, path="dataset/indian_food.csv"):
#         self.df = pd.read_csv(path)

#         # Keep original column names
#         self.df["Dish Name"] = self.df["Dish Name"].astype(str).str.lower().str.strip()

#     # 🔍 Suggestions (fuzzy allowed here)
#     def get_suggestions(self, query):

#         query = query.lower().strip()

#         if not query:
#             return []

#         matches = process.extract(query, self.df["Dish Name"], limit=5)

#         return [match[0] for match in matches]

#     # 🥗 Exact Match Calculation (NO FUZZY HERE)
#     def calculate_nutrition(self, food_name, quantity):

#         food_name = food_name.lower().strip()

#         # Exact match only
#         food_row = self.df[self.df["Dish Name"] == food_name]

#         if food_row.empty:
#             return None

#         food = food_row.iloc[0]

#         factor = float(quantity) / 100

#         return {
#             "food": food["Dish Name"],
#             "calories": float(food["Calories (kcal)"]) * factor,
#             "carbs": float(food["Carbohydrates (g)"]) * factor,
#             "protein": float(food["Protein (g)"]) * factor,
#             "fat": float(food["Fats (g)"]) * factor,
#             "sugar": float(food["Free Sugar (g)"]) * factor,
#             "fiber": float(food["Fibre (g)"]) * factor,
#             "sodium": float(food["Sodium (mg)"]) * factor,
#             "calcium": float(food["Calcium (mg)"]) * factor,
#             "iron": float(food["Iron (mg)"]) * factor,
#             "vitamin_c": float(food["Vitamin C (mg)"]) * factor,
#             "folate": float(food["Folate (µg)"]) * factor
#         }










# import pandas as pd
# from fuzzywuzzy import process

# class NutritionTracker:

#     def __init__(self, path="dataset/indian_food.csv"):
#         self.df = pd.read_csv(path)

#         # Clean Dish Name column
#         self.df["Dish Name"] = (
#             self.df["Dish Name"]
#             .astype(str)
#             .str.lower()
#             .str.strip()
#         )

#     # 🔍 Suggestions (fuzzy allowed here)
#     def get_suggestions(self, query):

#         query = query.lower().strip()

#         if not query:
#             return []

#         matches = process.extract(query, self.df["Dish Name"], limit=5)

#         return [match[0] for match in matches]

#     # 🛡 Safe float conversion (Prevents NaN crash)
#     def safe_value(self, value):
#         if pd.isna(value):
#             return 0.0
#         try:
#             return float(value)
#         except:
#             return 0.0

#     # 🥗 Exact Match Calculation (NO FUZZY HERE)
#     def calculate_nutrition(self, food_name, quantity):

#         food_name = food_name.lower().strip()

#         # 🛡 Protect against invalid quantity
#         try:
#             quantity = float(quantity)
#             if quantity <= 0:
#                 return None
#         except:
#             return None

#         # Exact match only
#         food_row = self.df[self.df["Dish Name"] == food_name]

#         if food_row.empty:
#             return None

#         food = food_row.iloc[0]

#         # Dataset is per 100g
#         factor = quantity / 100

#         return {
#             "food": food["Dish Name"],
#             "quantity": quantity,

#             "calories": self.safe_value(food["Calories (kcal)"]) * factor,
#             "carbs": self.safe_value(food["Carbohydrates (g)"]) * factor,
#             "protein": self.safe_value(food["Protein (g)"]) * factor,
#             "fat": self.safe_value(food["Fats (g)"]) * factor,
#             "sugar": self.safe_value(food["Free Sugar (g)"]) * factor,
#             "fiber": self.safe_value(food["Fibre (g)"]) * factor,
#             "sodium": self.safe_value(food["Sodium (mg)"]) * factor,
#             "calcium": self.safe_value(food["Calcium (mg)"]) * factor,
#             "iron": self.safe_value(food["Iron (mg)"]) * factor,
#             "vitamin_c": self.safe_value(food["Vitamin C (mg)"]) * factor,
#             "folate": self.safe_value(food["Folate (µg)"]) * factor
#         }





import pandas as pd
from fuzzywuzzy import process


class NutritionTracker:

    def __init__(self, path="dataset/perfect_nutrition_dataset_final.csv"):
        try:
            self.df = pd.read_csv(path)
        except:
            raise FileNotFoundError("Dataset not found")

        # Clean names
        self.df["Dish Name"] = (
            self.df["Dish Name"]
            .astype(str)
            .str.lower()
            .str.strip()
        )

    # ================= VALIDATION =================
    def _validate_input(self, food, quantity):
        if not food or not food.strip():
            return "Food name required"

        try:
            quantity = float(quantity)
        except:
            return "Invalid quantity"

        if quantity <= 0:
            return "Quantity must be > 0"

        if quantity > 2000:
            return "Quantity too large (max 2000g)"

        return None

    # ================= SAFE VALUE =================
    def safe(self, value):
        if pd.isna(value):
            return 0.0
        try:
            return float(value)
        except:
            return 0.0

    # ================= SUGGESTIONS =================
    def get_suggestions(self, query):
        query = query.lower().strip()

        if not query:
            return []

        matches = process.extract(query, self.df["Dish Name"], limit=5)

        return [m[0] for m in matches if m[1] > 60]

    # ================= FIND FOOD =================
    def _find_food(self, food_name):
        food_name = food_name.lower().strip()

        # Fuzzy match (better UX)
        result = process.extractOne(food_name, self.df["Dish Name"])

        if not result or result[1] < 60:
            return None

        match = result[0]

        row = self.df[self.df["Dish Name"] == match]

        if row.empty:
            return None

        return row.iloc[0]

    # ================= SINGLE FOOD =================
    def calculate_nutrition(self, food_name, quantity):

        error = self._validate_input(food_name, quantity)
        if error:
            return {"error": error}

        food = self._find_food(food_name)
        if food is None:
            return {"error": "Food not found"}

        quantity = float(quantity)
        factor = quantity / 100

        result = {
            "food": food["Dish Name"],
            "quantity": quantity,

            "calories": self.safe(food.get("Calories", 0)) * factor,
            "carbs": self.safe(food.get("Carbohydrates", 0)) * factor,
            "protein": self.safe(food.get("Protein", 0)) * factor,
            "fat": self.safe(food.get("Fats", 0)) * factor,
            "sugar": self.safe(food.get("Free_Sugar", 0)) * factor,
            "fiber": self.safe(food.get("Fibre", 0)) * factor,
            "sodium": self.safe(food.get("Sodium", 0)) * factor,
            "calcium": self.safe(food.get("Calcium", 0)) * factor,
            "iron": self.safe(food.get("Iron", 0)) * factor,
            "vitamin_c": self.safe(food.get("Vitamin_C", 0)) * factor,
            "folate": self.safe(food.get("Folate", 0)) * factor
        }

        return result

    # ================= MULTI FOOD (ADVANCED 🔥) =================
    def calculate_multiple(self, items):
        """
        items = [
            {"food": "rice", "qty": 100},
            {"food": "dal", "qty": 150}
        ]
        """

        total = {
            "calories": 0, "protein": 0, "carbs": 0, "fat": 0,
            "sugar": 0, "fiber": 0
        }

        breakdown = []

        for item in items:
            result = self.calculate_nutrition(item["food"], item["qty"])

            if "error" in result:
                continue

            breakdown.append(result)

            for key in total:
                total[key] += result[key]

        return {
            "total": total,
            "items": breakdown
        }