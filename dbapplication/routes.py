from flask import render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import Person, User
from flask_login import LoginManager

def register_routes(app, db):

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # Load user for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Home page: List all people
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'GET':
            people = Person.query.all()
            return render_template('index.html', people=people)
        elif request.method == 'POST':
            name = request.form.get('name')
            age = int(request.form.get('age'))
            job = request.form.get('job')

            person = Person(name=name, age=age, job=job)
            db.session.add(person)
            db.session.commit()

            people = Person.query.all()
            return render_template('index.html', people=people)

    # Register new users (for login)
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            hashed_password = generate_password_hash(password)  # Removed method='sha256'
            new_user = User(username=username, password_hash=hashed_password, role='user')  # Default role set to 'user'

            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('register.html')

    # Login existing users
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()

            # Compare hashed password with stored hash
            if user and check_password_hash(user.password_hash, password):  # Changed password to password_hash
                login_user(user)
                return redirect(url_for('index'))
            else:
                return 'Invalid username or password'
        return render_template('login.html')

    # Logout route
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    # Delete a person, only if the user is an admin
    @app.route('/delete/<pid>', methods=['POST'])
    @login_required
    def delete(pid):
        if current_user.role != 'admin':  # Ensure current_user has a 'role' attribute
            return 'You do not have permission to delete.'
        
        person = Person.query.filter_by(pid=pid).first()
        if person:
            db.session.delete(person)
            db.session.commit()
        return redirect(url_for('index'))

    # View details of a person
    @app.route('/details/<pid>')
    def details(pid):
        person = Person.query.filter(Person.pid == pid).first()
        return render_template('detail.html', person=person)
