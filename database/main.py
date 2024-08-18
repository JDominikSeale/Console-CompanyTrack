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
        if type(values) == tuple:
            values = self.valueClean(values)
        else:
            values = (values,)
        try:
            print(values)
            self.cursor.execute(command, values)
            self.conn.commit()
            return self.cursor.lastrowid, True
        except sqlite3.IntegrityError:
            return "Email already exists", False
        except Exception as e:
            print(e)
            return e, False

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
    b = a.put("INSERT INTO Companies (name) VALUES (?)" , ("testCompany6",))
    print(b)