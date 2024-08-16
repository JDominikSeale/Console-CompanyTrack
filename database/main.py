import sqlite3

class db():
    def __init__(self):
        self.conn = sqlite3.connect("CompanyTrack.db")
        self.cursor = self.conn.cursor()

    def find(self, command, values=None):
        if values != None:
            values = self.valueClean(values)
            result = self.cursor.execute(command, values)
        else:
            result = self.cursor.execute(command)
        return result
    
    def put(self, command, values):
        values = self.valueClean(values)
        try:
            self.cursor.execute(command, values)
            self.conn.commit()
        except sqlite3.IntegrityError:
            return "Email already exists", False
        except Exception as e:
            print(e)
    

    def valueClean(self, values):
        if type(values) == tuple:
            values = [str(value) for value in values]
        else:
            values = str(values)
        return values

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    a = db()
    b = a.find("SELECT job_id, description, address, created_date, predicted_end_datetime, price_job FROM Job_Offers RIGHT JOIN Job_Work ON Job_Work.worker != Job_Offers.job_id")
    print(b)