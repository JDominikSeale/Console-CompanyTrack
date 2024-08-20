import database, time, hashlib


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
        choice = None
        while choice.isalpha() == False:
            print("Select a job? (Y/N)")
            choice = input("Enter choice: ")
            if choice.lower() == "y":
                job_id = input("Enter job id: ")
                self.db.put("UPDATE Job_Work SET worker = ? WHERE job = ?", (self.user_id, job_id))
                self.viewCurrentJobs()
        self.pause()
        self.accountMenu()


    def viewCurrentJobs(self):
        self.clearScreen()
        print("YOURS CURRENT JOBS")
        result = self.db.find("SELECT job_id, description, address, created_date, predicted_end_datetime, price_job FROM Job_Offers LEFT JOIN Job_Work ON Job_Work.job == Job_Offers.job_id WHERE Job_Work.worker == ?", (self.user_id)).fetchall()
        self.displayMultiResult(result)
        choice = None
        while choice.isalpha() == False:
            print("Would you like to update a job? (Y/N)")
            choice = input("Enter choice: ")
            if choice.lower() == "y":
                job_id = input("Enter job id: ")
                self.db.put("UPDATE Job_Offers SET actual_end_datetime = ? WHERE job_id = ?", (time.datetime.now(), job_id))
        self.accountMenu()

    def logout(self):
        self.user_id = None
        self.startMenu()

    def deleteProfile(self):
        self.db.put("DELETE FROM Users WHERE user_id = ?", (self.user_id))
        self.db.put("DELETE FROM Company_User_Relationship WHERE user = ?", (self.user_id))
        self.user_id = None
        self.startMenu()

    def viewPastJobs(self):
        self.clearScreen()
        result = self.db.find("SELECT job_id, address, description, created_date, predicted_end_datetime, actual_end_date, price_job FROM Job_Offers JOIN Job_Work ON Job_Work.job = Job_Offers.job_id AND Job_Work.worker = ? WHERE actual_end_date IS NOT NULL", (self.user_id)).fetchall()
        print("YOURS PAST JOBS")
        self.displayMultiResult(result)

    def createCompany(self):
        self.clearScreen()
        print("CREATE COMPANY")
        name = input("Enter company name: ")
        result = self.db.put("INSERT INTO Companies (name) VALUES (?)", (name))
        if result[1] == False:
            print("Error Creating Company")
            self.pause()
            self.companyManagement()
        else:
            companyID = result[0]
            code = self.hashing(name)
            result = self.db.put("INSERT INTO Codes (code, company) VALUES (?, ?)", (code, companyID))
            result = self.db.put("INSERT INTO Company_User_Relationship (company, user, role) VALUES (?, ?, 'owner')", (companyID, self.user_id))

    def joinCompany(self):
        self.clearScreen()
        print("JOIN COMPANY")
        code = input("Enter company code: ")
        result = self.db.find("SELECT Companies.name FROM Companies JOIN Codes ON Codes.company_id = Companies.company_id WHERE Codes.code = ?", (code)).fetchone()
        if result != None:
            print(f"Are you sure you wish to join {result} (Y/N)")
            choice = input("Enter choice: ")
            if choice.lower() == "y":
                self.db.put("INSERT INTO Company_User_Relationship (company, user, role) VALUES (?, ?, 'worker')", (result, self.user_id))
                if result[1] == False:
                    print("Error Joining Company")
                    self.pause()
                    self.companyManagement()
                else:
                    print(f"Joined {result}")
                    self.pause()
                    self.companyManagement()


    def leaveCompany(self):
        self.clearScreen()
        print("LEAVE COMPANY")
        choice = input("Are you sure you wish to leave your company? (Y/N)")
        if choice.lower() == "y":
            print("Please enter the name of the company you wish to leave")
            self.viewCompaies()
            company = input("Enter company name: ")
            result = self.db.put("DELTE FROM Company_User_Relationship WHERE company = ? AND user = ?", (company, self.user_id))
            if result[1] == True:
                print(f"Left {company}")
                self.pause()
                self.companyManagement()
            else:
                print("Error Leaving Company")
                self.pause()
                self.companyManagement()
        elif choice.lower() == "n":
            self.companyManagement()

    def viewCompanies(self, calledOn=False):
        if calledOn == False:
            self.clearScreen()
        print("COMPANIES")
        result = self.db.find("SELECT Companies.name FROM Companies JOIN Company_User_Relationship ON Company_User_Relationship.company = Companies.company_id JOIN Users ON Users.user_id = Company_User_Relationship.user WHERE Users.user_id = ?", (self.user_id)).fetchall()
        if result == ():
            print("No Companies")
        else:
            self.displayMultiResult(result)
            if calledOn == False:
                self.pause()
                self.companyManagement()
            return result

    def editCompanyName(self):
        self.clearScreen()
        print("EDIT COMPANY NAME")
        compaines = self.viewCompanies()
        companyID = input("Enter company ID: ")
        if companyID in compaines:
            name = input("Enter new company name: ")
            self.db.put("UPDATE Companies SET name = ? WHERE company_id = ?", (name, companyID))
            print("Company name updated")
            self.pause()
            self.companyManagement()

    def editCompanyCode(self):
        self.clearScreen()
        print("EDIT COMPANY CODE")
        compaines = self.viewCompanies()
        companyID = input("Enter company ID: ")
        if companyID in compaines:
            code = self.hashing()
            self.db.put("UPDATE Codes SET code = ? WHERE company_id = ?", (code, companyID))
            print("Company code updated")
            self.pause()
            self.companyManagement()


    def editCompany(self):
        self.clearScreen()
        print("EDIT COMPANY")
        print("1. Edit Company Name")
        print("2. Edit Company Code")
        print("3. Edit Company Role")
        print("9. Back")
        choice = input("Enter choice: ")
        if choice == "1":
            self.editCompanyName()
        elif choice == "2":
            self.editCompanyCode()
        elif choice == "9":
            self.companyManagement()
        else:
            print("Invalid choice")
            self.pause()
            self.editCompany()

    def companyManagement(self):
        self.clearScreen()
        print("COMPANY MANAGEMENT")
        print("1. Create a Company")
        print("2. Join  a Company")
        print("3. Leave a Company")
        print("4. View Companies")
        print("5. Edit Company")
        print("9. Back")
        choice = input("Enter choice: ")
        if choice == "1":
            self.createCompany()
        elif choice == "2":
            self.joinCompany()
        elif choice == "3":
            self.leaveCompany()
        elif choice == "4":
            self.viewCompanies(True)
        elif choice == "5":
            self.editCompany()
        elif choice == "9":
            self.accountMenu()
        else:
            print("Invalid choice")
            self.pause()
            self.companyManagement()

    def hashing(self, values):
        m = hashlib.sha256()
        m.update(str(int(time.time())).encode())
        m.update(values.encode())
        return m.hexdigest()

    def accountMenu(self):
        self.clearScreen()
        print("ACCOUNT MENU")
        print("1. View Profile") #done
        print("2. Edit Profile") #done
        print("3. View Available Jobs") #done
        print("4. View Current Jobs") #done
        print("5. View Past Jobs")
        print("6. Company Management")
        print("9. Logout") #done
        print("99. Delete Profile") #done
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