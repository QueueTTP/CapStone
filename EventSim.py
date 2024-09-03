import time
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

conn = create_connection()

event_probabilities={
        'E1' :0.23,
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
#make sure the sum of the probability it's 1
print(sum(event_probabilities.values()))

category_1_events = {'E2', 'E3', 'E4', 'E5', 'E11', 'E12', 'E13', 'E14','E15', 'E16', 'E17', 'E18', 'E19', 'E20', 'E21', 'E22', 'E25', 'E26' }
category_2_events = {'E1', 'E10', 'E16', 'E24', 'E27', 'E28'}
category_3_events = {'E6', 'E7', 'E8', 'E9', 'E23', 'E29'}

celebrities = ['Sabrina Carpenter', 'Snoop Dogg', 'Tony Stark', 'LeBron James']

def choose_event():
    events=list(event_probabilities.keys())
    probabilities = list(event_probabilities.values())
    event = random.choices(events,probabilities)[0]
    return event

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
            print(f"User {user_id} changed favorite to {associated_celebrity} due to event {event}")

    connection.commit()


def situation_category_2_event(connection, event, associated_celebrity):


def situation_category_3_event(connection, event, associated_celebrity):



def run_event_sum(connection, num_days = (6*30)):



if __name__ == "__main__":
    conn = create_connection()
