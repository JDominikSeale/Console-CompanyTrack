CREATE TABLE IF NOT EXISTS Companies(
company_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
name char(100),
email char(100)
);

CREATE TABLE IF NOT EXISTS Users(
user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
name char(100),
email char(100) UNIQUE
);

CREATE TABLE IF NOT EXISTS Company_User_Relationship(
role INTEGER,
company INTEGER,
user INTEGER,
FOREIGN KEY(company) REFERENCES Companies(company_id),
FOREIGN KEY(user) REFERENCES User(user_id)
);

CREATE TABLE IF NOT EXISTS Job_Offers (
    job_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    address TEXT,
    description TEXT,
    created_date DATE DEFAULT CURRENT_DATE,
    predicted_end_datetime DATETIME,
    actual_end_date DATETIME,
    price_job DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS Job_Work(
job INTEGER,
worker INTEGER,
FOREIGN KEY(job) REFERENCES Job_Offers(job_id),
FOREIGN KEY (worker) REFERENCES Users(user_id)
)

