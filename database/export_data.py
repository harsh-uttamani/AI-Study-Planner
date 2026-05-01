from pymongo import MongoClient
import pandas as pd

# ---------------- DATABASE CONNECTION ----------------

client = MongoClient("mongodb://localhost:27017/")

db = client["study_planner_db"]

plans = db["study_plans"]

# ---------------- FETCH DATA ----------------

data = list(plans.find())

# ---------------- REMOVE MongoDB ID ----------------

for record in data:

    record.pop("_id", None)

# ---------------- CREATE DATAFRAME ----------------

df = pd.DataFrame(data)

# ---------------- EXPORT CSV ----------------

df.to_csv("study_plans.csv", index=False)

print("✅ CSV Exported Successfully!")