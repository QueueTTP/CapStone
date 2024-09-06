import random
import sys
from flask import Flask
from dotenv import load_dotenv
import os
import time
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Website.models import UserDefaultSettings, UserDynamicPreferences, db

# Load environment variables from the .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuring the database URI from the .env file
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the app
db.init_app(app)

# Event probabilities and descriptions
event_probabilities = {
    'E1': 0.23, 'E2': 0.07, 'E3': 0.05, 'E4': 0.05, 'E5': 0.06, 'E6': 0.03, 'E7': 0.02,
    'E8': 0.02, 'E9': 0.03, 'E10': 0.03, 'E11': 0.03, 'E12': 0.03, 'E13': 0.04, 'E14': 0.01,
    'E15': 0.03, 'E16': 0.02, 'E17': 0.04, 'E18': 0.01, 'E19': 0.01, 'E20': 0.02, 'E21': 0.02,
    'E22': 0.01, 'E23': 0.01, 'E24': 0.01, 'E25': 0.01, 'E26': 0.01, 'E27': 0.02, 'E28': 0.01,
    'E29': 0.02, 'SC1': 0.001, 'SC2': 0.001, 'SC3': 0.0045, 'SC4': 0.005, 'SC5': 0.001,
    'SD1': 0.0005, 'SD2': 0.005, 'SD3': 0.0025, 'SD4': 0.001, 'SD5': 0.0035, 'T1': 0.0005,
    'T2': 0.005, 'T3': 0.002, 'T4': 0.005, 'L1': 0.0005, 'L2': 0.001, 'L3': 0.0005,
    'L4': 0.0015, 'L5': 0.0015, 'L6': 0.0075
}

event_descriptions = {
    'E1': 'Nothing happen', 'E2': 'Public appearance', 'E3': 'Got Award', 'E4': 'Philanthropy/donation',
    'E5': 'New post on social media (positive)', 'E6': 'New post on social media (negative)',
    'E7': 'Public argument/feud', 'E8': 'Legal issue', 'E9': 'Poor performance',
    'E10': 'Controversial statement', 'E11': 'Attends high profile event', 'E12': 'Cameo appearance',
    'E13': 'New project or franchise', 'E14': 'Gets married/has child', 'E15': 'New social media platform',
    'E16': 'Major news story', 'E17': 'Celebrity collaboration', 'E18': 'Health decline',
    'E19': 'Podcast appearance', 'E20': 'Health fitness', 'E21': 'Talk show appearance',
    'E22': 'Feature film', 'E23': 'Scandalous clothing', 'E24': 'Bizarre fashion choice',
    'E25': 'Mysterious post/teaser', 'E26': 'Book/memoir', 'E27': 'Candid photograph / normal day',
    'E28': 'Request of fans', 'E29': 'Political alignment', 'SC1': 'Releases new album/tour',
    'SC2': 'Hosts SNL', 'SC3': 'Relationship drama', 'SC4': 'Hit Song', 'SC5': 'Launching a fashion line',
    'SD1': 'Carry torch at Olympics', 'SD2': 'Music Performance', 'SD3': 'Offensive comments',
    'SD4': 'Newfound public friendship with Bill Gates', 'SD5': 'Featured in a new song', 'T1': 'Developed new suit',
    'T2': 'Saved the world', 'T3': 'Become a villain', 'T4': 'Public appearance with iron man suit',
    'L1': 'Losses in NBA playoffs', 'L2': 'Son gets drafted onto same team', 'L3': 'Wins Olympic Gold Medal',
    'L4': 'Releases new shoe/product', 'L5': 'Gets Injured', 'L6': 'Sits out for rest'
}

category_1_events = {'E2', 'E3', 'E4', 'E5', 'E11', 'E12', 'E13', 'E14', 'E15', 'E16', 'E17', 'E18', 'E19', 'E20', 'E21', 'E22', 'E25', 'E26'}
category_2_events = {'E1', 'E10', 'E16', 'E24', 'E27', 'E28'}
category_3_events = {'E6', 'E7', 'E8', 'E9', 'E23', 'E29'}
category_4_events = {'SC1', 'SC2', 'SC3', 'SC4', 'SC5', 'SD1', 'SD2', 'SD3', 'SD4', 'SD5', 'T1', 'T2', 'T3', 'T4', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6'}

celebrities = ['Sabrina Carpenter', 'Snoop Dogg', 'Tony Stark', 'LeBron James']

# Utility functions
def choose_event():
    """Randomly select an event based on predefined probabilities."""
    events = list(event_probabilities.keys())
    probabilities = list(event_probabilities.values())
    event = random.choices(events, probabilities)[0]
    return event

def reset_probability_to_default(user_id):
    """Reset user probabilities in `user_dynamic_preferences` to the defaults."""
    user_default = UserDefaultSettings.query.get(user_id)
    
    if user_default:
        user_dynamic = UserDynamicPreferences.query.get(user_id)
        if user_dynamic:
            for field in event_probabilities.keys():
                setattr(user_dynamic, field, getattr(user_default, field))
            db.session.commit()
            print(f"User {user_id}'s probabilities reset to default.")
        else:
            print(f"No dynamic preferences found for user {user_id}.")
    else:
        print(f"No default settings found for user {user_id}.")

# Situation Functions
def situation_category_1_event(event, associated_celebrity):
    users = UserDynamicPreferences.query.all()

    for user in users:
        event_prob = getattr(user, event)

        if random.random() < event_prob:
            new_favorite = random.choice(celebrities)
            user.current_favorite = new_favorite
            reset_probability_to_default(user.user_id)
            print(f"User {user.user_id} changed favorite to {associated_celebrity} due to event {event_descriptions[event]}")

    db.session.commit()

def situation_category_2_event(event, associated_celebrity):
    users = UserDynamicPreferences.query.filter_by(current_favorite=associated_celebrity).all()

    for user in users:
        event_prob = getattr(user, event)

        if random.random() < event_prob:
            new_favorite = random.choice([celeb for celeb in celebrities if celeb != associated_celebrity])
            user.current_favorite = new_favorite
            reset_probability_to_default(user.user_id)
            print(f"User {user.user_id} changed favorite from {associated_celebrity} to {new_favorite} due to event {event_descriptions[event]}")

    db.session.commit()

def situation_category_3_event(event, associated_celebrity):
    users = UserDynamicPreferences.query.filter_by(current_favorite=associated_celebrity).all()

    for user in users:
        event_prob = getattr(user, event)

        if random.random() < event_prob:
            new_favorite = random.choice([celeb for celeb in celebrities if celeb != associated_celebrity])
            user.current_favorite = new_favorite
            reset_probability_to_default(user.user_id)
            print(f"User {user.user_id} changed favorite from {associated_celebrity} to {new_favorite} due to event {event}")
        else:
            new_prob = min(event_prob + 0.15, 1.0)
            setattr(user, event, new_prob)
            print(f"User {user.user_id}'s probability for event {event_descriptions[event]} increased to {new_prob}")

    db.session.commit()

# Main Simulation Function
def run_event_sum(num_days=180):
    for day in range(num_days):
        print(f"Simulating day {day+1}...")

        event = choose_event()
        event_description = event_descriptions.get(event, "Unknown event")
        associated_celebrity = random.choice(celebrities)
        print(f"Event {event} occurred ({event_description}), associated with {associated_celebrity}")

        if event in category_1_events:
            situation_category_1_event(event, associated_celebrity)
        elif event in category_2_events:
            situation_category_2_event(event, associated_celebrity)
        elif event in category_3_events:
            situation_category_3_event(event, associated_celebrity)

        time.sleep(10)  # Simulate a delay between events

# Running the Simulation
if __name__ == "__main__":
    with app.app_context():
        run_event_sum(num_days=180)
