from app import create_app, db

app = create_app()

if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()
        app.run(debug=True)
    except Exception as e:
        print(f"Error starting app: {str(e)}") 