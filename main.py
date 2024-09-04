from Website import create_app, db

app = create_app()

with app.app_context():
    db.create_all()
    print("UserDefaultSettings table created successfully")


if __name__ == "__main__":
    app.run(debug=True)