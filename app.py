import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'sakhi_secret_key_123'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Rose2005@'
app.config['MYSQL_DB'] = 'skillsakhi'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# --- LOGIN PROTECTION ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in first", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        teaches = request.form['teaches']
        learns = request.form['learns']
        
        cur = mysql.connection.cursor()
        try:
            cur.execute("""INSERT INTO users (name, email, password, teaches, learns, is_verified) 
                           VALUES (%s, %s, %s, %s, %s, %s)""", 
                        (name, email, password, teaches, learns, True))
            mysql.connection.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Error during registration: {e}")
            flash("Email already exists or Database Error", "danger")
        finally:
            cur.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        candidate_pw = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", [email])
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user['password'], candidate_pw):
            session['user_id'] = user['id']
            session['name'] = user['name']
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials", "danger")
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", [session['user_id']])
    user = cur.fetchone()
    
    cur.execute("""
        SELECT m.*, u.name as partner_name 
        FROM matches m 
        JOIN users u ON (m.requester_id = u.id OR m.receiver_id = u.id)
        WHERE (m.requester_id = %s OR m.receiver_id = %s) AND u.id != %s
    """, (session['user_id'], session['user_id'], session['user_id']))
    my_matches = cur.fetchall()
    cur.close()
    return render_template('dashboard.html', user=user, matches=my_matches)

@app.route('/find-matches')
@login_required
def find_matches():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", [session['user_id']])
    me = cur.fetchone()
    
    # Matching Logic: Convert comma strings to lowercase lists
    my_teaches = [s.strip().lower() for s in me['teaches'].split(',')] if me['teaches'] else []
    my_learns = [s.strip().lower() for s in me['learns'].split(',')] if me['learns'] else []
    
    cur.execute("SELECT * FROM users WHERE id != %s", [session['user_id']])
    others = cur.fetchall()
    
    suggestions = []
    for other in others:
        other_teaches = [s.strip().lower() for s in other['teaches'].split(',')] if other['teaches'] else []
        other_learns = [s.strip().lower() for s in other['learns'].split(',')] if other['learns'] else []
        
        # Intersection logic: Do we have a mutual interest?
        match_found = any(skill in other_learns for skill in my_teaches) and \
                      any(skill in my_learns for skill in other_teaches)
        
        if match_found:
            suggestions.append(other)
            
    cur.close()
    return render_template('matches.html', suggestions=suggestions)

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

@app.route('/request-swap/<int:receiver_id>')
@login_required
def request_swap(receiver_id):
    cur = mysql.connection.cursor()
    
    # 1. Check if the requester has at least 1 credit
    cur.execute("SELECT credits FROM users WHERE id = %s", [session['user_id']])
    user_data = cur.fetchone()
    
    if user_data['credits'] < 1:
        flash("You need at least 1 credit to request a swap! Teach a skill to earn more.", "danger")
        return redirect(url_for('find_matches'))

    # 2. Check if a request already exists to prevent duplicates
    cur.execute("""SELECT * FROM matches 
                   WHERE requester_id = %s AND receiver_id = %s AND status = 'pending'""", 
                (session['user_id'], receiver_id))
    if cur.fetchone():
        flash("You already have a pending request with this user.", "warning")
        return redirect(url_for('find_matches'))

    # 3. Create the match request
    try:
        cur.execute("INSERT INTO matches (requester_id, receiver_id, status) VALUES (%s, %s, 'pending')", 
                    (session['user_id'], receiver_id))
        mysql.connection.commit()
        flash("Swap request sent successfully! Wait for their confirmation.", "success")
    except Exception as e:
        print(f"Error creating match: {e}")
        flash("Something went wrong while sending the request.", "danger")
    finally:
        cur.close()
        
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)