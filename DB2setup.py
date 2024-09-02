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
        E1 Float,
        E2 Float,
        E3 Float,
        E4 Float,
        E5 Float,
        E6 Float,
        E7 Float,
        E8 Float,
        E9 Float,
        E10 Float,
        E11 Float,
        E12 Float,
        E13 Float,
        E14 Float,
        E15 Float,
        E16 Float,
        E17 Float,
        E18 Float,
        E19 Float,
        E20 Float,
        E21 Float,
        E22 Float,
        E23 Float,
        E24 Float,
        E25 Float,
        E26 Float,
        E27 Float,
        E28 Float,
        E29 Float,
        SC1 Float,
        SC2 Float,
        SC3 Float,
        SC4 Float,
        SC5 Float,
        SD1 Float,
        SD2 Float,
        SD3 Float,
        SD4 Float,
        SD5 Float,
        T1 Float,
        T2 Float,
        T3 Float,
        T4 Float,
        L1 Float,
        L2 Float,
        L3 Float,
        L4 Float,
        L5 Float,
        L6 Float,
        Foreign key (user_id) references user_default_settings(user_id)
    );

"""


    cursor = connection.cursor()
    cursor.execute(create_table_query)
    connection.commit()
    print("User Dynamic Preferences table created successfully")

celebrities = ["Sabrina Carpenter", "Snoop Dogg", "Tony Stark", "LeBron James"]

def populate_user_dynamic_preferences(connection):
    select_query = "SELECT * FROM user_default_settings;"
    insert_query = """
    INSERT INTO user_dynamic_preferences (
        E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, 
        E16, E17, E18, E19, E20, E21, E22, E23, E24, E25, E26, E27, E28, 
        E29, SC1, SC2, SC3, SC4, SC5, SD1, SD2, SD3, SD4, SD5, T1, T2, 
        T3, T4, L1, L2, L3, L4, L5, L6
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s);
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