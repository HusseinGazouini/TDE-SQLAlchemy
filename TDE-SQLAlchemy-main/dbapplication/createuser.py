from app import create_app, db
from models import User

app = create_app()

with app.app_context():
    # Check if the admin user exists
    admin = User.query.filter_by(username='admin').first()

    if admin is None:
        # Create an admin user
        admin = User(username='admin', role='admin')
        admin.set_password('admin')  # Set the password to 'admin'
        db.session.add(admin)
        db.session.commit()
        print("Admin user created!")
    else:
        print("Admin user already exists!")
