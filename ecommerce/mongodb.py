from pymongo import MongoClient
 
# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
 
# Check if the connection is successful
try:
    # List available databases
    databases = client.list_database_names()
    print(" MongoDB Connected! Databases:", databases)
except Exception as e:
    print(" MongoDB Connection Failed:", e)
 
# Access a specific database
db = client["StudentForm"]  # Replace with your database name