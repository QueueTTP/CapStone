import mysql.connector
import random

def create_connection():
    connection = mysql.connector.connect(
        host ="localhost",
        user = "qian",
        password = "zipcode0",
        database = "starmeter"
    )
    return connection


def create_user_dynamic_table(connection):
    create_table_query = """
    create table if not exists user_dynamic_preferences(
        user_id INT PRIMARY KEY,
        current_favorite VARCHAR(50),
        event_1_prob Float,
        event_2_prob Float,
        event_3_prob Float,
        event_4_prob Float,
        event_5_prob Float,
        event_6_prob Float,
        event_7_prob Float,
        event_8_prob Float,
        event_9_prob Float,
        event_10_prob Float,
        Foreign key (user_id) references user_default_settings(user_id)
    );

"""


    cursor = connection.cursor()
    cursor.execute(create_table_query)
    connection.commit()
    print("User Dynamic Preferences table created successfully")

celebrities = ["Sabrina Carpenter", "Snoop Dogg", "Tony Stark", "LeBron James"]

def populate_user_dynamic_preferences(connection):
    select_query = "SELECT user_id, event_1_prob, event_2_prob, event_3_prob, event_4_prob, event_5_prob, event_6_prob, event_7_prob, event_8_prob, event_9_prob, event_10_prob FROM user_default_settings;"
    insert_query = """
    INSERT INTO user_dynamic_preferences (
        user_id, current_favorite, event_1_prob, event_2_prob, event_3_prob, event_4_prob, 
        event_5_prob, event_6_prob, event_7_prob, event_8_prob, event_9_prob, event_10_prob
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    
    cursor = connection.cursor()
    cursor.execute(select_query)
    user_data = cursor.fetchall()
    
    for user in user_data:
        user_id = user[0]
        probs = user[1:]
        current_favorite = random.choice(celebrities)
        
        values = (user_id, current_favorite) + probs
        cursor.execute(insert_query, values)
    
    connection.commit()
    print("User Dynamic Preferences populated with initial data")


if __name__ == "__main__":
    conn = create_connection()
    if conn.is_connected():
        print("Connected to the database")
        create_user_dynamic_table(conn)
        populate_user_dynamic_preferences(conn)
        conn.close()
        print("Connection closed")
    else:
        print("Failed to connect")