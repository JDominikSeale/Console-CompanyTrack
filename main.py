import database

class Main:
    def __init__(self):
        self.db = database.db()
        self.user_id = None
        self.startMenu()

    def clearScreen(self):
        print("\n" * 100)

    def pause(self):
        input("Enter key to continue")

    def displayMultiResult(self, result):
        if result == ():
            print("EMPTY")
        else:
            print("Job ID | Description | Address | Created Date | Predicted End Date | Price")
            for row in result:
                print(row, end="\n")

    def startMenu(self):
        self.clearScreen()
        print("START MENU")
        print("1. Register")
        print("2. Login")
        choice = input("Enter choice: ")
        if choice == "1":
            self.register()
        elif choice == "2":
            self.login()
        else:
            print("Invalid choice")
            self.startMenu()
    
    def login(self):
        self.clearScreen()
        print("LOGIN MENU")
        email = input("Enter Email: ")
        name = input("Enter Name: ")
        result = self.db.find(f"SELECT user_id FROM Users WHERE email = ? AND name = ?", (email, name)).fetchone()
        if result != None:
            print("Login successful")
            self.user_id = result[0]
            self.accountMenu()
        else:
            print("Login failed")
            self.startMenu()

    def register(self):
        self.clearScreen()
        print("REGISTER MENU")
        email = input("Enter Email: ")
        name= input("Enter Name: ")
        result = self.db.put(f"INSERT INTO Users (email, name) VALUES (?, ?)", (email, name))
        if result[1]:
            print("Registration successful")
            self.pause()
            self.login()
        else:
            print(result[0])
            self.register()

    def viewProfile(self, edit=False):
        self.clearScreen()
        result = self.db.find(f"SELECT Users.name, Users.email, Companies.name, Company_User_Relationship.role FROM Users LEFT JOIN Company_User_Relationship ON Users.user_id = Company_User_Relationship.user LEFT JOIN Companies ON Companies.company_id = Company_User_Relationship.company WHERE Users.user_id = ?;", (self.user_id)).fetchone()
        if result != None:
            print("Name:", result[0])
            print("Email:", result[1])
            print("Company:", result[2], "Role:", result[3])
            if not edit:
                self.pause()
                self.accountMenu()
        else:
            print("Profile not found")
            self.pause()
            self.startMenu()
        
    def editProfile(self):
        self.viewProfile(True)
        print("EDIT PROFILE")
        print("1. Edit Name")
        print("2. Edit Email")
        choice = input("Enter choice: ")
        if choice == "1":
            name = input("Enter new name: ")
            self.db.put(f"UPDATE Users SET name = ? WHERE user_id = ?", (name, self.user_id))
            self.viewProfile(True)


    def viewAvailableJobs(self):
        self.clearScreen()
        print("AVAILABLE JOBS")
        result = self.db.find("SELECT job_id, description, address, created_date, predicted_end_datetime, price_job FROM Job_Offers RIGHT JOIN Job_Work ON Job_Work.job != Job_Offers.job_id").fetchall()
        self.displayMultiResult(result)
        self.pause()
        self.accountMenu()


    def viewCurrentJobs(self):
        self.clearScreen()
        print("YOURS CURRENT JOBS")
        result = self.db.find("SELECT job_id, description, address, created_date, predicted_end_datetime, price_job FROM Job_Offers LEFT JOIN Job_Work ON Job_Work.job == Job_Offers.job_id WHERE Job_Work.worker == ?", (self.user_id)).fetchall()
        self.displayMultiResult(result)
        
        choice = None
        while choice.isalpha() == False:
            print("Select a job (Y/N)")
            choice = input("Enter choice: ")
            if choice.lower() == "y":
                job_id = input("Enter job id: ")
                self.db.put("UPDATE Job_Work SET worker = ? WHERE job = ?", (self.user_id, job_id))
                self.viewCurrentJobs()

        self.pause()
        self.accountMenu()

    def accountMenu(self):
        self.clearScreen()
        print("ACCOUNT MENU")
        print("1. View Profile")
        print("2. Edit Profile")
        print("3. View Available Jobs")
        print("4. View Current Jobs")
        print("9. Logout")
        print("99. Delete Profile")
        choice = input("Enter choice: ")
        if choice == "1":
            self.viewProfile() # Show company, name, email.
        elif choice == "2":
            self.editProfile() # Edit company, name, email.
        elif choice == "3":
            self.viewAvailableJobs()
        elif choice == "4":
            self.viewCurrentJobs()
        elif choice == "4":
            self.logout()
            self.startMenu()
        elif choice == "99":
            print("Are you sure you want to delete your profile? (Y/N)")
            choice = input("Enter choice: ")
            if choice.lower() == "y":
                self.deleteProfile() # Delete profile
            else:
                self.accountMenu()
        else:
            print("Invalid choice")
            self.pause()
            self.accountMenu()

if __name__ == "__main__":
    main = Main()