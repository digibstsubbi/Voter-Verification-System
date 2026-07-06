import psycopg2
from datetime import datetime, date

# ================= DATABASE CONNECTION =================

con = psycopg2.connect(
    host="localhost",
    database="voter_verfication",
    user="postgres",
    password="Saurabh@123"
)

cur = con.cursor()

print("=" * 60)
print("        VOTING VERIFICATION SYSTEM")
print("=" * 60)

# ================= ADMIN LOGIN =================

def login():

    while True:

        username = input("Enter Username : ")
        password = input("Enter Password : ")

        cur.execute(
            "SELECT * FROM admin WHERE username=%s AND password=%s",
            (username, password)
        )

        data = cur.fetchone()

        if data:
            print("\nLogin Successful...")
            break

        else:
            print("\nInvalid Username or Password")
            print("Try Again...\n")


# ================= MAIN MENU =================

def menu():

    print("\n")
    print("=" * 60)
    print("                MAIN MENU")
    print("=" * 60)
    print("1. Add New Voter")
    print("2. Search Voter")
    print("3. Show All Voters")
    print("4. Delete Voter")
    print("5. Verify Voter")
    print("6. Exit")
    print("=" * 60)


# ================= FUNCTION DECLARATIONS =================

def add_voter():
    pass


def search_voter():
    pass


def show_voters():
    pass


def delete_voter():
    pass


def verify_voter():
    pass
# ================= ADD NEW VOTER =================

def calculate_age(dob):

    today = date.today()

    age = today.year - dob.year

    if (today.month, today.day) < (dob.month, dob.day):
        age -= 1

    return age


def add_voter():

    print("\n========== ADD NEW VOTER ==========\n")

    name = input("Enter Name : ")
    father = input("Enter Father Name : ")
    aadhaar = input("Enter Aadhaar Number : ")
    dob_input = input("Enter DOB (YYYY-MM-DD) : ")

    try:

        dob = datetime.strptime(dob_input, "%Y-%m-%d").date()

    except:

        print("\nInvalid Date Format!")
        return

    age = calculate_age(dob)

    print("\nAge :", age)

    if age < 18:

        print("\nNot Eligible For Voting")
        return

    try:

        cur.execute("SELECT * FROM voters WHERE aadhaar_no=%s",(aadhaar,))

        if cur.fetchone():

            print("\nAadhaar Number Already Exists")
            return


        cur.execute("""

        INSERT INTO voters
        (name,father_name,aadhaar_no,dob)
        VALUES(%s,%s,%s,%s)
        RETURNING voter_no

        """,(name,father,aadhaar,dob))

        voter_no = cur.fetchone()[0]

        con.commit()

        print("\n===================================")
        print("Eligible For Voting")
        print("Voter Number :", voter_no)
        print("Data Saved Successfully")
        print("===================================")

    except Exception as e:

        con.rollback()

        print("Error :",e)
# ================= SEARCH VOTER =================

def search_voter():

    print("\n========== SEARCH VOTER ==========\n")

    aadhaar = input("Enter Aadhaar Number : ")

    cur.execute(
        "SELECT * FROM voters WHERE aadhaar_no=%s",
        (aadhaar,)
    )

    data = cur.fetchone()

    if data:

        print("\n========== VOTER DETAILS ==========")
        print("Voter No      :", data[0])
        print("Name          :", data[1])
        print("Father Name   :", data[2])
        print("Aadhaar No    :", data[3])
        print("Date of Birth :", data[4])

    else:

        print("\nVoter Not Found")


# ================= SHOW ALL VOTERS =================

def show_voters():

    print("\n========== ALL VOTERS ==========\n")

    cur.execute("SELECT * FROM voters ORDER BY voter_no")

    data = cur.fetchall()

    if len(data) == 0:

        print("No Record Found")
        return

    print("-"*75)
    print("VoterNo\tName\tFather Name\tAadhaar\t\tDOB")
    print("-"*75)

    for i in data:

        print(i[0],"\t",i[1],"\t",i[2],"\t",i[3],"\t",i[4])



# ================= DELETE VOTER =================

def delete_voter():

    print("\n========== DELETE VOTER ==========\n")

    aadhaar = input("Enter Aadhaar Number : ")

    cur.execute(
        "SELECT * FROM voters WHERE aadhaar_no=%s",
        (aadhaar,)
    )

    if cur.fetchone() is None:

        print("\nVoter Not Found")
        return

    cur.execute(
        "DELETE FROM voters WHERE aadhaar_no=%s",
        (aadhaar,)
    )

    con.commit()

    print("\nVoter Deleted Successfully")


# ================= VERIFY VOTER =================

def verify_voter():

    print("\n========== VERIFY VOTER ==========\n")

    aadhaar = input("Enter Aadhaar Number : ")

    cur.execute(
        "SELECT * FROM voters WHERE aadhaar_no=%s",
        (aadhaar,)
    )

    data = cur.fetchone()

    if data:

        dob = data[4]

        age = calculate_age(dob)

        print("\n========== VERIFICATION ==========")
        print("Voter No      :", data[0])
        print("Name          :", data[1])
        print("Father Name   :", data[2])
        print("Aadhaar No    :", data[3])
        print("Date of Birth :", data[4])
        print("Age           :", age)

        if age >= 18:
            print("\nStatus : VERIFIED (Eligible)")
        else:
            print("\nStatus : NOT ELIGIBLE")

    else:

        print("\nVoter Not Found")
# ================= MAIN PROGRAM =================

login()

while True:

    menu()

    try:
        choice = int(input("Enter Your Choice : "))

    except ValueError:
        print("\nInvalid Input")
        continue

    if choice == 1:

        add_voter()

    elif choice == 2:

        search_voter()

    elif choice == 3:

        show_voters()

    elif choice == 4:

        delete_voter()

    elif choice == 5:

        verify_voter()

    elif choice == 6:

        print("\nThank You For Using Voting Verification System")
        break

    else:

        print("\nInvalid Choice")

con.close()