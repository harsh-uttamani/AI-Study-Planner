import tkinter as tk
from tkinter import scrolledtext
from pymongo import MongoClient

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["study_planner_db"]
plans = db["study_plans"]

# Create Window
root = tk.Tk()

root.title("AI Study Planner")
root.geometry("500x600")

# Heading
heading = tk.Label(
    root,
    text="AI STUDY PLANNER",
    font=("Arial", 20, "bold")
)

heading.pack(pady=10)

# ---------------- LABELS + ENTRIES ----------------

tk.Label(root, text="Student Name").pack()
student_entry = tk.Entry(root, width=40)
student_entry.pack(pady=5)

tk.Label(root, text="Subject").pack()
subject_entry = tk.Entry(root, width=40)
subject_entry.pack(pady=5)

tk.Label(root, text="Topic").pack()
topic_entry = tk.Entry(root, width=40)
topic_entry.pack(pady=5)

tk.Label(root, text="Exam Date (DD/MM/YYYY)").pack()
exam_entry = tk.Entry(root, width=40)
exam_entry.pack(pady=5)

tk.Label(root, text="Daily Study Hours").pack()
hours_entry = tk.Entry(root, width=40)
hours_entry.pack(pady=5)

tk.Label(root, text="Progress").pack()
progress_entry = tk.Entry(root, width=40)
progress_entry.pack(pady=5)

tk.Label(root, text="Weak Topic").pack()
weak_entry = tk.Entry(root, width=40)
weak_entry.pack(pady=5)

tk.Label(root, text="Search Topic").pack()

search_entry = tk.Entry(root, width=40)
search_entry.pack(pady=5)

# ---------------- ADD FUNCTION ----------------

def add_plan_gui():

    student_name = student_entry.get()
    subject = subject_entry.get()
    topic = topic_entry.get()
    exam_date = exam_entry.get()
    study_hours = hours_entry.get()
    progress = progress_entry.get()
    weak_topic = weak_entry.get()

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

    status_label.config(text="✅ Study Plan Added Successfully!")

    # Clear fields after insert
    student_entry.delete(0, tk.END)
    subject_entry.delete(0, tk.END)
    topic_entry.delete(0, tk.END)
    exam_entry.delete(0, tk.END)
    hours_entry.delete(0, tk.END)
    progress_entry.delete(0, tk.END)
    weak_entry.delete(0, tk.END)
    
def view_plans_gui():
    
    print("Button clicked")

    output_area.delete(1.0, tk.END)

    all_plans = plans.find()

    for plan in all_plans:

        output_area.insert(
            tk.END,
            f"""
----------------------------------------
Student Name : {plan.get('student_name', '')}
Subject      : {plan.get('subject', '')}
Topic        : {plan.get('topic', '')}
Exam Date    : {plan.get('exam_date', '')}
Study Hours  : {plan.get('study_hours', '')}
Progress     : {plan.get('progress', '')}
Weak Topic   : {plan.get('weak_topic', '')}
----------------------------------------

"""
        )
        
def search_plan_gui():

    output_area.delete(1.0, tk.END)

    topic = search_entry.get()

    plan = plans.find_one({
        "topic": {
            "$regex": topic,
            "$options": "i"
        }
    })

    if plan:

        output_area.insert(
            tk.END,
            f"""
=========== STUDY PLAN FOUND ===========

Student Name : {plan.get('student_name', '')}
Subject      : {plan.get('subject', '')}
Topic        : {plan.get('topic', '')}
Exam Date    : {plan.get('exam_date', '')}
Study Hours  : {plan.get('study_hours', '')}
Progress     : {plan.get('progress', '')}
Weak Topic   : {plan.get('weak_topic', '')}

========================================
"""
        )

    else:
        output_area.insert(
            tk.END,
            "❌ Study plan not found!"
        )

def delete_plan_gui():

    topic = search_entry.get()

    result = plans.delete_one({
        "topic": {
            "$regex": f"^{topic}$",
            "$options": "i"
        }
    })

    output_area.delete(1.0, tk.END)

    if result.deleted_count > 0:

        output_area.insert(
            tk.END,
            "✅ Study plan deleted successfully!"
        )

    else:

        output_area.insert(
            tk.END,
            "❌ Study plan not found!"
        )

# ---------------- BUTTON ----------------

add_button = tk.Button(
    root,
    text="Add Study Plan",
    command=add_plan_gui,
    bg="green",
    fg="white",
    width=20
)

add_button.pack(pady=20)

view_button = tk.Button(
    root,
    text="View Study Plans",
    command=view_plans_gui,
    bg="blue",
    fg="white",
    width=20
)

view_button.pack(pady=10)

search_button = tk.Button(
    root,
    text="Search Study Plan",
    command=search_plan_gui,
    bg="orange",
    fg="white",
    width=20
)

search_button.pack(pady=10)

delete_button = tk.Button(
    root,
    text="Delete Study Plan",
    command=delete_plan_gui,
    bg="red",
    fg="white",
    width=20
)

delete_button.pack(pady=10)
# Status Label
status_label = tk.Label(root, text="")
status_label.pack()

output_area = scrolledtext.ScrolledText(
    root,
    width=55,
    height=15
)

output_area.pack(pady=10)

# Run Window
root.mainloop()