from pymongo import MongoClient
from faker import Faker
import random

# ---------------- DATABASE ----------------

client = MongoClient("mongodb://localhost:27017/")

db = client["study_planner_db"]

plans = db["study_plans"]

# ---------------- DELETE OLD DATA ----------------

plans.delete_many({})

# ---------------- FAKER ----------------

fake = Faker()

# ---------------- DATA ----------------

subjects = [
    "Python",
    "Java",
    "Machine Learning",
    "Data Science",
    "MongoDB",
    "Big Data",
    "Tableau",
    "Cloud Computing",
    "AI",
    "Statistics"
]

topics = [
    "Aggregation",
    "Regression",
    "JDBC",
    "NumPy",
    "Pandas",
    "Visualization",
    "Clustering",
    "Functions",
    "OOP",
    "Statistics",
    "ETL",
    "Prediction",
    "Data Cleaning"
]

progress_options = [
    "Completed",
    "Pending"
]

# ---------------- COUNTRY & CITY ----------------

countries_and_cities = {

    "India": [
        "Mumbai",
        "Delhi",
        "Pune",
        "Bangalore",
        "Hyderabad"
    ],

    "USA": [
        "New York",
        "Chicago",
        "Houston",
        "Los Angeles"
    ],

    "Canada": [
        "Toronto",
        "Vancouver",
        "Montreal"
    ],

    "UK": [
        "London",
        "Manchester",
        "Liverpool"
    ],

    "Germany": [
        "Berlin",
        "Munich",
        "Hamburg"
    ]
}

# ---------------- GENERATE 1000 RECORDS ----------------

for i in range(1000):

    country = random.choice(
        list(countries_and_cities.keys())
    )

    city = random.choice(
        countries_and_cities[country]
    )

    plan = {

        "student_name": fake.name(),

        "country": country,

        "city": city,

        "subject": random.choice(subjects),

        "topic": random.choice(topics),

        "exam_date": fake.date(pattern="%d/%m/%Y"),

        "study_hours": random.randint(1, 8),

        "progress": random.choice(progress_options),

        "weak_topic": random.choice(topics)
    }

    plans.insert_one(plan)

# ---------------- SUCCESS MESSAGE ----------------

print("✅ 1000 Records Generated Successfully!")