import time
from flask import Blueprint, current_app, render_template
from . import socketio
from .functions import get_fan_counts, fetch_and_calculate_changes
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
            
            # Fetch event log changes
            event_log_changes = fetch_and_calculate_changes().to_dict(orient='records')

            # Emit event log data to all connected clients
            socketio.emit('updateEventLog', event_log_changes)


            # Sleep for 5 seconds before the next update
            time.sleep(5)  # Emit data every 5 seconds
