
SELECT job_id, address, description, created_date, predicted_end_datetime, actual_end_date, price_job
FROM Job_Offers
JOIN Job_Work ON Job_Work.job = Job_Offers.job_id AND Job_Work.worker = 1
WHERE actual_end_date IS NOT NULL;