#this file only needs to run once! if you run multiple times, it will add more user(you don't want that)


import mysql.connector
import random


def create_connection():
    connection = mysql.connector.connect(
        host="localhost",         
        user="qian",     
        password="zipcode0", 
        database="starmeter"  
    )
    return connection


conn = create_connection()




def create_user_default_table(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_default_settings (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        event_1_prob FLOAT,
        event_2_prob FLOAT,
        event_3_prob FLOAT,
        event_4_prob FLOAT,
        event_5_prob FLOAT,
        event_6_prob FLOAT,
        event_7_prob FLOAT,
        event_8_prob FLOAT,
        event_9_prob FLOAT,
        event_10_prob FLOAT
    );
    """
    
    cursor = connection.cursor()
    cursor.execute(create_table_query)
    connection.commit()
    print("User Default Settings table created successfully")

# Create the table
create_user_default_table(conn)


def populate_user_defaults(connection, num_users=10000):
    insert_query = """
    INSERT INTO user_default_settings (
        event_1_prob, event_2_prob, event_3_prob, event_4_prob, 
        event_5_prob, event_6_prob, event_7_prob, event_8_prob, 
        event_9_prob, event_10_prob
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    
    cursor = connection.cursor()
    
    for _ in range(num_users):
        values = tuple(random.uniform(0, 1) for _ in range(10))
        cursor.execute(insert_query, values)
    
    connection.commit()
    print(f"{num_users} users inserted into user_default_settings")

# Populate the table
populate_user_defaults(conn, num_users=10000)

def verify_insertion(connection):
    select_query = "SELECT COUNT(*) FROM user_default_settings;"
    
    cursor = connection.cursor()
    cursor.execute(select_query)
    
    count = cursor.fetchone()[0]
    print(f"Total records in user_default_settings: {count}")

# Verify the data
verify_insertion(conn)

conn.close()
print("Connection closed")