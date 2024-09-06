<<<<<<< HEAD
<<<<<<< HEAD
import pandas as pd
from .models import UserDynamicPreferences
from . import db

def reset_session():
    db.session.remove()
    
=======
from nbconvert import HTMLExporter
import nbformat
=======
>>>>>>> 30fa1389 (updated docker file)
import pandas as pd
from . import UserDynamicPreferences, db

def reset_session():
    db.session.remove()
<<<<<<< HEAD
    db.session.configure(bind=db.engine)  # Rebind the engine if necessary

>>>>>>> d1a44570 (live updating chart on markets.html)
=======
    
>>>>>>> 30fa1389 (updated docker file)
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

