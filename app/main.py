from datetime import datetime
from pymongo import MongoClient


# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Create database
db = client["study_planner_db"]

# Create collection
plans = db["study_plans"]

def add_plan():
    student_name = input("Enter student name: ")
    subject = input("Enter subject: ")
    topic = input("Enter topic: ")
    exam_date = input("Enter exam date (DD/MM/YYYY): ")
    study_hours = float(input("Enter daily study hours: "))
    progress = input("Enter progress status (Pending/Completed): ")
    weak_topic = input("Enter weak topic: ")

    plan = {
        "student_name": student_name,
        "subject": subject,
        "topic": topic,
        "exam_date": exam_date,
        "study_hours": study_hours,
        "progress": progress,
        "weak_topic": weak_topic
    }

    plans.insert_one(plan)

    print("✅ Study plan added successfully!")
    
def view_plans():
    all_plans = plans.find()

    print("\n===== STUDY PLANS =====")

    for plan in all_plans:
        print("-" * 35)
        print(f"Student Name : {plan.get('student_name', '')}")
        print(f"Subject      : {plan.get('subject', '')}")
        print(f"Topic        : {plan.get('topic', '')}")
        print(f"Exam Date    : {plan.get('exam_date', '')}")
        print(f"Study Hours  : {plan.get('study_hours', '')}")
        print(f"Progress     : {plan.get('progress', '')}")
        print(f"Weak Topic   : {plan.get('weak_topic', '')}")

def update_plan():
    topic = input("Enter topic to update: ")

    new_progress = input("Enter new progress status: ")
    new_hours = float(input("Enter new study hours: "))

    result = plans.update_one(
        {"topic": topic},
        {
            "$set": {
                "progress": new_progress,
                "study_hours": new_hours
            }
        }
    )

    if result.modified_count > 0:
        print("✅ Study plan updated successfully!")
    else:
        print("❌ Topic not found!")

def delete_plan():
    topic = input("Enter topic to delete: ")

    result = plans.delete_one({"topic": topic})

    if result.deleted_count > 0:
        print("✅ Study plan deleted successfully!")
    else:
        print("❌ Topic not found!")
        
def search_plan():
    topic = input("Enter topic to search: ")

    plan = plans.find_one({
        "topic": {
            "$regex": topic,
            "$options": "i"
        }
    })

    if plan:
        print("\n✅ Study Plan Found!")
        print(f"Student Name : {plan.get('student_name', '')}")
        print(f"Subject      : {plan.get('subject', '')}")
        print(f"Topic        : {plan.get('topic', '')}")
        print(f"Exam Date    : {plan.get('exam_date', '')}")
        print(f"Study Hours  : {plan.get('study_hours', '')}")
        print(f"Progress     : {plan.get('progress', '')}")
        print(f"Weak Topic   : {plan.get('weak_topic', '')}")
    else:
        print("❌ Study plan not found!")
        
def progress_analytics():

    total_plans = plans.count_documents({})

    completed_plans = plans.count_documents({
        "progress": {
            "$regex": "^completed$",
            "$options": "i"
        }
    })

    pending_plans = total_plans - completed_plans

    print("\n====== PROGRESS ANALYTICS ======")

    print(f"Total Study Plans : {total_plans}")
    print(f"Completed Plans   : {completed_plans}")
    print(f"Pending Plans     : {pending_plans}")

    if total_plans > 0:

        progress_percentage = (completed_plans / total_plans) * 100

        print(f"Overall Progress  : {progress_percentage:.2f}%")

        if progress_percentage >= 80:
            print("🔥 Excellent progress!")

        elif progress_percentage >= 50:
            print("👍 Good progress!")

        else:
            print("⚠️ Need more consistency!")

    else:
        print("❌ No study plans found!")
        

            
def generate_study_schedule():

    exam_date_input = input("Enter exam date (DD/MM/YYYY): ")
    total_topics = int(input("Enter total number of topics: "))
    daily_hours = float(input("Enter daily study hours: "))

    today = datetime.today()

    exam_date = datetime.strptime(exam_date_input, "%d/%m/%Y")

    days_left = (exam_date - today).days

    if days_left <= 0:
        print("❌ Exam date already passed!")
        return

    topics_per_day = total_topics / days_left

    print("\n====== STUDY SCHEDULE ======")
    print(f"Days Left        : {days_left}")
    print(f"Topics Per Day   : {topics_per_day:.2f}")
    print(f"Daily Study Time : {daily_hours} hours")

    if daily_hours < 2:
        print("⚠️ Recommendation: Increase study hours.")

    elif daily_hours >= 5:
        print("🔥 Excellent study consistency!")

    else:
        print("👍 Good study routine!")
        
def recommend_weak_topics():

    weak_plans = plans.find({
        "weak_topic": {
            "$ne": ""
        }
    })

    print("\n====== WEAK TOPIC RECOMMENDATIONS ======")

    found = False

    for plan in weak_plans:

        found = True

        print("-" * 40)
        print(f"Student Name : {plan.get('student_name', '')}")
        print(f"Subject      : {plan.get('subject', '')}")
        print(f"Weak Topic   : {plan.get('weak_topic', '')}")

        print("📌 Recommendation:")
        print(f"Revise '{plan.get('weak_topic', '')}' daily for 1 hour.")

    if not found:
        print("✅ No weak topics found!")
        
def menu():
    while True:
        print("\n====== AI STUDY PLANNER ======")
        print("1. Add Study Plan")
        print("2. View Study Plans")
        print("3. Update Study Plan")
        print("4. Delete Study Plan")
        print("5. Search Study Plan")
        print("6. Generate Study Schedule")
        print("7. Weak Topic Recommendations")
        print("8. Progress Analytics")
        print("9. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            add_plan()

        elif choice == "2":
            view_plans()

        elif choice == "3":
            update_plan()

        elif choice == "4":
            delete_plan()

        elif choice == "5":
            search_plan()

        elif choice == "6":
            generate_study_schedule()

        elif choice == "7":
            recommend_weak_topics()

        elif choice == "8":
            progress_analytics()

        elif choice == "9":
            print("Exiting system...")
            break

    else:
            print("❌ Invalid choice!")
        
    

if __name__ == "__main__":
    menu()
print("Connected to MongoDB successfully!")