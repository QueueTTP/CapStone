import eventlet

eventlet.monkey_patch()

import os
import logging
from Website import create_app, db, socketio



# Create and configure the app
app = create_app()

# Set up logging
logging.basicConfig(level=logging.INFO)


with app.app_context():
        db.create_all()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, debug=True, host='0.0.0.0', port=port, use_reloader=False)
