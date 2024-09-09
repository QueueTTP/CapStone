import pandas as pd
from .models import UserDynamicPreferences, EventLog 
from . import db

def reset_session():
    db.session.remove()
    
def get_fan_counts():
    reset_session()  # Reset the session to avoid stale data
    
    # Perform the query to get fan counts grouped by current_favorite
    query = db.session.query(
        UserDynamicPreferences.current_favorite,
        db.func.count(UserDynamicPreferences.current_favorite).label('fan_count')
    ).group_by(UserDynamicPreferences.current_favorite)
    
    result = query.all()

    # Convert query result to Pandas DataFrame
    df = pd.DataFrame(result, columns=['current_favorite', 'fan_count'])

    # Debugging: print the result of the query
    print("Query Result:")
    print(df)

    return df


def get_events_log():
    reset_session()  # Reset the session to avoid stale data

    # Fetch data from the 'event_log' table
    query = db.session.query(
        EventLog.event_date,
        EventLog.celebrity,
        EventLog.event_description,
        EventLog.current_fan_count
    ).order_by(EventLog.event_date.desc()).limit(10)

    result = query.all()

    # Convert query result to Pandas DataFrame
    df = pd.DataFrame(result, columns=['event_date', 'celebrity', 'event_description', 'current_fan_count'])
    
    # Convert dates to strings to avoid JSON serialization issues
    df['event_date'] = df['event_date'].apply(lambda x: x.strftime('%Y-%m-%d'))

    # Calculate fan_count_change (difference in fan count over time)
    df['fan_count_change'] = df['current_fan_count'].diff().fillna(0).astype(int)

    # Debugging: print the result of the query
    print("Event Log with Fan Count Changes:")
    print(df)

    return df
