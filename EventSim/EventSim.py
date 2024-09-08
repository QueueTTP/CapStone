import datetime
import os
import time
import mysql.connector
import random


def create_connection():
    connection = mysql.connector.connect(
    host = 'test-db.c3u680mys7w2.us-east-1.rds.amazonaws.com',
    user = 'admin',
    password = 'zip.code123!',
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
    'E1': 'Editorial Article',
    'E2': 'Public appearance',
    'E3': 'Wins Award',
    'E4': 'Philanthropy/donation',
    'E5': 'Social media post (pos)',
    'E6': 'Social media post (neg)',
    'E7': 'Public argument/feud',
    'E8': 'Legal issues',
    'E9': 'Poor performance',
    'E10': 'Controversial statement',
    'E11': 'Attends high profile event',
    'E12': 'Cameo appearance',
    'E13': 'New project and franchise',
    'E14': 'Gets married',
    'E15': 'New social media platform',
    'E16': 'Major news story',
    'E17': 'Celebrity collaboration',
    'E18': 'Health declines',
    'E19': 'Podcast appearance',
    'E20': 'Health & fitness photo',
    'E21': 'Talk show appearance',
    'E22': 'New Feature film',
    'E23': 'Scandalous clothing',
    'E24': 'Bizarre fashion choice',
    'E25': 'Teaser released',
    'E26': 'Book/memoir released',
    'E27': 'Candid public photos',
    'E28': 'Reacts to fan requests',
    'E29': 'Political statements',
    'SC1': 'Releases new album/tour',
    'SC2': 'Hosts SNL',
    'SC3': 'Relationship drama',
    'SC4': 'Hit Song tops charts',
    'SC5': 'Launches fashion line',
    'SD1': 'Carries Olympic torch',
    'SD2': 'Music Performance',
    'SD3': 'Offensive comments',
    'SD4': 'Public friendship with ...',
    'SD5': 'Featured in a new song',
    'T1': 'Develops new suit',
    'T2': 'Saves the world',
    'T3': 'Becomes a villain',
    'T4': 'Wears new Iron Man suit',
    'L1': 'Losses in NBA playoffs',
    'L2': 'Son drafted same team',
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

# updated to include unique events for only those celebs
def choose_event(celebrity):
    if celebrity == 'Sabrina Carpenter':
        events = list(event_probabilities.keys())
        events = [e for e in events if e.startswith('E') or e.startswith('SC')]
    elif celebrity == 'Snoop Dogg':
        events = list(event_probabilities.keys())
        events = [e for e in events if e.startswith('E') or e.startswith('SD')]
    elif celebrity == 'Tony Stark':
        events = list(event_probabilities.keys())
        events = [e for e in events if e.startswith('E') or e.startswith('T')]
    elif celebrity == 'LeBron James':
        events = list(event_probabilities.keys())
        events = [e for e in events if e.startswith('E') or e.startswith('L')]
    else:
        events = [e for e in event_probabilities.keys() if e.startswith('E')]
    
    probabilities = [event_probabilities[e] for e in events]
    total_prob = sum(probabilities)
    normalized_probabilities = [p / total_prob for p in probabilities]
    
    return random.choices(events, normalized_probabilities)[0]


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

    #print(f"User {user_id} probabilities reset to default")


def situation_category_1_event(connection, event, associated_celebrity):
    cursor = connection.cursor()

    select_query = f"select user_id, current_favorite, {event} from user_dynamic_preferences"
    cursor.execute(select_query)
    users = cursor.fetchall()

    for user in users:
        user_id = user[0]
        current_favorite = user[1]
        event_prob = user[2]

        #should change or not, Dice rolling!!!
        if random.random() < event_prob:
            new_favorite = random.choice(celebrities)
            update_query = "update user_dynamic_preferences set current_favorite = %s where user_id = %s"
            cursor.execute(update_query, (new_favorite, user_id))
            reset_probability_to_default(connection, user_id)
            #print(f"User {user_id} changed favorite to {associated_celebrity} due to event {event_descriptions[event]}")

    connection.commit()


def situation_category_2_event(connection, event, associated_celebrity):
    cursor = connection.cursor()

    select_query = f"SELECT user_id, current_favorite, {event} FROM user_dynamic_preferences WHERE current_favorite = %s"
    cursor.execute(select_query, (associated_celebrity,))
    users = cursor.fetchall()

    for user in users:
        user_id = user[0]
        event_prob = user[2]

        #should change or not, Dice rolling!!!
        if random.random() < event_prob:
            new_favorite = random.choice([celeb for celeb in celebrities if celeb != associated_celebrity])
            update_query = "UPDATE user_dynamic_preferences SET current_favorite = %s WHERE user_id = %s"
            cursor.execute(update_query, (new_favorite, user_id))
            reset_probability_to_default(connection, user_id)
            #print(f"User {user_id} changed favorite from {associated_celebrity} to {new_favorite} due to event {event_descriptions[event]}")

    connection.commit()


def situation_category_3_event(connection, event, associated_celebrity):
    cursor = connection.cursor()

    select_query = f"SELECT user_id, current_favorite, {event} FROM user_dynamic_preferences WHERE current_favorite = %s"
    cursor.execute(select_query, (associated_celebrity,))
    users = cursor.fetchall()

    for user in users:
        user_id = user[0]
        event_prob = user[2]

        #should change or not, Dice rolling!!!
        if random.random() < event_prob:
            new_favorite = random.choice([celeb for celeb in celebrities if celeb != associated_celebrity])
            update_query = "UPDATE user_dynamic_preferences SET current_favorite = %s WHERE user_id = %s"
            cursor.execute(update_query, (new_favorite, user_id))
            reset_probability_to_default(connection, user_id)
            #print(f"User {user_id} changed favorite from {associated_celebrity} to {new_favorite} due to event {event}")
        else:
            new_prob = min(event_prob + 0.15, 1.0)
            update_prob_query = f"UPDATE user_dynamic_preferences SET {event} = %s WHERE user_id = %s"
            cursor.execute(update_prob_query, (new_prob, user_id))
            #print(f"User {user_id}'s probability for event {event_descriptions[event]} increased to {new_prob}")

    connection.commit()
    
def situation_category_4_event(connection, event, associated_celebrity):
    cursor = connection.cursor()

    select_query = f"SELECT user_id, current_favorite, {event} FROM user_dynamic_preferences WHERE current_favorite = %s"
    cursor.execute(select_query, (associated_celebrity,))
    users = cursor.fetchall()

    for user in users:
        user_id = user[0]
        event_prob = user[2]

        #should change or not, Dice rolling!!!
        if random.random() < event_prob:
            new_favorite = random.choice([celeb for celeb in celebrities if celeb!= associated_celebrity])
            update_query = "UPDATE user_dynamic_preferences SET current_favorite = %s WHERE user_id = %s"
            cursor.execute(update_query, (new_favorite, user_id))
            reset_probability_to_default(connection, user_id)
            #print(f"User {user_id} changed favorite from {associated_celebrity} to {new_favorite} due to event {event}")

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
  

def log_event(connection, event_date, event, associated_celebrity):
    cursor = connection.cursor()
    
    # Get the current fan count for the associated celebrity
    fan_counts = get_total_fans(connection)
    fan_count = fan_counts[associated_celebrity]
    
    insert_query = """
    INSERT INTO event_log (event_date, celebrity, event_description, current_fan_count)
    VALUES (%s, %s, %s, %s);
    """
    
    event_desc = event_descriptions[event]
    
    cursor.execute(insert_query, (
        event_date, 
        associated_celebrity,
        event_desc,
        fan_count
    ))
    
    connection.commit()
    print(f"Event {event} logged for {associated_celebrity}.")
    print(f"Current fan count for {associated_celebrity}: {fan_count}")

def run_event_sum(connection, start_date, num_days=180):
    for day in range(num_days):
        current_date = start_date + datetime.timedelta(days=day)
        print(f"Simulating day {day+1}... ({current_date})")

        for celebrity in celebrities:
            event = choose_event(celebrity)
            event_description = event_descriptions.get(event, "Unknown event")
            print(f"Event {event} occurred ({event_description}), associated with {celebrity}")

            if event.startswith('E'):
                if event in category_1_events:
                    situation_category_1_event(conn, event, celebrity)
                elif event in category_2_events:
                    situation_category_2_event(conn, event, celebrity)
                elif event in category_3_events:
                    situation_category_3_event(conn, event, celebrity)
            # unique events
            elif event.startswith(('SC', 'SD', 'T', 'L')):
                situation_category_4_event(conn, event, celebrity)

            log_event(connection, current_date, event, celebrity)

        time.sleep(1)  # Sleep for 1 second after processing all celebrities for a day

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