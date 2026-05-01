import customtkinter as ctk
from tkinter import messagebox
from pymongo import MongoClient

# ---------------- DATABASE ----------------

client = MongoClient("mongodb://localhost:27017/")

db = client["study_planner_db"]

users = db["users"]

# ---------------- APP SETTINGS ----------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------------- WINDOW ----------------

app = ctk.CTk()

app.title("AI Study Planner - Login")

app.geometry("700x700")

# ---------------- TITLE ----------------

title = ctk.CTkLabel(
    app,
    text="AI STUDY PLANNER",
    font=("Arial", 32, "bold")
)

title.pack(pady=20)

# ---------------- TABS ----------------

tabview = ctk.CTkTabview(app, width=500, height=550)

tabview.pack(pady=20)

tabview.add("Login")

tabview.add("Signup")

# =========================================================
# LOGIN TAB
# =========================================================

login_tab = tabview.tab("Login")

login_title = ctk.CTkLabel(
    login_tab,
    text="Login",
    font=("Arial", 24, "bold")
)

login_title.pack(pady=20)

# LOGIN EMAIL

login_email = ctk.CTkEntry(
    login_tab,
    placeholder_text="Email",
    width=300,
    height=40
)

login_email.pack(pady=10)

# LOGIN PASSWORD

login_password = ctk.CTkEntry(
    login_tab,
    placeholder_text="Password",
    show="*",
    width=300,
    height=40
)

login_password.pack(pady=10)

# =========================================================
# SIGNUP TAB
# =========================================================

signup_tab = tabview.tab("Signup")

signup_title = ctk.CTkLabel(
    signup_tab,
    text="Create Account",
    font=("Arial", 24, "bold")
)

signup_title.pack(pady=20)

# NAME

signup_name = ctk.CTkEntry(
    signup_tab,
    placeholder_text="Full Name",
    width=300,
    height=40
)

signup_name.pack(pady=10)

# EMAIL

signup_email = ctk.CTkEntry(
    signup_tab,
    placeholder_text="Email",
    width=300,
    height=40
)

signup_email.pack(pady=10)

# PASSWORD

signup_password = ctk.CTkEntry(
    signup_tab,
    placeholder_text="Password",
    show="*",
    width=300,
    height=40
)

signup_password.pack(pady=10)

# COUNTRY

signup_country = ctk.CTkEntry(
    signup_tab,
    placeholder_text="Country",
    width=300,
    height=40
)

signup_country.pack(pady=10)

# CITY

signup_city = ctk.CTkEntry(
    signup_tab,
    placeholder_text="City",
    width=300,
    height=40
)

signup_city.pack(pady=10)

# =========================================================
# FUNCTIONS
# =========================================================

# ---------------- SIGNUP FUNCTION ----------------

def signup():

    name = signup_name.get().strip()
    email = signup_email.get().strip()
    password = signup_password.get().strip()
    country = signup_country.get().strip()
    city = signup_city.get().strip()

    # VALIDATION

    if (
        name == "" or
        email == "" or
        password == "" or
        country == "" or
        city == ""
    ):

        messagebox.showerror(
            "Error",
            "Please fill all fields!"
        )

        return

    # CHECK EXISTING USER

    existing_user = users.find_one({
        "email": email
    })

    if existing_user:

        messagebox.showerror(
            "Error",
            "Email already exists!"
        )

        return

    # INSERT USER

    user = {

        "name": name,
        "email": email,
        "password": password,
        "country": country,
        "city": city
    }

    users.insert_one(user)

    messagebox.showinfo(
        "Success",
        "Account created successfully!"
    )

# ---------------- LOGIN FUNCTION ----------------

def login():

    email = login_email.get().strip()

    password = login_password.get().strip()

    user = users.find_one({

        "email": email,
        "password": password
    })
    if user:

        messagebox.showinfo(
            "Success",
            f"Welcome {user['name']}!"
        )

        # OPEN DASHBOARD

        

        import modern_gui

        modern_gui.current_user = user["name"]

        modern_gui.app.mainloop()

        app.destroy()
    else:

        messagebox.showerror(
            "Error",
            "Invalid email or password!"
        )
    


# =========================================================
# BUTTONS
# =========================================================

# LOGIN BUTTON

login_button = ctk.CTkButton(
    login_tab,
    text="Login",
    command=login,
    width=300,
    height=45,
    font=("Arial", 16, "bold")
)

login_button.pack(pady=20)

# SIGNUP BUTTON

signup_button = ctk.CTkButton(
    signup_tab,
    text="Create Account",
    command=signup,
    width=300,
    height=45,
    font=("Arial", 16, "bold")
)

signup_button.pack(pady=20)

# =========================================================
# RUN APP
# =========================================================

app.mainloop()