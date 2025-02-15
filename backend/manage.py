from flask.cli import FlaskGroup
from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models.user import User
from app.models.trip import Trip

app = create_app()
migrate = Migrate(app, db)
cli = FlaskGroup(app)

@cli.command("migrate_db")
def migrate_db():
    """Run database migrations automatically"""
    with app.app_context():
        try:
            # Generate migration
            from flask_migrate import stamp
            stamp()
            
            # Create new migration
            from flask_migrate import revision
            revision(autogenerate=True)
            
            # Apply migration
            upgrade()
            
            print("Database migration completed successfully!")
        except Exception as e:
            print(f"Error during migration: {str(e)}")

if __name__ == "__main__":
    cli() 