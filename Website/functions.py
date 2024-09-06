import pandas as pd
from . import UserDynamicPreferences, db

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

