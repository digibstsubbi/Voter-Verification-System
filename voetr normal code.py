from datetime import datetime, date

print("=" * 60)
print("        VOTING VERIFICATION SYSTEM")
print("=" * 60)

# ================= ADMIN LOGIN =================

USERNAME = "admin"
PASSWORD = "1234"

voters = []
voter_no = 1001

# ================= LOGIN =================

def login():

    while True:

        username = input("Enter Username : ")
        password = input("Enter Password : ")

        if username == USERNAME and password == PASSWORD:
            print("\nLogin Successful...")
            break
        else:
            print("\nInvalid Username or Password\n")


# ================= MENU =================

def menu():

    print("\n" + "=" * 60)
    print("                MAIN MENU")
    print("=" * 60)
    print("1. Add New Voter")
    print("2. Search Voter")
    print("3. Show All Voters")
    print("4. Delete Voter")
    print("5. Verify Voter")
    print("6. Exit")
    print("=" * 60)


# ================= AGE =================

def calculate_age(dob):

    today = date.today()

    age = today.year - dob.year

    if (today.month, today.day) < (dob.month, dob.day):
        age -= 1

    return age


# ================= ADD =================

def add_voter():

    global voter_no

    print("\n========== ADD NEW VOTER ==========\n")

    name = input("Enter Name : ")
    father = input("Enter Father Name : ")
    aadhaar = input("Enter Aadhaar Number : ")
    dob_input = input("Enter DOB (YYYY-MM-DD) : ")

    try:
        dob = datetime.strptime(dob_input, "%Y-%m-%d").date()
    except:
        print("Invalid Date Format")
        return

    age = calculate_age(dob)

    if age < 18:
        print("Not Eligible For Voting")
        return

    for i in voters:
        if i["aadhaar"] == aadhaar:
            print("Aadhaar Already Exists")
            return

    voter = {
        "voter_no": voter_no,
        "name": name,
        "father": father,
        "aadhaar": aadhaar,
        "dob": dob
    }

    voters.append(voter)

    print("\nEligible For Voting")
    print("Voter Number :", voter_no)
    print("Data Saved Successfully")

    voter_no += 1


# ================= SEARCH =================

def search_voter():

    aadhaar = input("Enter Aadhaar Number : ")

    for i in voters:

        if i["aadhaar"] == aadhaar:

            print("\nVoter No :", i["voter_no"])
            print("Name :", i["name"])
            print("Father :", i["father"])
            print("Aadhaar :", i["aadhaar"])
            print("DOB :", i["dob"])
            return

    print("Voter Not Found")


# ================= SHOW =================

def show_voters():

    if len(voters) == 0:
        print("\nNo Record Found")
        return

    print("-" * 80)
    print("VoterNo\tName\tFather\tAadhaar\t\tDOB")
    print("-" * 80)

    for i in voters:

        print(
            i["voter_no"],
            "\t",
            i["name"],
            "\t",
            i["father"],
            "\t",
            i["aadhaar"],
            "\t",
            i["dob"]
        )


# ================= DELETE =================

def delete_voter():

    aadhaar = input("Enter Aadhaar Number : ")

    for i in voters:

        if i["aadhaar"] == aadhaar:
            voters.remove(i)
            print("Voter Deleted Successfully")
            return

    print("Voter Not Found")


# ================= VERIFY =================

def verify_voter():

    aadhaar = input("Enter Aadhaar Number : ")

    for i in voters:

        if i["aadhaar"] == aadhaar:

            age = calculate_age(i["dob"])

            print("\nVoter No :", i["voter_no"])
            print("Name :", i["name"])
            print("Father :", i["father"])
            print("Aadhaar :", i["aadhaar"])
            print("DOB :", i["dob"])
            print("Age :", age)

            if age >= 18:
                print("Status : VERIFIED")
            else:
                print("Status : NOT ELIGIBLE")

            return

    print("Voter Not Found")


# ================= MAIN =================

login()

while True:

    menu()

    try:
        choice = int(input("Enter Your Choice : "))
    except:
        print("Invalid Input")
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
        print("Thank You")
        break

    else:
        print("Invalid Choice")