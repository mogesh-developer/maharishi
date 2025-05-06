from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this!
app.config['MONGO_URI'] = 'mongodb://localhost:27017/flask_auth_db'

mongo = PyMongo(app)
users = mongo.db.users


@app.route('/')
def home():
    if 'username' in session:
        return f"Welcome, {session['username']}! <a href='/logout'>Logout</a>"
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if users.find_one({'username': username}):
            flash('Username already exists!')
            return redirect(url_for('register'))

        hashed_pw = generate_password_hash(password)
        users.insert_one({'username': username, 'password': hashed_pw})
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('dashboard'))

        else:
            flash('Invalid credentials.')
            return redirect(url_for('index.html'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    flash('You must be logged in to view the dashboard.')
    return redirect(url_for('login'))

@app.route('/dhm.html')
def dhm():
    return render_template('dhm.html')

@app.route('/dgda')
def dgda_course():
    return render_template('dgda.html')

@app.route('/dxrt')
def dxrt_course():
    return render_template('dxrt.html')

@app.route('/dmlta')
def dmlta_course():
    return render_template('dmlta.html')

@app.route('/dna')
def dna():
    return render_template('dna.html')

@app.route('/dhmct')
def dhmct():
    return render_template('dhmct.html')

@app.route('/dpsm')
def dpsm():
    return render_template('dpsm.html')

@app.route('/dct')
def dct():
    return render_template('dct.html')

@app.route('/difp')
def difp():
    return render_template('difp.html')






@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully.')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
