SELECT * FROM Users WHERE user_id = 1;

SELECT name, email FROM Users WHERE user_id = 1;

SELECT Users.name, Users.email, Companies.name FROM Users 
LEFT JOIN Company_User_Relationship ON Users.user_id = Company_User_Relationship.user
LEFT JOIN Companies ON Companies.company_id = Company_User_Relationship.company;

SELECT Users.name, Users.email, Companies.name FROM Users 
LEFT JOIN Company_User_Relationship ON Users.user_id = Company_User_Relationship.user
LEFT JOIN Companies ON Companies.company_id = Company_User_Relationship.company
WHERE Users.user_id = 1;

SELECT Users.name, Users.email, Companies.name, Company_User_Relationship.role FROM Users 
LEFT JOIN Company_User_Relationship ON Users.user_id = Company_User_Relationship.user
LEFT JOIN Companies ON Companies.company_id = Company_User_Relationship.company
WHERE Users.user_id = 1;