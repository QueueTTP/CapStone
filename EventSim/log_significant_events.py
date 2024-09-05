import mysql.connector
from datetime import datetime
import pandas as pd

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',      
            user='timlinkous',            
            password='zipcode1',  
            database='starmeter'   
        )
        if connection.is_connected():
            print("Successfully connected to the database")
            return connection
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None

from datetime import datetime

def get_significant_changes(connection):
    cursor = connection.cursor()

    # Retrieve current and previous sentiment values
    select_query = """
    SELECT udp.user_id, 
       uds.E1 as prev_E1, udp.E1 as curr_E1,
       uds.E2 as prev_E2, udp.E2 as curr_E2,
       uds.E3 as prev_E3, udp.E3 as curr_E3,
       uds.E4 as prev_E4, udp.E4 as curr_E4,
       uds.E5 as prev_E5, udp.E5 as curr_E5,
       uds.E6 as prev_E6, udp.E6 as curr_E6,
       uds.E7 as prev_E7, udp.E7 as curr_E7,
       uds.E8 as prev_E8, udp.E8 as curr_E8,
       uds.E9 as prev_E9, udp.E9 as curr_E9,
       uds.E10 as prev_E10, udp.E10 as curr_E10,
       uds.E11 as prev_E11, udp.E11 as curr_E11,
       uds.E12 as prev_E12, udp.E12 as curr_E12,
       uds.E13 as prev_E13, udp.E13 as curr_E13,
       uds.E14 as prev_E14, udp.E14 as curr_E14,
       uds.E15 as prev_E15, udp.E15 as curr_E15,
       uds.E16 as prev_E16, udp.E16 as curr_E16,
       uds.E17 as prev_E17, udp.E17 as curr_E17,
       uds.E18 as prev_E18, udp.E18 as curr_E18,
       uds.E19 as prev_E19, udp.E19 as curr_E19,
       uds.E20 as prev_E20, udp.E20 as curr_E20,
       uds.E21 as prev_E21, udp.E21 as curr_E21,
       uds.E22 as prev_E22, udp.E22 as curr_E22,
       uds.E23 as prev_E23, udp.E23 as curr_E23,
       uds.E24 as prev_E24, udp.E24 as curr_E24,
       uds.E25 as prev_E25, udp.E25 as curr_E25,
       uds.E26 as prev_E26, udp.E26 as curr_E26,
       uds.E27 as prev_E27, udp.E27 as curr_E27,
       uds.E28 as prev_E28, udp.E28 as curr_E28,
       uds.E29 as prev_E29, udp.E29 as curr_E29
FROM user_dynamic_preferences udp
JOIN user_default_settings uds ON udp.user_id = uds.user_id;
    """
    
    cursor.execute(select_query)
    data = cursor.fetchall()
    
    significant_events = []
    
    for row in data:
        user_id = row[0]
        prev_values = row[1::2]  # odd indices are previous values
        curr_values = row[2::2]  # even indices are current values
        
        changes = []
        for prev, curr in zip(prev_values, curr_values):
            if prev != 0:
                change_percentage = ((curr - prev) / prev) * 100
            else:
                change_percentage = 0 if curr == 0 else 100  # Assume 100% increase if prev was 0
            changes.append(change_percentage)
        
        # Check if any change is 10% or more
        if any(abs(change) >= 10 for change in changes):
            event_date = datetime.now()
            event_description = f"Significant sentiment change detected for user {user_id}"
            total_gains = sum(1 for change in changes if change >= 10)
            total_losses = sum(1 for change in changes if change <= -10)
            average_change = sum(changes) / len(changes)
            
            significant_events.append((event_date, event_description, total_gains, total_losses, average_change))
    
    return significant_events

def log_significant_events(connection, events):
    insert_query = """
    INSERT INTO significant_events (event_date, event_description, total_gains, total_losses, percentage_change)
    VALUES (%s, %s, %s, %s, %s);
    """
    cursor = connection.cursor()
    cursor.executemany(insert_query, events)
    connection.commit()

def main():
    connection = create_connection()
    if connection and connection.is_connected():
        print("Connected to the database")
        events = get_significant_changes(connection)
        if events:
            log_significant_events(connection, events)
            print(f"Logged {len(events)} significant events")
        else:
            print("No significant events found")
        connection.close()
        print("Connection closed")
    else:
        print("Failed to connect")

if __name__ == "__main__":
    main()