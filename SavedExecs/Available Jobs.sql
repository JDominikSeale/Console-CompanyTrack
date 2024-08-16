#Find available jobs 

SELECT job_id, description, address, created_date, predicted_end_datetime, price_job
FROM Job_Offers
RIGHT JOIN Job_Work ON Job_Work.worker != Job_Offers.job_id;