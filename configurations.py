from pymongo import MongoClient


client = MongoClient("mongodb+srv://admin:admin123@cluster0.gtldf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client.employee_db

collection = db["employee_data"]