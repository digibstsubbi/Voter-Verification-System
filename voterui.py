import psycopg2
from datetime import datetime, date
import tkinter as tk
from tkinter import messagebox, simpledialog

# ================= DATABASE CONNECTION =================

con = psycopg2.connect(
    host="localhost",
    database="voter_verfication",
    user="postgres",
    password="Saurabh@123"
)

cur = con.cursor()

# ================= LOGIN CREDENTIALS =================

VALID_USER = "subbi"
VALID_PASS = "subbi@123"
VALID_MOBILE = "8954246887"

# ================= CORE LOGIC =================

def calculate_age(dob):
    today = date.today()
    age = today.year - dob.year
    if (today.month, today.day) < (dob.month, dob.day):
        age -= 1
    return age


# ================= APP FUNCTIONS =================

def add_voter_ui():
    name = simpledialog.askstring("Input", "Enter Name")
    father = simpledialog.askstring("Input", "Enter Father Name")
    aadhaar = simpledialog.askstring("Input", "Enter Aadhaar Number")
    dob_input = simpledialog.askstring("Input", "Enter DOB (YYYY-MM-DD)")

    if not name or not father or not aadhaar or not dob_input:
        messagebox.showerror("Error", "All fields required")
        return

    try:
        dob = datetime.strptime(dob_input, "%Y-%m-%d").date()
    except:
        messagebox.showerror("Error", "Invalid DOB format")
        return

    age = calculate_age(dob)

    if age < 18:
        messagebox.showwarning("Not Eligible", "Age less than 18")
        return

    try:
        cur.execute("SELECT * FROM voters WHERE aadhaar_no=%s", (aadhaar,))
        if cur.fetchone():
            messagebox.showerror("Error", "Aadhaar already exists")
            return

        cur.execute("""
        INSERT INTO voters(name,father_name,aadhaar_no,dob)
        VALUES(%s,%s,%s,%s)
        RETURNING voter_no
        """, (name, father, aadhaar, dob))

        voter_no = cur.fetchone()[0]
        con.commit()

        messagebox.showinfo("Success", f"Voter Added!\nVoter No: {voter_no}")

    except Exception as e:
        con.rollback()
        messagebox.showerror("DB Error", str(e))


def search_voter_ui():
    aadhaar = simpledialog.askstring("Search", "Enter Aadhaar Number")

    cur.execute("SELECT * FROM voters WHERE aadhaar_no=%s", (aadhaar,))
    data = cur.fetchone()

    if data:
        messagebox.showinfo("Voter Found",
            f"Voter No: {data[0]}\nName: {data[1]}\nFather: {data[2]}\nDOB: {data[4]}"
        )
    else:
        messagebox.showerror("Not Found", "Voter not found")


def show_voters_ui():
    cur.execute("SELECT * FROM voters ORDER BY voter_no")
    data = cur.fetchall()

    text = ""
    for i in data:
        text += f"{i[0]} | {i[1]} | {i[2]} | {i[3]} | {i[4]}\n"

    messagebox.showinfo("All Voters", text if text else "No Data")


def delete_voter_ui():
    aadhaar = simpledialog.askstring("Delete", "Enter Aadhaar Number")

    cur.execute("DELETE FROM voters WHERE aadhaar_no=%s", (aadhaar,))
    con.commit()

    messagebox.showinfo("Success", "Deleted Successfully")


def verify_voter_ui():
    aadhaar = simpledialog.askstring("Verify", "Enter Aadhaar Number")

    cur.execute("SELECT * FROM voters WHERE aadhaar_no=%s", (aadhaar,))
    data = cur.fetchone()

    if not data:
        messagebox.showerror("Error", "Not Found")
        return

    age = calculate_age(data[4])
    status = "ELIGIBLE" if age >= 18 else "NOT ELIGIBLE"

    messagebox.showinfo("Verification",
        f"Name: {data[1]}\nAge: {age}\nStatus: {status}"
    )


# ================= MAIN DASHBOARD =================

def open_main_app():
    login_window.destroy()

    root = tk.Tk()
    root.title("Voting System Dashboard")
    root.geometry("500x500")
    root.configure(bg="#1e1e2f")

    tk.Label(root, text="VOTING SYSTEM", font=("Arial", 18, "bold"),
             fg="white", bg="#1e1e2f").pack(pady=20)

    btn = {"width": 25, "height": 2}

    tk.Button(root, text="Add Voter", command=add_voter_ui, **btn).pack(pady=5)
    tk.Button(root, text="Search Voter", command=search_voter_ui, **btn).pack(pady=5)
    tk.Button(root, text="Show All", command=show_voters_ui, **btn).pack(pady=5)
    tk.Button(root, text="Delete Voter", command=delete_voter_ui, **btn).pack(pady=5)
    tk.Button(root, text="Verify Voter", command=verify_voter_ui, **btn).pack(pady=5)
    tk.Button(root, text="Exit", command=root.destroy, bg="red", fg="white", **btn).pack(pady=20)

    root.mainloop()


# ================= LOGIN WINDOW =================

def check_login():
    u = entry_user.get()
    p = entry_pass.get()
    m = entry_mobile.get()

    if u == VALID_USER and p == VALID_PASS and m == VALID_MOBILE:
        messagebox.showinfo("Success", "Login Successful")
        open_main_app()
    else:
        messagebox.showerror("Error", "Invalid Login")


login_window = tk.Tk()
login_window.title("Login Page")
login_window.geometry("350x300")
login_window.configure(bg="#2c2c3e")

tk.Label(login_window, text="LOGIN", font=("Arial", 16, "bold"),
         fg="white", bg="#2c2c3e").pack(pady=15)

tk.Label(login_window, text="Username", fg="white", bg="#2c2c3e").pack()
entry_user = tk.Entry(login_window)
entry_user.pack()

tk.Label(login_window, text="Password", fg="white", bg="#2c2c3e").pack()
entry_pass = tk.Entry(login_window, show="*")
entry_pass.pack()

tk.Label(login_window, text="Mobile", fg="white", bg="#2c2c3e").pack()
entry_mobile = tk.Entry(login_window)
entry_mobile.pack()

tk.Button(login_window, text="Login", command=check_login,
          bg="green", fg="white", width=15).pack(pady=20)

login_window.mainloop()