import mysql.connector
from dotenv import load_dotenv
import os

#tim added to create the 3rd table that logs the events

#load_dotenv()

def create_connection():
    connection = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'zipcode123',
    database = 'starmeter_sim'
    )
    return connection

def create_event_log_table(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS event_log (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_date DATE,
    celebrity VARCHAR(50),
    event_description VARCHAR(255),
    fans_gained INT,
    fans_lost INT
    );
    """
    
    cursor = connection.cursor()
    cursor.execute(create_table_query)
    connection.commit()
    print("Event Log table created successfully")

conn = create_connection()
create_event_log_table(conn)
conn.close()