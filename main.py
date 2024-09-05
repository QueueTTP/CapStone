import eventlet

eventlet.monkey_patch()


from Website import create_app, db, socketio



app = create_app()

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, use_reloader=False)
