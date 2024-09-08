import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

#tim added to create the 3rd table that logs the events

#load_dotenv()

def create_connection():
    connection = mysql.connector.connect(
    host = 'test-db.c3u680mys7w2.us-east-1.rds.amazonaws.com',
    user = 'admin',
    password = 'zip.code123!',
    database = 'starmeter'
    )
    return connection

def create_event_log_table(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS event_log (
        event_id INT AUTO_INCREMENT PRIMARY KEY,
        event_date DATE,
        celebrity VARCHAR(50),
        event_description VARCHAR(255),
        current_fan_count INT
    );
    """

    cursor = connection.cursor()
    cursor.execute(create_table_query)
    connection.commit()
    print("Event Log table created successfully")

conn = create_connection()
create_event_log_table(conn)
conn.close()
