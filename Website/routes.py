import time
from flask import Blueprint, current_app, render_template
from . import socketio, db
from .functions import get_fan_counts, get_events_log
from .models import EventLog
import eventlet

# Ensure eventlet is monkey patched for concurrency
eventlet.monkey_patch()

routes = Blueprint('routes', __name__)

@routes.route('/about-us')
def about_us():
    return render_template('about-us.html')

@routes.route('/markets')
def markets():
    return render_template('markets.html')

# Start the background task when a client connects
@socketio.on('connect')
def start_background_task():
    """Start the background task when a client connects."""
    app = current_app._get_current_object()  # Get the real app instance
    socketio.start_background_task(background_fan_count_task, app)
    socketio.start_background_task(background_event_log_task, app)



def background_fan_count_task(app):
    """Background task to emit fan counts every 5 seconds."""
    with app.app_context():  # Ensure the task runs inside the app context
        while True:

            # Fetch fan counts from the database
            fan_counts = get_fan_counts().to_dict(orient='records')

            # Filter out negative values if any
            fan_counts = [f for f in fan_counts if f['fan_count'] >= 0]

            # Emit data to all connected clients
            socketio.emit('updateFanCounts', fan_counts)
            
            # Print fan counts for debugging
            print("Fan Counts Emitted to Clients:")
            print(fan_counts)


            # Sleep for 5 seconds before the next update
            time.sleep(5)  # Emit data every 5 seconds
            
def background_event_log_task(app):
    """Background task to emit event log updates every 5 seconds."""
    with app.app_context():
        while True:
            
            # Fetch event log data from the database
            event_log = get_events_log().to_dict(orient='records')

            # Emit data to all connected clients
            socketio.emit('updateEventLog', event_log)
            
            # Print event log for debugging
            print("Event Log Emitted to Clients:")
            print(event_log)

            # Sleep for 5 seconds before the next update
            time.sleep(5)


