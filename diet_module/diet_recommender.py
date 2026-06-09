# import pandas as pd
# import random


# class DietRecommender:
#     def __init__(self, path="dataset/indian_food.csv"):
#         self.df = pd.read_csv(path)

#         # Rename columns for consistency
#         self.df.rename(columns={
#             "Dish Name": "name",
#             "Calories (kcal)": "calories",
#             "Protein (g)": "protein",
#             "Carbohydrates (g)": "carbs",
#             "Fats (g)": "fat",
#             "Fibre (g)": "fiber"
#         }, inplace=True)

#         self.df.dropna(inplace=True)

#     # ---------- AGE CATEGORY ----------
#     def age_category(self, age):
#         if age < 16:
#             return "child"
#         elif age < 19:
#             return "teen"
#         else:
#             return "adult"

#     # ---------- BMR (Mifflin-St Jeor Formula) ----------
#     def bmr(self, gender, weight, height, age):
#         if gender.lower() == "male":
#             return 10 * weight + 6.25 * height - 5 * age + 5
#         else:
#             return 10 * weight + 6.25 * height - 5 * age - 161

#     # ---------- DAILY CALORIES WITH AGE SAFETY ----------
#     def daily_calories(self, bmr, activity, goal, age):
#         factors = {
#             "sedentary": 1.2,
#             "light": 1.375,
#             "moderate": 1.55,
#             "active": 1.725
#         }

#         calories = bmr * factors.get(activity, 1.2)
#         category = self.age_category(age)

#         # 🔒 AGE-BASED SAFETY RULES
#         if category == "child":
#             # No weight loss or aggressive gain
#             return max(int(calories), 1600)

#         if category == "teen":
#             if goal == "loss":
#                 calories -= 200
#             elif goal == "gain":
#                 calories += 200
#             return max(int(calories), 1500)

#         # Adult logic
#         if goal == "loss":
#             calories -= 400
#         elif goal == "gain":
#             calories += 300

#         return max(int(calories), 1200)

#     # ---------- DAILY DIET PLAN ----------
#     def daily_plan(self, user):
#         bmr_value = self.bmr(
#             user["gender"],
#             user["weight"],
#             user["height"],
#             user["age"]
#         )

#         daily_cal = self.daily_calories(
#             bmr_value,
#             user["activity"],
#             user["goal"],
#             user["age"]
#         )

#         # Meal-wise calorie distribution
#         meals = {
#             "Breakfast": daily_cal * 0.25,
#             "Lunch": daily_cal * 0.30,
#             "Snack": daily_cal * 0.15,
#             "Dinner": daily_cal * 0.30
#         }

#         plan = {}

#         for meal, meal_cal in meals.items():
#             # Filter foods by calorie range
#             options = self.df[
#                 (self.df["calories"] <= meal_cal) &
#                 (self.df["calories"] >= meal_cal * 0.4)
#             ]

#             # Goal-based sorting
#             if user["goal"] == "gain":
#                 options = options.sort_values("protein", ascending=False)
#             elif user["goal"] == "loss":
#                 options = options.sort_values("calories")

#             # Fallback if dataset filter is too strict
#             if len(options) < 2:
#                 options = self.df.sample(5)

#             plan[meal] = options.sample(2).to_dict(orient="records")

#         explanation = (
#             "Diet plan is generated using Mifflin-St Jeor BMR formula, "
#             "activity level multiplier, age-based safety rules, "
#             "and goal-based food selection from an Indian nutrition dataset."
#         )

#         return daily_cal, plan, explanation

#     # ---------- WEEKLY DIET PLAN ----------
#     def weekly_plan(self, user):
#         week = {}

#         for day in [
#             "Monday", "Tuesday", "Wednesday",
#             "Thursday", "Friday", "Saturday", "Sunday"
#         ]:
#             _, daily_plan, _ = self.daily_plan(user)
#             week[day] = daily_plan

#         return week
























# import pandas as pd


# class DietRecommender:
#     def __init__(self, path="dataset/Nutrition_Data.csv"):
#         try:
#             self.df = pd.read_csv(path)
#         except Exception:
#             raise FileNotFoundError(f"Dataset not found at {path}")

#         # Standardize columns
#         self.df.rename(columns={
#             "Dish Name": "name",
#             "Calories (kcal)": "calories",
#             "Protein (g)": "protein",
#             "Carbohydrates (g)": "carbs",
#             "Fats (g)": "fat",
#             "Fibre (g)": "fiber"
#         }, inplace=True)

#         required_cols = ["name", "calories", "protein", "carbs", "fat"]
#         self.df.dropna(subset=required_cols, inplace=True)
#         self.df.reset_index(drop=True, inplace=True)

#     # ================= BMI =================
#     def calculate_bmi(self, weight, height):
#         height_m = height / 100
#         bmi = weight / (height_m ** 2)
#         return round(bmi, 2)

#     def bmi_category(self, bmi):
#         if bmi < 18.5:
#             return "Underweight"
#         elif bmi < 24.9:
#             return "Normal"
#         elif bmi < 29.9:
#             return "Overweight"
#         return "Obese"

#     # ================= BMR =================
#     def calculate_bmr(self, gender, weight, height, age):
#         if gender.lower() == "male":
#             return 10 * weight + 6.25 * height - 5 * age + 5
#         return 10 * weight + 6.25 * height - 5 * age - 161

#     # ================= CALORIES =================
#     def calculate_daily_calories(self, bmr, activity, goal):
#         factors = {
#             "sedentary": 1.2,
#             "light": 1.375,
#             "moderate": 1.55,
#             "active": 1.725
#         }

#         calories = bmr * factors.get(activity, 1.2)

#         if goal == "loss":
#             calories -= 400
#         elif goal == "gain":
#             calories += 300

#         return max(int(calories), 1200)

#     # ================= FOOD SELECTION =================
#     def _select_meal_items(self, meal_cal, goal, used):
#         lower = meal_cal * 0.5
#         upper = meal_cal * 1.1

#         options = self.df[
#             (self.df["calories"] >= lower) &
#             (self.df["calories"] <= upper)
#         ]

#         options = options[~options["name"].isin(used)]

#         if goal == "gain":
#             options = options.sort_values("protein", ascending=False)
#         elif goal == "loss":
#             options = options.sort_values("calories")

#         if len(options) == 0:
#             options = self.df.sample(min(5, len(self.df)))

#         selected = options.sample(min(2, len(options)))
#         return selected.to_dict(orient="records")

#     # ================= DAILY PLAN =================
#     def daily_plan(self, user):
#         age = int(user["age"])
#         weight = float(user["weight"])
#         height = float(user["height"])
#         gender = user["gender"]
#         activity = user["activity"]
#         goal = user["goal"]

#         bmi = self.calculate_bmi(weight, height)
#         bmi_status = self.bmi_category(bmi)

#         bmr = self.calculate_bmr(gender, weight, height, age)
#         daily_cal = self.calculate_daily_calories(bmr, activity, goal)

#         meal_ratio = {
#             "Breakfast": 0.25,
#             "Lunch": 0.30,
#             "Snack": 0.15,
#             "Dinner": 0.30
#         }

#         plan = {}
#         used_foods = set()

#         for meal, ratio in meal_ratio.items():
#             meal_cal = daily_cal * ratio
#             items = self._select_meal_items(meal_cal, goal, used_foods)

#             for i in items:
#                 used_foods.add(i["name"])

#             plan[meal] = items

#         explanation = (
#             f"BMI: {bmi} ({bmi_status}). "
#             f"Calories calculated using Mifflin-St Jeor formula "
#             f"and adjusted for activity & goal."
#         )

#         return daily_cal, plan, explanation

#     # ================= WEEKLY PLAN =================
#     def weekly_plan(self, user):
#         week = {}
#         for day in ["Monday","Tuesday","Wednesday",
#                     "Thursday","Friday","Saturday","Sunday"]:
#             _, plan, _ = self.daily_plan(user)
#             week[day] = plan
#         return week



# import pandas as pd
# import random


# class DietRecommender:
#     def __init__(self, path="dataset/Nutrition_Data.csv"):
#         try:
#             self.df = pd.read_csv(path)
#         except Exception:
#             raise FileNotFoundError(f"Dataset not found at {path}")

#         # Normalize column names safely
#         self.df.columns = self.df.columns.str.strip()

#         self.df.rename(columns={
#             "Food_Name": "name",
#             "Calories": "calories",
#             "Protein": "protein",
#             "Carbohydrates": "carbs",
#             "Fats": "fat",
#             "Fibre": "fiber",
#             "Category": "category"
#         }, inplace=True)

#         # 🔥 AUTO FIX: If category missing → create it
#         if "category" not in self.df.columns:
#             categories = ["Breakfast", "Lunch", "Dinner", "Snack"]
#             self.df["category"] = [random.choice(categories) for _ in range(len(self.df))]

#         # 🔥 FIX: Standardize category values
#         self.df["category"] = self.df["category"].astype(str).str.strip().str.capitalize()

#         required_cols = ["name", "calories", "protein", "carbs", "fat", "category"]
#         self.df.dropna(subset=required_cols, inplace=True)
#         self.df.reset_index(drop=True, inplace=True)

#         # DEBUG (remove later)
#         print("Columns:", self.df.columns)
#         print("Categories:", self.df["category"].unique())

#     # ================= BMI =================
#     def calculate_bmi(self, weight, height):
#         return round(weight / ((height / 100) ** 2), 2)

#     def bmi_category(self, bmi):
#         if bmi < 18.5:
#             return "Underweight"
#         elif bmi < 24.9:
#             return "Normal"
#         elif bmi < 29.9:
#             return "Overweight"
#         return "Obese"

#     # ================= BMR =================
#     def calculate_bmr(self, gender, weight, height, age):
#         if gender.lower() == "male":
#             return 10 * weight + 6.25 * height - 5 * age + 5
#         return 10 * weight + 6.25 * height - 5 * age - 161

#     # ================= CALORIES =================
#     def calculate_daily_calories(self, bmr, activity, goal):
#         factors = {
#             "sedentary": 1.2,
#             "light": 1.375,
#             "moderate": 1.55,
#             "active": 1.725
#         }

#         calories = bmr * factors.get(activity, 1.2)

#         if goal == "loss":
#             calories -= 400
#         elif goal == "gain":
#             calories += 300

#         return max(int(calories), 1200)

#     # ================= FILTER =================
#     def _filter_foods(self, meal_type, lower, upper, goal, used_foods):
#         options = self.df[
#             (self.df["category"].str.lower() == meal_type.lower()) &
#             (self.df["calories"] >= lower) &
#             (self.df["calories"] <= upper)
#         ]

#         options = options[~options["name"].isin(used_foods)]

#         if goal == "gain":
#             options = options[options["protein"] >= 8]
#             options = options.sort_values("protein", ascending=False)

#         elif goal == "loss":
#             options = options[options["fat"] <= 12]
#             options = options.sort_values("calories")

#         return options

#     # ================= FALLBACK =================
#     def _fallback(self, meal_type):
#         options = self.df[self.df["category"].str.lower() == meal_type.lower()]
#         return options.sample(min(2, len(options))).to_dict(orient="records")

#     # ================= GENERATE MEAL =================
#     def _generate_meal(self, meal_type, meal_cal, goal, used_foods):
#         lower = meal_cal * 0.5
#         upper = meal_cal * 1.1

#         options = self._filter_foods(meal_type, lower, upper, goal, used_foods)

#         if len(options) == 0:
#             return self._fallback(meal_type)

#         selected = options.sample(min(2, len(options))).to_dict(orient="records")

#         for item in selected:
#             used_foods.add(item["name"])

#         return selected

#     # ================= DAILY PLAN =================
#     def daily_plan(self, user):
#         bmi = self.calculate_bmi(user["weight"], user["height"])
#         bmi_status = self.bmi_category(bmi)

#         bmr = self.calculate_bmr(
#             user["gender"], user["weight"], user["height"], user["age"]
#         )

#         daily_cal = self.calculate_daily_calories(
#             bmr, user["activity"], user["goal"]
#         )

#         meal_distribution = {
#             "Breakfast": 0.25,
#             "Lunch": 0.30,
#             "Snack": 0.15,
#             "Dinner": 0.30
#         }

#         plan = {}
#         used_foods = set()

#         for meal, ratio in meal_distribution.items():
#             plan[meal] = self._generate_meal(
#                 meal,
#                 daily_cal * ratio,
#                 user["goal"],
#                 used_foods
#             )

#         explanation = (
#             f"BMI: {bmi} ({bmi_status}) | "
#             f"Calories: {daily_cal} kcal | "
#             f"Goal: {user['goal'].upper()}"
#         )

#         return daily_cal, plan, explanation

#     # ================= WEEKLY =================
#     def weekly_plan(self, user):
#         week = {}
#         for day in ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]:
#             _, plan, _ = self.daily_plan(user)
#             week[day] = plan
#         return week





# import pandas as pd
# import random


# class DietRecommender:
#     def __init__(self, path="dataset/Nutrition_Data.csv"):
#         try:
#             self.df = pd.read_csv(path)
#         except Exception:
#             raise FileNotFoundError(f"Dataset not found at {path}")

#         # Clean column names
#         self.df.columns = self.df.columns.str.strip()

#         self.df.rename(columns={
#             "Food_Name": "name",
#             "Calories": "calories",
#             "Protein": "protein",
#             "Carbohydrates": "carbs",
#             "Fats": "fat",
#             "Fibre": "fiber",
#             "Category": "category"
#         }, inplace=True)

#         # If category missing → assign safely
#         if "category" not in self.df.columns:
#             categories = ["Breakfast", "Lunch", "Dinner", "Snack"]
#             self.df["category"] = [random.choice(categories) for _ in range(len(self.df))]

#         # Normalize values
#         self.df["category"] = self.df["category"].astype(str).str.strip().str.capitalize()

#         required = ["name", "calories", "protein", "carbs", "fat", "category"]
#         self.df.dropna(subset=required, inplace=True)
#         self.df.reset_index(drop=True, inplace=True)

#     # ================= VALIDATION =================
#     def _validate_user(self, user):
#         if user["age"] < 5 or user["age"] > 100:
#             raise ValueError("Invalid age")

#         if user["weight"] < 20 or user["weight"] > 200:
#             raise ValueError("Invalid weight")

#         if user["height"] < 80 or user["height"] > 250:
#             raise ValueError("Invalid height")

#     # ================= BMI =================
#     def calculate_bmi(self, weight, height):
#         return round(weight / ((height / 100) ** 2), 2)

#     def bmi_category(self, bmi):
#         if bmi < 18.5:
#             return "Underweight"
#         elif bmi < 24.9:
#             return "Normal"
#         elif bmi < 29.9:
#             return "Overweight"
#         return "Obese"

#     # ================= BMR =================
#     def calculate_bmr(self, gender, weight, height, age):
#         if gender.lower() == "male":
#             return 10 * weight + 6.25 * height - 5 * age + 5
#         return 10 * weight + 6.25 * height - 5 * age - 161

#     # ================= CALORIES =================
#     def calculate_daily_calories(self, bmr, activity, goal):
#         factors = {
#             "sedentary": 1.2,
#             "light": 1.375,
#             "moderate": 1.55,
#             "active": 1.725
#         }

#         calories = bmr * factors.get(activity, 1.2)

#         if goal == "loss":
#             calories -= 400
#             return max(int(calories), 1200)

#         elif goal == "gain":
#             calories += 300
#             return min(int(calories), 4000)

#         return int(calories)

#     # ================= FILTER =================
#     def _filter_foods(self, meal_type, lower, upper, goal, used_foods):
#         options = self.df[
#             (self.df["category"].str.lower().str.contains(meal_type.lower())) &
#             (self.df["calories"] >= lower) &
#             (self.df["calories"] <= upper)
#         ]

#         # Remove duplicates
#         options = options[~options["name"].isin(used_foods)]

#         # 🔥 STRICT RULES
#         if goal == "loss":
#             options = options[(options["fat"] <= 10)]
#             options = options.sort_values("calories")

#         elif goal == "gain":
#             options = options[(options["protein"] >= 10)]
#             options = options.sort_values("protein", ascending=False)

#         else:  # maintain
#             options = options[(options["protein"] >= 5)]

#         return options

#     # ================= FALLBACK =================
#     def _fallback(self, meal_type):
#         options = self.df[
#             self.df["category"].str.lower().str.contains(meal_type.lower())
#         ]

#         if len(options) == 0:
#             return self.df.sample(2).to_dict(orient="records")

#         return options.sample(min(2, len(options))).to_dict(orient="records")

#     # ================= GENERATE MEAL =================
#     def _generate_meal(self, meal_type, meal_cal, goal, used_foods):
#         lower = meal_cal * 0.5
#         upper = meal_cal * 1.1

#         options = self._filter_foods(meal_type, lower, upper, goal, used_foods)

#         if len(options) < 2:
#             return self._fallback(meal_type)

#         selected = options.sample(2).to_dict(orient="records")

#         for item in selected:
#             used_foods.add(item["name"])

#         return selected

#     # ================= DAILY PLAN =================
#     def daily_plan(self, user):
#         self._validate_user(user)

#         bmi = self.calculate_bmi(user["weight"], user["height"])
#         bmi_status = self.bmi_category(bmi)

#         bmr = self.calculate_bmr(
#             user["gender"], user["weight"], user["height"], user["age"]
#         )

#         daily_cal = self.calculate_daily_calories(
#             bmr, user["activity"], user["goal"]
#         )

#         meal_distribution = {
#             "Breakfast": 0.25,
#             "Lunch": 0.30,
#             "Snack": 0.15,
#             "Dinner": 0.30
#         }

#         plan = {}
#         used_foods = set()

#         for meal, ratio in meal_distribution.items():
#             plan[meal] = self._generate_meal(
#                 meal,
#                 daily_cal * ratio,
#                 user["goal"],
#                 used_foods
#             )

#         explanation = (
#             f"BMI: {bmi} ({bmi_status}) | "
#             f"Calories: {daily_cal} kcal | "
#             f"Goal: {user['goal'].upper()} | "
#             f"Strict diet rules applied (protein/fat control)."
#         )

#         return daily_cal, plan, explanation

#     # ================= WEEKLY PLAN =================
#     def weekly_plan(self, user):
#         week = {}
#         used_global = set()

#         for day in [
#             "Monday","Tuesday","Wednesday",
#             "Thursday","Friday","Saturday","Sunday"
#         ]:
#             _, plan, _ = self.daily_plan(user)

#             # Avoid repetition across week
#             for meal in plan:
#                 unique = []
#                 for item in plan[meal]:
#                     if item["name"] not in used_global:
#                         unique.append(item)
#                         used_global.add(item["name"])

#                 if len(unique) < 2:
#                     unique.extend(self._fallback(meal))

#                 plan[meal] = unique[:2]

#             week[day] = plan

#         return week
















# import pandas as pd
# import random


# class DietRecommender:
#     def __init__(self, path="dataset/Nutrition_Data.csv"):
#         try:
#             self.df = pd.read_csv(path)
#         except Exception:
#             raise FileNotFoundError(f"Dataset not found at {path}")

#         # Clean column names
#         self.df.columns = self.df.columns.str.strip()

#         self.df.rename(columns={
#             "Food_Name": "name",
#             "Calories": "calories",
#             "Protein": "protein",
#             "Carbohydrates": "carbs",
#             "Fats": "fat",
#             "Fibre": "fiber",
#             "Category": "category"
#         }, inplace=True)

#         # 🔥 ADD THIS (IMPORTANT)
#         if "diet_type" not in self.df.columns:
#             self.df["diet_type"] = "mixed"

#         self.df["diet_type"] = self.df["diet_type"].astype(str).str.lower().str.strip()

#         # Category fix
#         if "category" not in self.df.columns:
#             categories = ["Breakfast", "Lunch", "Dinner", "Snack"]
#             self.df["category"] = [random.choice(categories) for _ in range(len(self.df))]

#         self.df["category"] = self.df["category"].astype(str).str.strip().str.capitalize()

#         required = ["name", "calories", "protein", "carbs", "fat", "category", "diet_type"]
#         self.df.dropna(subset=required, inplace=True)
#         self.df.reset_index(drop=True, inplace=True)

#     # ================= VALIDATION =================
#     def _validate_user(self, user):
#         if user["age"] < 5 or user["age"] > 100:
#             raise ValueError("Invalid age")

#         if user["weight"] < 20 or user["weight"] > 200:
#             raise ValueError("Invalid weight")

#         if user["height"] < 80 or user["height"] > 250:
#             raise ValueError("Invalid height")

#     # ================= BMI =================
#     def calculate_bmi(self, weight, height):
#         return round(weight / ((height / 100) ** 2), 2)

#     def bmi_category(self, bmi):
#         if bmi < 18.5:
#             return "Underweight"
#         elif bmi < 24.9:
#             return "Normal"
#         elif bmi < 29.9:
#             return "Overweight"
#         return "Obese"

#     # ================= BMR =================
#     def calculate_bmr(self, gender, weight, height, age):
#         if gender.lower() == "male":
#             return 10 * weight + 6.25 * height - 5 * age + 5
#         return 10 * weight + 6.25 * height - 5 * age - 161

#     # ================= CALORIES =================
#     def calculate_daily_calories(self, bmr, activity, goal):
#         factors = {
#             "sedentary": 1.2,
#             "light": 1.375,
#             "moderate": 1.55,
#             "active": 1.725
#         }

#         calories = bmr * factors.get(activity, 1.2)

#         if goal == "loss":
#             calories -= 400
#             return max(int(calories), 1200)

#         elif goal == "gain":
#             calories += 300
#             return min(int(calories), 4000)

#         return int(calories)

#     # ================= FILTER =================
#     def _filter_foods(self, meal_type, lower, upper, goal, used_foods, diet_pref):
#         options = self.df[
#             (self.df["category"].str.lower().str.contains(meal_type.lower())) &
#             (self.df["calories"] >= lower) &
#             (self.df["calories"] <= upper)
#         ]

#         # 🔥 MAIN FEATURE (diet filter)
#         if diet_pref == "veg":
#             options = options[options["diet_type"] == "veg"]
#         else:
#             options = options[options["diet_type"].isin(["veg", "mixed"])]

#         options = options[~options["name"].isin(used_foods)]

#         if goal == "loss":
#             options = options[(options["fat"] <= 10)]
#             options = options.sort_values("calories")

#         elif goal == "gain":
#             options = options[(options["protein"] >= 10)]
#             options = options.sort_values("protein", ascending=False)

#         else:
#             options = options[(options["protein"] >= 5)]

#         return options

#     # ================= FALLBACK =================
#     def _fallback(self, meal_type, diet_pref):
#         options = self.df[
#             self.df["category"].str.lower().str.contains(meal_type.lower())
#         ]

#         if diet_pref == "veg":
#             options = options[options["diet_type"] == "veg"]

#         if len(options) == 0:
#             return self.df.sample(2).to_dict(orient="records")

#         return options.sample(min(2, len(options))).to_dict(orient="records")

#     # ================= GENERATE MEAL =================
#     def _generate_meal(self, meal_type, meal_cal, goal, used_foods, diet_pref):
#         lower = meal_cal * 0.5
#         upper = meal_cal * 1.1

#         options = self._filter_foods(meal_type, lower, upper, goal, used_foods, diet_pref)

#         if len(options) < 2:
#             return self._fallback(meal_type, diet_pref)

#         selected = options.sample(2).to_dict(orient="records")

#         for item in selected:
#             used_foods.add(item["name"])

#         return selected

#     # ================= DAILY PLAN =================
#     def daily_plan(self, user):
#         self._validate_user(user)

#         diet_pref = user.get("diet_pref", "mixed")

#         bmi = self.calculate_bmi(user["weight"], user["height"])
#         bmi_status = self.bmi_category(bmi)

#         bmr = self.calculate_bmr(
#             user["gender"], user["weight"], user["height"], user["age"]
#         )

#         daily_cal = self.calculate_daily_calories(
#             bmr, user["activity"], user["goal"]
#         )

#         meal_distribution = {
#             "Breakfast": 0.25,
#             "Lunch": 0.30,
#             "Snack": 0.15,
#             "Dinner": 0.30
#         }

#         plan = {}
#         used_foods = set()

#         for meal, ratio in meal_distribution.items():
#             plan[meal] = self._generate_meal(
#                 meal,
#                 daily_cal * ratio,
#                 user["goal"],
#                 used_foods,
#                 diet_pref
#             )

#         explanation = (
#             f"BMI: {bmi} ({bmi_status}) | "
#             f"Calories: {daily_cal} kcal | "
#             f"Goal: {user['goal'].upper()} | "
#             f"Diet: {diet_pref.upper()}"
#         )

#         return daily_cal, plan, explanation

#     # ================= WEEKLY PLAN =================
#     def weekly_plan(self, user):
#         week = {}
#         used_global = set()

#         for day in [
#             "Monday","Tuesday","Wednesday",
#             "Thursday","Friday","Saturday","Sunday"
#         ]:
#             _, plan, _ = self.daily_plan(user)

#             for meal in plan:
#                 unique = []
#                 for item in plan[meal]:
#                     if item["name"] not in used_global:
#                         unique.append(item)
#                         used_global.add(item["name"])

#                 if len(unique) < 2:
#                     unique.extend(self._fallback(meal, user.get("diet_pref", "mixed")))

#                 plan[meal] = unique[:2]

#             week[day] = plan

#         return week



import pandas as pd
import random


class DietRecommender:
    def __init__(self, path="dataset/Nutrition_Data.csv"):
        try:
            self.df = pd.read_csv(path)
        except Exception:
            raise FileNotFoundError(f"Dataset not found at {path}")

        # Clean column names
        self.df.columns = self.df.columns.str.strip()

        self.df.rename(columns={
            "Food_Name": "name",
            "Calories": "calories",
            "Protein": "protein",
            "Carbohydrates": "carbs",
            "Fats": "fat",
            "Fibre": "fiber",
            "Category": "category",
            "Free_Sugar": "sugar",
            "Sodium": "sodium"
        }, inplace=True)

        # Diet type fix
        if "diet_type" not in self.df.columns:
            self.df["diet_type"] = "mixed"

        self.df["diet_type"] = self.df["diet_type"].astype(str).str.lower().str.strip()

        # Category fix
        if "category" not in self.df.columns:
            categories = ["Breakfast", "Lunch", "Dinner", "Snack"]
            self.df["category"] = [random.choice(categories) for _ in range(len(self.df))]

        self.df["category"] = self.df["category"].astype(str).str.strip().str.capitalize()

        required = ["name", "calories", "protein", "carbs", "fat", "category", "diet_type"]
        self.df.dropna(subset=required, inplace=True)
        self.df.reset_index(drop=True, inplace=True)

    # ================= VALIDATION =================
    def _validate_user(self, user):
        if user["age"] < 5 or user["age"] > 100:
            raise ValueError("Invalid age")

        if user["weight"] < 20 or user["weight"] > 200:
            raise ValueError("Invalid weight")

        if user["height"] < 80 or user["height"] > 250:
            raise ValueError("Invalid height")

    # ================= BMI =================
    def calculate_bmi(self, weight, height):
        return round(weight / ((height / 100) ** 2), 2)

    def bmi_category(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 24.9:
            return "Normal"
        elif bmi < 29.9:
            return "Overweight"
        return "Obese"

    # ================= BMR =================
    def calculate_bmr(self, gender, weight, height, age):
        if gender.lower() == "male":
            return 10 * weight + 6.25 * height - 5 * age + 5
        return 10 * weight + 6.25 * height - 5 * age - 161

    # ================= CALORIES =================
    def calculate_daily_calories(self, bmr, activity, goal):
        factors = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725
        }

        calories = bmr * factors.get(activity, 1.2)

        if goal == "loss":
            calories -= 400
            return max(int(calories), 1200)

        elif goal == "gain":
            calories += 300
            return min(int(calories), 4000)

        return int(calories)

    # ================= FILTER =================
    def _filter_foods(self, meal_type, lower, upper, goal, used_foods, diet_pref, health):
        options = self.df[
            (self.df["category"].str.lower().str.contains(meal_type.lower())) &
            (self.df["calories"] >= lower) &
            (self.df["calories"] <= upper)
        ]

        # Diet filter
        if diet_pref == "veg":
            options = options[options["diet_type"] == "veg"]
        else:
            options = options[options["diet_type"].isin(["veg", "mixed"])]

        # 🔥 HEALTH FILTER
        if health == "diabetes":
            options = options[options["sugar"] <= 8]

        elif health == "bp":
            options = options[options["sodium"] <= 400]

        elif health == "heart":
            options = options[options["fat"] <= 12]

        # Remove used foods
        options = options[~options["name"].isin(used_foods)]

        # Goal logic
        if goal == "loss":
            options = options[(options["fat"] <= 10)]
            options = options.sort_values("calories")

        elif goal == "gain":
            options = options[(options["protein"] >= 10)]
            options = options.sort_values("protein", ascending=False)

        else:
            options = options[(options["protein"] >= 5)]

        return options

    # ================= FALLBACK =================
    def _fallback(self, meal_type, diet_pref):
        options = self.df[
            self.df["category"].str.lower().str.contains(meal_type.lower())
        ]

        if diet_pref == "veg":
            options = options[options["diet_type"] == "veg"]

        if len(options) == 0:
            return self.df.sample(2).to_dict(orient="records")

        return options.sample(min(2, len(options))).to_dict(orient="records")

    # ================= GENERATE MEAL =================
    def _generate_meal(self, meal_type, meal_cal, goal, used_foods, diet_pref, health):
        lower = meal_cal * 0.5
        upper = meal_cal * 1.1

        options = self._filter_foods(meal_type, lower, upper, goal, used_foods, diet_pref, health)

        if len(options) < 2:
            return self._fallback(meal_type, diet_pref)

        selected = options.sample(2).to_dict(orient="records")

        for item in selected:
            used_foods.add(item["name"])

        return selected

    # ================= DAILY PLAN =================
    def daily_plan(self, user):
        self._validate_user(user)

        diet_pref = user.get("diet_pref", "mixed")
        health = user.get("health_condition", "none")

        bmi = self.calculate_bmi(user["weight"], user["height"])
        bmi_status = self.bmi_category(bmi)

        bmr = self.calculate_bmr(
            user["gender"], user["weight"], user["height"], user["age"]
        )

        daily_cal = self.calculate_daily_calories(
            bmr, user["activity"], user["goal"]
        )

        meal_distribution = {
            "Breakfast": 0.25,
            "Lunch": 0.30,
            "Snack": 0.15,
            "Dinner": 0.30
        }

        plan = {}
        used_foods = set()

        for meal, ratio in meal_distribution.items():
            plan[meal] = self._generate_meal(
                meal,
                daily_cal * ratio,
                user["goal"],
                used_foods,
                diet_pref,
                health
            )

        explanation = (
            f"BMI: {bmi} ({bmi_status}) | "
            f"Calories: {daily_cal} kcal | "
            f"Goal: {user['goal'].upper()} | "
            f"Diet: {diet_pref.upper()} | "
            f"Health: {health.upper()}"
        )

        return daily_cal, plan, explanation

    # ================= WEEKLY PLAN =================
    def weekly_plan(self, user):
        week = {}
        used_global = set()

        for day in [
            "Monday","Tuesday","Wednesday",
            "Thursday","Friday","Saturday","Sunday"
        ]:
            _, plan, _ = self.daily_plan(user)

            for meal in plan:
                unique = []
                for item in plan[meal]:
                    if item["name"] not in used_global:
                        unique.append(item)
                        used_global.add(item["name"])

                if len(unique) < 2:
                    unique.extend(self._fallback(meal, user.get("diet_pref", "mixed")))

                plan[meal] = unique[:2]

            week[day] = plan

        return week





