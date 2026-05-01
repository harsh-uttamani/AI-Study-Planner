import customtkinter as ctk
from tkinter import END
from pymongo import MongoClient

current_user = ""
# -------------------- DATABASE CONNECTION --------------------

client = MongoClient("mongodb://localhost:27017/")
db = client["study_planner_db"]
plans = db["study_plans"]

# -------------------- APP SETTINGS --------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# -------------------- MAIN WINDOW --------------------

app = ctk.CTk()

text="AI STUDY PLANNER DASHBOARD",
app.geometry("1500x900")
app.minsize(1200, 800)

# -------------------- TITLE --------------------

title = ctk.CTkLabel(
    app,
    text="AI STUDY PLANNER DASHBOARD",
    font=("Arial", 32, "bold")
)

title.pack(pady=20)

# -------------------- MAIN FRAME --------------------

main_frame = ctk.CTkFrame(
    app,
    fg_color="#1E1E2E"
)
main_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

# -------------------- LEFT FRAME --------------------

left_frame = ctk.CTkFrame(
    main_frame,
    width=350,
    corner_radius=20,
    fg_color="#25253A"
)
left_frame.pack(side="left", fill="y", padx=20, pady=20)

# -------------------- RIGHT FRAME --------------------

right_frame = ctk.CTkFrame(
    main_frame,
    corner_radius=20,
    fg_color="#25253A"
)
right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

# -------------------- FORM TITLE --------------------

form_title = ctk.CTkLabel(
    left_frame,
    text="Study Plan Form",
    font=("Arial", 24, "bold")
)

form_title.pack(pady=20)

# -------------------- ENTRIES --------------------


subject_entry = ctk.CTkEntry(
    left_frame,
    placeholder_text="Subject",
    width=300,
    height=40
)
subject_entry.pack(pady=6)

topic_entry = ctk.CTkEntry(
    left_frame,
    placeholder_text="Topic",
    width=300,
    height=40
)
topic_entry.pack(pady=6)

exam_entry = ctk.CTkEntry(
    left_frame,
    placeholder_text="Exam Date (DD/MM/YYYY)",
    width=300,
    height=40
)
exam_entry.pack(pady=6)

hours_entry = ctk.CTkEntry(
    left_frame,
    placeholder_text="Daily Study Hours",
    width=300,
    height=40
)
hours_entry.pack(pady=6)

progress_entry = ctk.CTkEntry(
    left_frame,
    placeholder_text="Progress",
    width=300,
    height=40
)
progress_entry.pack(pady=6)

weak_entry = ctk.CTkEntry(
    left_frame,
    placeholder_text="Weak Topic",
    width=300,
    height=40
)
weak_entry.pack(pady=6)

search_entry = ctk.CTkEntry(
    left_frame,
    placeholder_text="Search Topic",
    width=300,
    height=40
)
search_entry.pack(pady=10)

# -------------------- OUTPUT BOX --------------------

output_box = ctk.CTkTextbox(
    right_frame,
    width=850,
    height=550,
    font=("Consolas", 16),
    corner_radius=15,
    border_width=2,
    border_color="#3B8ED0",
    fg_color="#101820",
    text_color="white",
    scrollbar_button_color="#3B8ED0",
    scrollbar_button_hover_color="#5DADE2"
)

output_box.pack(
    padx=20,
    pady=20,
    fill="both",
    expand=True
)

# -------------------- FUNCTIONS --------------------

def show_analytics():

    output_box.delete("1.0", END)

    # ---------------- TOTAL COUNTS ----------------

    total_plans = plans.count_documents({})

    completed = plans.count_documents({
        "progress": "Completed"
    })

    pending = plans.count_documents({
        "progress": "Pending"
    })

    # ---------------- COMPLETION PERCENTAGE ----------------

    completion_rate = round(
        (completed / total_plans) * 100,
        2
    )

    pending_rate = round(
        (pending / total_plans) * 100,
        2
    )

    # ---------------- AVERAGE STUDY HOURS ----------------

    avg_pipeline = [

        {
            "$group": {

                "_id": None,

                "avg_hours": {
                    "$avg": "$study_hours"
                }
            }
        }
    ]

    avg_result = list(
        plans.aggregate(avg_pipeline)
    )

    avg_hours = round(
        avg_result[0]["avg_hours"],
        2
    )

    # ---------------- MOST COMMON WEAK TOPIC ----------------

    weak_pipeline = [

        {
            "$group": {

                "_id": "$weak_topic",

                "count": {
                    "$sum": 1
                }
            }
        },

        {
            "$sort": {
                "count": -1
            }
        },

        {
            "$limit": 1
        }
    ]

    weak_result = list(
        plans.aggregate(weak_pipeline)
    )

    weak_topic = weak_result[0]["_id"]

    weak_count = weak_result[0]["count"]

    # ---------------- TOP SUBJECT ----------------

    subject_pipeline = [

        {
            "$group": {

                "_id": "$subject",

                "count": {
                    "$sum": 1
                }
            }
        },

        {
            "$sort": {
                "count": -1
            }
        },

        {
            "$limit": 1
        }
    ]

    subject_result = list(
        plans.aggregate(subject_pipeline)
    )

    top_subject = subject_result[0]["_id"]

    top_subject_count = subject_result[0]["count"]

    # ---------------- AI INSIGHTS ----------------

    insights = []

    if completion_rate > 70:

        insights.append(
            "Excellent overall student performance detected."
        )

    else:

        insights.append(
            "Many students still have pending study plans."
        )

    if avg_hours < 4:

        insights.append(
            "Average study time is low. Students need more study hours."
        )

    else:

        insights.append(
            "Average study hours are satisfactory."
        )

    insights.append(
        f"Most difficult topic identified: {weak_topic}"
    )

    # ---------------- OUTPUT ----------------

    output_box.insert(
        END,

f"""

╔══════════════════════════════════════════════╗
        AI STUDY PLANNER ANALYTICS REPORT
╚══════════════════════════════════════════════╝

📊 TOTAL RECORDS ANALYSIS
------------------------------------------------

📚 Total Study Plans      : {total_plans}

✅ Completed Plans        : {completed}

⌛ Pending Plans          : {pending}

📈 Completion Rate        : {completion_rate}%

📉 Pending Rate           : {pending_rate}%


⏰ STUDY HOURS ANALYSIS
------------------------------------------------

🕒 Average Study Hours    : {avg_hours} hrs/day


📚 SUBJECT ANALYSIS
------------------------------------------------

🏆 Most Popular Subject   : {top_subject}

📌 Total Students         : {top_subject_count}


⚠️ WEAK TOPIC ANALYSIS
------------------------------------------------

🚨 Most Weak Topic        : {weak_topic}

👥 Students Affected      : {weak_count}


🤖 AI GENERATED INSIGHTS
------------------------------------------------

• {insights[0]}

• {insights[1]}

• {insights[2]}


═══════════════════════════════════════════════
MongoDB Aggregation Pipeline Analytics Completed
═══════════════════════════════════════════════

"""
    )
def clear_fields():

    
    subject_entry.delete(0, END)
    topic_entry.delete(0, END)
    exam_entry.delete(0, END)
    hours_entry.delete(0, END)
    progress_entry.delete(0, END)
    weak_entry.delete(0, END)

# -------------------- ADD PLAN --------------------

def add_plan():

    
    subject = subject_entry.get().strip()
    topic = topic_entry.get().strip()
    exam_date = exam_entry.get().strip()
    study_hours = hours_entry.get().strip()
    progress = progress_entry.get().strip()
    weak_topic = weak_entry.get().strip()

    # ---------------- VALIDATION ----------------

    if (
        

        
        subject == "" or
        topic == "" or
        exam_date == "" or
        study_hours == "" or
        progress == ""
    ):

        output_box.delete("1.0", END)

        output_box.insert(
            END,
            "❌ Please fill all required fields!"
        )

        return

    # ---------------- NUMBER VALIDATION ----------------

    try:
        study_hours = float(study_hours)

    except:

        output_box.delete("1.0", END)

        output_box.insert(
            END,
            "❌ Study hours must be a number!"
        )

        return

    # ---------------- DATABASE INSERT ----------------

    plan = {

        "student_name": current_user,
        "subject": subject,
        "topic": topic,
        "exam_date": exam_date,
        "study_hours": study_hours,
        "progress": progress,
        "weak_topic": weak_topic
    }

    plans.insert_one(plan)

    output_box.delete("1.0", END)

    output_box.insert(
        END,
        "✅ Study Plan Added Successfully!"
    )

    clear_fields()

# -------------------- VIEW PLANS --------------------

def view_plans():

    output_box.delete("1.0", END)

    all_plans = plans.find()

    for plan in all_plans:

        output_box.insert(
            END,
            f"""

==================================================

Student Name : {plan.get('student_name', '')}
Subject      : {plan.get('subject', '')}
Topic        : {plan.get('topic', '')}
Exam Date    : {plan.get('exam_date', '')}
Study Hours  : {plan.get('study_hours', '')}
Progress     : {plan.get('progress', '')}
Weak Topic   : {plan.get('weak_topic', '')}

==================================================

"""
        )

# -------------------- SEARCH PLAN --------------------

def search_plan():

    output_box.delete("1.0", END)

    topic = search_entry.get()

    plan = plans.find_one({

        "topic": {
            "$regex": topic,
            "$options": "i"
        }
    })

    if plan:

        output_box.insert(
            END,
            f"""

============= STUDY PLAN FOUND =============

Student Name : {plan.get('student_name', '')}
Subject      : {plan.get('subject', '')}
Topic        : {plan.get('topic', '')}
Exam Date    : {plan.get('exam_date', '')}
Study Hours  : {plan.get('study_hours', '')}
Progress     : {plan.get('progress', '')}
Weak Topic   : {plan.get('weak_topic', '')}

============================================

"""
        )

    else:

        output_box.insert(
            END,
            "❌ Study Plan Not Found!"
        )

# -------------------- DELETE PLAN --------------------

def delete_plan():

    topic = search_entry.get()

    result = plans.delete_one({

        "topic": {
            "$regex": f"^{topic}$",
            "$options": "i"
        }
    })

    output_box.delete("1.0", END)

    if result.deleted_count > 0:

        output_box.insert(
            END,
            "✅ Study Plan Deleted Successfully!"
        )

    else:

        output_box.insert(
            END,
            "❌ Study Plan Not Found!"
        )
        
    

# -------------------- BUTTONS --------------------

add_button = ctk.CTkButton(
    left_frame,
    text="Add Study Plan",
    command=add_plan,
    width=300,
    height=45,
    fg_color="#2563EB",
    hover_color="#1D4ED8",
    corner_radius=12,
    font=("Arial", 16, "bold")
)

add_button.pack(pady=4)

view_button = ctk.CTkButton(
    left_frame,
    text="View Study Plans",
    command=view_plans,
    fg_color="#0EA5E9",
    hover_color="#0284C7",
    corner_radius=12,
    width=300,
    height=45,
    font=("Arial", 16, "bold")
)

view_button.pack(pady=4)

search_button = ctk.CTkButton(
    left_frame,
    text="Search Study Plan",
    command=search_plan,
    width=300,
    fg_color="#F59E0B",
    hover_color="#D97706",
    corner_radius=12,
    height=45,
    font=("Arial", 16, "bold")
)

search_button.pack(pady=4) 

delete_button = ctk.CTkButton(
    left_frame,
    text="Delete Study Plan",
    command=delete_plan,
    width=300,
    corner_radius=12,
    height=45,
    fg_color="red",
    hover_color="darkred",
    font=("Arial", 16, "bold")
)

delete_button.pack(pady=4)

analytics_button = ctk.CTkButton(

    left_frame,

    text="Progress Analytics",

    command=show_analytics,

    width=300,

    height=40,

    fg_color="purple",

    hover_color="darkviolet",

    font=("Arial", 16, "bold")
)

analytics_button.pack(pady=8)



schedule_button = ctk.CTkButton(
    left_frame,
    text="Generate Schedule",
    width=300,
    height=45,
    fg_color="#16A085",
    hover_color="#1ABC9C",
    font=("Arial", 16, "bold")
)

schedule_button.pack(pady=4)

recommend_button = ctk.CTkButton(
    left_frame,
    text="Weak Topic Suggestions",
    width=300,
    height=45,
    fg_color="#D35400",
    hover_color="#E67E22",
    font=("Arial", 16, "bold")
)

recommend_button.pack(pady=4)

# -------------------- RUN APP --------------------



