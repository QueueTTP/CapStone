#this file only needs to run once! if you run multiple times, it will add more user(you don't want that)


import dotenv
import mysql.connector
import random
import os
from dotenv import load_dotenv

load_dotenv()

def create_connection():
    connection = mysql.connector.connect(
    host = 'test-db.c3u680mys7w2.us-east-1.rds.amazonaws.com',
    user = 'admin',
    password = 'zip.code123!',
    database = 'starmeter'
    )
    return connection


conn = create_connection()




def create_user_default_table(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_default_settings (
        user_id INT  PRIMARY KEY,
        E1 FLOAT,AUTO_INCREMENT
        E2 FLOAT,
        E3 FLOAT,
        E4 FLOAT,
        E5 FLOAT,
        E6 FLOAT,
        E7 FLOAT,
        E8 FLOAT,
        E9 FLOAT,
        E10 FLOAT,
        E11 FLOAT,
        E12 FLOAT,
        E13 FLOAT,
        E14 FLOAT,
        E15 FLOAT,
        E16 FLOAT,
        E17 FLOAT,
        E18 FLOAT,
        E19 FLOAT,
        E20 FLOAT,
        E21 FLOAT,
        E22 FLOAT,
        E23 FLOAT,
        E24 FLOAT,
        E25 FLOAT,
        E26 FLOAT,
        E27 FLOAT,
        E28 FLOAT,
        E29 FLOAT,
        SC1 FLOAT,
        SC2 FLOAT,
        SC3 FLOAT,
        SC4 FLOAT,
        SC5 FLOAT,
        SD1 FLOAT,
        SD2 FLOAT,
        SD3 FLOAT,
        SD4 FLOAT,
        SD5 FLOAT,
        T1 FLOAT,
        T2 FLOAT,
        T3 FLOAT,
        T4 FLOAT,
        L1 FLOAT,
        L2 FLOAT,
        L3 FLOAT,
        L4 FLOAT,
        L5 FLOAT,
        L6 FLOAT
    );
    """
    
    cursor = connection.cursor()
    cursor.execute(create_table_query)
    connection.commit()
    print("User Default Settings table created successfully")

# Create the table
create_user_default_table(conn)

#normal distribution detail % is >0
def generate_prob(mean,std_dev):
    prob = -1
    while prob<0:
        prob = random.gauss(mean,std_dev)
    return prob


def populate_user_defaults(connection, num_users=10000):
    insert_query = """
    INSERT INTO user_default_settings (
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

    #normal distribution set up
    means = {
        'E1' :0.03,
        'E2':0.15,
        'E3':0.1,
        'E4':0.09,
        'E5':0.08,
        'E6':0.15,
        'E7':0.20,
        'E8':0.3,
        'E9':0.15,
        'E10':0.15,
        'E11':0.1,
        'E12':0.12,
        'E13':0.08,
        'E14':0.2,
        'E15':0.25,
        'E16':0.1,
        'E17':0.15,
        'E18':0.18,
        'E19':0.22,
        'E20':0.26,
        'E21':0.14,
        'E22':0.2,
        'E23':0.15,
        'E24':0.13,
        'E25':0.15,
        'E26':0.2,
        'E27':0.25,
        'E28':0.3,
        'E29':0.1,
        'SC1':0.2,
        'SC2':0.15,
        'SC3':0.05,
        'SC4':0.25,
        'SC5':0.1,
        'SD1':0.15,
        'SD2':0.1,
        'SD3':0.2,
        'SD4':0.2,
        'SD5':0.05,
        'T1':0.15,
        'T2':0.3,
        'T3':0.6,
        'T4':0.2,
        'L1':0.25,
        'L2':0.2,
        'L3':0.15,
        'L4':0.05,
        'L5':0.05,
        'L6':0.07
    }
    stddev=0.1
    
    for _ in range(num_users):
        values = tuple(generate_prob(means[key],stddev) for key in means.keys())
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