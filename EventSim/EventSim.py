import os
import time
import mysql.connector
import random
from dotenv import load_dotenv
import datetime

#load_dotenv()

def create_connection():
    connection = mysql.connector.connect(
    host = 'localhost',
    user = 'timlinkous',
    password = 'zipcode1',
    database = 'starmeter'
    )
    return connection

conn = create_connection()

event_probabilities={
        'E1':0.23,
        'E2':0.07,
        'E3':0.05,
        'E4':0.05,
        'E5':0.06,
        'E6':0.03,
        'E7':0.02,
        'E8':0.02,
        'E9':0.03,
        'E10':0.03,
        'E11':0.03,
        'E12':0.03,
        'E13':0.04,
        'E14':0.01,
        'E15':0.03,
        'E16':0.02,
        'E17':0.04,
        'E18':0.01,
        'E19':0.01,
        'E20':0.02,
        'E21':0.02,
        'E22':0.01,
        'E23':0.01,
        'E24':0.01,
        'E25':0.01,
        'E26':0.01,
        'E27':0.02,
        'E28':0.01,
        'E29':0.02,
        'SC1':0.001,
        'SC2':0.001,
        'SC3':0.0045,
        'SC4':0.005,
        'SC5':0.001,
        'SD1':0.0005,
        'SD2':0.005,
        'SD3':0.0025,
        'SD4':0.001,
        'SD5':0.0035,
        'T1':0.0005,
        'T2':0.005,
        'T3':0.002,
        'T4':0.005,
        'L1':0.0005,
        'L2':0.001,
        'L3':0.0005,
        'L4':0.0015,
        'L5':0.0015,
        'L6':0.0075
}

event_descriptions = {
    'E1': 'Nothing happen',
    'E2': 'Public appearance',
    'E3': 'Got Award',
    'E4': 'Philanthropy/donation',
    'E5': 'New post on social media (positive)',
    'E6': 'New post on social media (negative)',
    'E7': 'Public argument/feud',
    'E8': 'Legal issue',
    'E9': 'Poor performance',
    'E10': 'Controversial statement',
    'E11': 'Attends high profile event',
    'E12': 'Cameo appearance',
    'E13': 'New project or franchise',
    'E14': 'Gets married/has child',
    'E15': 'New social media platform',
    'E16': 'Major news story',
    'E17': 'Celebrity collaboration',
    'E18': 'Health decline',
    'E19': 'Podcast appearance',
    'E20': 'Health fitness',
    'E21': 'Talk show appearance',
    'E22': 'Feature film',
    'E23': 'Scandalous clothing',
    'E24': 'Bizarre fashion choice',
    'E25': 'Mysterious post/teaser',
    'E26': 'Book/memoir',
    'E27': 'Candid photograph / normal day',
    'E28': 'Request of fans',
    'E29': 'Political alignment',
    'SC1': 'Releases new album/tour',
    'SC2': 'Hosts SNL',
    'SC3': 'Relationship drama',
    'SC4': 'Hit Song',
    'SC5': 'Launching a fashion line',
    'SD1': 'Carry torch at Olympics',
    'SD2': 'Music Performance',
    'SD3': 'Offensive comments',
    'SD4': 'Newfound public friendship with Bill Gates',
    'SD5': 'Featured in a new song',
    'T1': 'Developed new suit',
    'T2': 'Saved the world',
    'T3': 'Become a villain',
    'T4': 'Public appearance with iron man suit',
    'L1': 'Losses in NBA playoffs',
    'L2': 'Son gets drafted onto same team',
    'L3': 'Wins Olympic Gold Medal',
    'L4': 'Releases new shoe/product',
    'L5': 'Gets Injured',
    'L6': 'Sits out for rest'
}

#make sure the sum of the probability it's 1
print(sum(event_probabilities.values()))

category_1_events = {'E2', 'E3', 'E4', 'E5', 'E11', 'E12', 'E13', 'E14','E15', 'E16', 'E17', 'E18', 'E19', 'E20', 'E21', 'E22', 'E25', 'E26' }
category_2_events = {'E1', 'E10', 'E16', 'E24', 'E27', 'E28'}
category_3_events = {'E6', 'E7', 'E8', 'E9', 'E23', 'E29'}
category_4_events = {'SC1', 'SC2', 'SC3', 'SC4', 'SC5', 'SD1', 'SD2', 'SD3', 'SD4', 'SD5', 'T1', 'T2', 'T3', 'T4', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6'}

celebrities = ['Sabrina Carpenter', 'Snoop Dogg', 'Tony Stark', 'LeBron James']

def choose_event():
    events=list(event_probabilities.keys())
    probabilities = list(event_probabilities.values())
    event = random.choices(events,probabilities)[0]
    return event


def reset_probability_to_default(connection,user_id):
    cursor = connection.cursor()

    select_query = "select E1,E2,E3,E4,E5,E6,E7,E8,E9,E10,E11,E12,E13,E14,E15,E16,E17,E18,E19,E20,E21,E22,E23,E24,E25,E26,E27,E28,E29,SC1,SC2,SC3,SC4,SC5,SD1,SD2,SD3,SD4,SD5,T1,T2,T3,T4,L1,L2,L3,L4,L5,L6 from user_default_settings where user_id = %s"
    cursor.execute(select_query, (user_id,))
    default_probs = cursor.fetchone()

    #uptade the user_dynamic_preferences table
    update_query = """
    update user_dynamic_preferences set
    E1 = %s, E2 = %s, E3 = %s, E4 = %s, E5 = %s, E6 = %s, E7 = %s, E8 = %s, E9 = %s, E10 = %s, E11 = %s, E12 = %s, E13 = %s, E14 = %s, E15 = %s, E16 = %s, E17 = %s, E18 = %s, E19 = %s, E20 = %s, E21 = %s, E22 = %s, E23 = %s, E24 = %s, E25 = %s, E26 = %s, E27 = %s, E28 = %s, E29 = %s, SC1 = %s, SC2 = %s, SC3 = %s, SC4 = %s, SC5 = %s, SD1 = %s, SD2 = %s, SD3 = %s, SD4 = %s, SD5 = %s, T1 = %s, T2 = %s, T3 = %s, T4 = %s, L1 = %s, L2 = %s, L3 = %s, L4 = %s, L5 = %s, L6 = %s
    where user_id = %s
    """
    cursor.execute(update_query, (*default_probs, user_id))
    connection.commit()

    print(f"User {user_id} probabilities reset to default")


def situation_category_1_event(connection, event, associated_celebrity):
    cursor = connection.cursor()

    select_query = f"SELECT user_id, current_favorite, {event} FROM user_dynamic_preferences"
    cursor.execute(select_query)
    users = cursor.fetchall()

    for user in users:
        user_id, current_favorite, event_prob = user

        if random.random() < event_prob:
            # Change favorite and reset probability
            if current_favorite != associated_celebrity:
                update_query = "UPDATE user_dynamic_preferences SET current_favorite = %s WHERE user_id = %s"
                cursor.execute(update_query, (associated_celebrity, user_id))
                reset_probability_to_default(connection, user_id)

    connection.commit()


def situation_category_2_event(connection, event, associated_celebrity):
    cursor = connection.cursor()

    select_query = f"SELECT user_id, current_favorite, {event} FROM user_dynamic_preferences WHERE current_favorite = %s"
    cursor.execute(select_query, (associated_celebrity,))
    users = cursor.fetchall()

    for user in users:
        user_id, current_favorite, event_prob = user

        if random.random() < event_prob:
            # Change favorite
            new_favorite = random.choice([celeb for celeb in celebrities if celeb != associated_celebrity])
            update_query = "UPDATE user_dynamic_preferences SET current_favorite = %s WHERE user_id = %s"
            cursor.execute(update_query, (new_favorite, user_id))
            reset_probability_to_default(connection, user_id)

    connection.commit()


def situation_category_3_event(connection, event, associated_celebrity):
    cursor = connection.cursor()

    select_query = f"SELECT user_id, current_favorite, {event} FROM user_dynamic_preferences WHERE current_favorite = %s"
    cursor.execute(select_query, (associated_celebrity,))
    users = cursor.fetchall()

    for user in users:
        user_id, current_favorite, event_prob = user

        if random.random() < event_prob:
            new_favorite = random.choice([celeb for celeb in celebrities if celeb != associated_celebrity])
            update_query = "UPDATE user_dynamic_preferences SET current_favorite = %s WHERE user_id = %s"
            cursor.execute(update_query, (new_favorite, user_id))
            reset_probability_to_default(connection, user_id)
        else:
            new_prob = min(event_prob + 0.15, 1.0)  # Increase event probability for the future
            update_prob_query = f"UPDATE user_dynamic_preferences SET {event} = %s WHERE user_id = %s"
            cursor.execute(update_prob_query, (new_prob, user_id))

    connection.commit()
    
def situation_category_4_event(connection, event, associated_celebrity):
    cursor = connection.cursor()

    select_query = f"SELECT user_id, current_favorite, {event} FROM user_dynamic_preferences WHERE current_favorite = %s"
    cursor.execute(select_query, (associated_celebrity,))
    users = cursor.fetchall()

    for user in users:
        user_id, current_favorite, event_prob = user

        if random.random() < event_prob:
            new_favorite = random.choice([celeb for celeb in celebrities if celeb != associated_celebrity])
            update_query = "UPDATE user_dynamic_preferences SET current_favorite = %s WHERE user_id = %s"
            cursor.execute(update_query, (new_favorite, user_id))
            reset_probability_to_default(connection, user_id)

    connection.commit()

def get_total_fans(connection):
    cursor = connection.cursor(dictionary=True)
    fan_counts = {celeb: 0 for celeb in celebrities}
    
    cursor.execute("SELECT current_favorite, COUNT(*) as count FROM user_dynamic_preferences GROUP BY current_favorite")
    results = cursor.fetchall()
    
    for row in results:
        if row['current_favorite'] in fan_counts:
            fan_counts[row['current_favorite']] = row['count']
    
    return fan_counts
    print("fan_counts")

def log_event(connection, event_date, event, associated_celebrity):
    cursor = connection.cursor()
    
    # Get the current fan count for the celebrity
    fan_counts = get_total_fans(connection)
    current_fan_count = fan_counts.get(associated_celebrity, 0)
    
    insert_query = """
    INSERT INTO event_log (event_date, celebrity, event_description, current_fan_count)
    VALUES (%s, %s, %s, %s);
    """
    
    cursor.execute(insert_query, (event_date, associated_celebrity, event_descriptions[event], current_fan_count))
    
    connection.commit()
    print(f"Event {event} with {associated_celebrity} logged. Current fan count: {current_fan_count}")


def run_event_sum(connection, start_date, num_days=180):
    for day in range(num_days):
        current_date = start_date + datetime.timedelta(days=day)
        print(f"Simulating day {day+1}... ({current_date})")

        event = choose_event()
        event_description = event_descriptions.get(event, "Unknown event")
        associated_celebrity = random.choice(celebrities)
        print(f"Event {event} occurred ({event_description}), associated with {associated_celebrity}")

        if event in category_1_events:
            situation_category_1_event(conn, event, associated_celebrity)
        elif event in category_2_events:
            situation_category_2_event(conn, event, associated_celebrity)
        elif event in category_3_events:
            situation_category_3_event(conn, event, associated_celebrity)
        elif event in category_4_events:
            situation_category_4_event(conn, event, associated_celebrity)

        log_event(connection, current_date, event, associated_celebrity)

        fan_counts = get_total_fans(connection)
        print(f"Current fan counts: {fan_counts}")

        time.sleep(10)

    print("Event simulation complete.")

if __name__ == "__main__":
    conn = create_connection()
    if conn.is_connected():
        print("Connected to the database")
        start_date = datetime.date(2024, 3, 12)
        run_event_sum(conn, start_date, num_days=180)
        conn.close()
        print("Database connection closed")
    else:
        print("Connection failed")