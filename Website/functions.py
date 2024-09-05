from nbconvert import HTMLExporter
import nbformat
import pandas as pd
from .models import UserDynamicPreferences, db

def get_fan_counts():
    # Perform the query to get fan counts grouped by current_favorite
    query = db.session.query(
        UserDynamicPreferences.current_favorite,
        db.func.count(UserDynamicPreferences.current_favorite).label('fan_count')
    ).group_by(UserDynamicPreferences.current_favorite)
    
    # Convert query result to Pandas DataFrame
    result = query.all()
    df = pd.DataFrame(result, columns=['current_favorite', 'fan_count'])
    return df

def reset_session():
    db.session.remove()
    db.session.configure(bind=db.engine)  # Rebind the engine if necessary

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

