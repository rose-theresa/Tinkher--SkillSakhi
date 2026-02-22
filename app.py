import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# --- INITIALIZATION ---
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
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- AUTHENTICATION ROUTES ---

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
            cur.execute("INSERT INTO users (name, email, password, teaches, learns, credits) VALUES (%s, %s, %s, %s, %s, 5)", 
                        (name, email, password, teaches, learns))
            mysql.connection.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('login'))
        except:
            flash("Error: Email already exists.", "danger")
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
            session.update({'user_id': user['id'], 'name': user['name']})
            return redirect(url_for('dashboard'))
        flash("Invalid credentials", "danger")
    return render_template('login.html')

# --- DASHBOARD & MATCHING ---

@app.route('/dashboard')
@login_required
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", [session['user_id']])
    user = cur.fetchone()
    
    cur.execute("""
        SELECT m.*, u.name as partner_name FROM matches m 
        JOIN users u ON (m.requester_id = u.id OR m.receiver_id = u.id)
        WHERE (m.requester_id = %s OR m.receiver_id = %s) AND u.id != %s
        AND m.status != 'completed'
        ORDER BY m.created_at DESC
    """, (session['user_id'], session['user_id'], session['user_id']))
    matches = cur.fetchall()

    cur.execute("""
        SELECT sd.*, sch.scheduled_time, u.name as partner_name FROM session_days sd
        JOIN schedules sch ON sd.schedule_id = sch.id
        JOIN matches m ON sch.match_id = m.id
        JOIN users u ON (m.requester_id = u.id OR m.receiver_id = u.id)
        WHERE (m.requester_id = %s OR m.receiver_id = %s) AND u.id != %s
        ORDER BY sd.session_date ASC
    """, (session['user_id'], session['user_id'], session['user_id']))
    session_days = cur.fetchall()
    cur.close()
    return render_template('dashboard.html', user=user, matches=matches, session_days=session_days)

@app.route('/find-matches')
@login_required
def find_matches():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", [session['user_id']])
    me = cur.fetchone()
    
    my_t = [s.strip().lower() for s in me['teaches'].split(',')] if me['teaches'] else []
    my_l = [s.strip().lower() for s in me['learns'].split(',')] if me['learns'] else []
    
    cur.execute("SELECT * FROM users WHERE id != %s", [session['user_id']])
    others = cur.fetchall()
    
    suggestions = []
    for o in others:
        o_t = [s.strip().lower() for s in o['teaches'].split(',')] if o['teaches'] else []
        o_l = [s.strip().lower() for s in o['learns'].split(',')] if o['learns'] else []
        if any(s in o_l for s in my_t) and any(s in my_l for s in o_t):
            suggestions.append(o)
    
    cur.close()
    return render_template('matches.html', suggestions=suggestions)

@app.route('/request-swap/<int:receiver_id>')
@login_required
def request_swap(receiver_id):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO matches (requester_id, receiver_id, status) VALUES (%s, %s, 'pending')",
                (session['user_id'], receiver_id))
    mysql.connection.commit()
    cur.close()
    flash("Swap request sent!", "success")
    return redirect(url_for('dashboard'))

# ADDED: Accept Swap Route
@app.route('/accept-swap/<int:match_id>')
@login_required
def accept_swap(match_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE matches SET status = 'accepted' WHERE id = %s AND receiver_id = %s", 
                (match_id, session['user_id']))
    mysql.connection.commit()
    cur.close()
    flash("Swap request accepted! You are now connected.", "success")
    return redirect(url_for('dashboard'))

# ADDED: Decline Swap Route
@app.route('/decline-swap/<int:match_id>')
@login_required
def decline_swap(match_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM matches WHERE id = %s AND receiver_id = %s", (match_id, session['user_id']))
    mysql.connection.commit()
    cur.close()
    flash("Swap request declined.", "info")
    return redirect(url_for('dashboard'))

@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        cur.execute("UPDATE users SET teaches = %s, learns = %s WHERE id = %s", 
                    (request.form['teaches'], request.form['learns'], session['user_id']))
        mysql.connection.commit()
        cur.close()
        flash("Profile updated!", "success")
        return redirect(url_for('dashboard'))
    
    cur.execute("SELECT teaches, learns FROM users WHERE id = %s", [session['user_id']])
    user_data = cur.fetchone()
    cur.close()
    return render_template('edit_profile.html', user_data=user_data)

# --- INTERACTION & CHAT ---

@app.route('/interaction/<int:match_id>')
@login_required
def interaction_room(match_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT m.*, u1.name as requester_name, u2.name as receiver_name,
               u1.teaches as req_teaches, u2.teaches as rec_teaches
        FROM matches m
        JOIN users u1 ON m.requester_id = u1.id
        JOIN users u2 ON m.receiver_id = u2.id
        WHERE m.id = %s AND (m.requester_id = %s OR m.receiver_id = %s)
    """, (match_id, session['user_id'], session['user_id']))
    match = cur.fetchone()
    
    if not match:
        cur.close()
        flash("Unauthorized access.", "danger")
        return redirect(url_for('dashboard'))

    cur.execute("""
        SELECT msg.*, u.name as sender_name 
        FROM messages msg
        JOIN users u ON msg.sender_id = u.id
        WHERE msg.match_id = %s
        ORDER BY msg.created_at ASC
    """, [match_id])
    chat_history = cur.fetchall()
    
    cur.close()
    return render_template('interaction.html', match=match, chat_history=chat_history)

@app.route('/send-message/<int:match_id>', methods=['POST'])
@login_required
def send_message(match_id):
    message_text = request.form.get('message')
    if message_text:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO messages (match_id, sender_id, message_text) VALUES (%s, %s, %s)",
                    (match_id, session['user_id'], message_text))
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('interaction_room', match_id=match_id))

# --- SESSION MANAGEMENT & CREDITS ---

@app.route('/complete-session/<int:match_id>')
@login_required
def complete_session(match_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM matches WHERE id = %s", [match_id])
    match = cur.fetchone()
    
    if match:
        learner_id = session['user_id']
        teacher_id = match['receiver_id'] if learner_id == match['requester_id'] else match['requester_id']
        
        # Credit Transfer: Teacher +1, Learner -1
        cur.execute("UPDATE users SET credits = credits + 1 WHERE id = %s", [teacher_id])
        cur.execute("UPDATE users SET credits = credits - 1 WHERE id = %s AND credits > 0", [learner_id])
        cur.execute("UPDATE matches SET status = 'completed' WHERE id = %s", [match_id])
        mysql.connection.commit()
        flash("Swap completed! Credits updated.", "success")
        
    cur.close()
    return redirect(url_for('dashboard'))

@app.route('/update-session-day/<int:day_id>', methods=['POST'])
@login_required
def update_session_day(day_id):
    new_date, new_time = request.form.get('new_date'), request.form.get('new_time')
    cur = mysql.connection.cursor()
    cur.execute("UPDATE session_days SET session_date = %s, status = 'scheduled' WHERE id = %s", (new_date, day_id))
    cur.execute("SELECT schedule_id FROM session_days WHERE id = %s", [day_id])
    sch_id = cur.fetchone()['schedule_id']
    cur.execute("UPDATE schedules SET scheduled_time = %s WHERE id = %s", (new_time, sch_id))
    mysql.connection.commit()
    cur.close()
    flash("Session updated!", "success")
    return redirect(url_for('dashboard'))

@app.route('/schedule/<int:match_id>', methods=['GET', 'POST'])
@login_required
def schedule_session(match_id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        date, time, days = request.form['date'], request.form['time'], int(request.form['days'])
        cur.execute("INSERT INTO schedules (match_id, scheduled_date, scheduled_time, duration_days) VALUES (%s, %s, %s, %s)", 
                    (match_id, date, time, days))
        sch_id = cur.lastrowid
        start_dt = datetime.strptime(date, '%Y-%m-%d')
        for i in range(days):
            cur.execute("INSERT INTO session_days (schedule_id, session_date) VALUES (%s, %s)", 
                        (sch_id, (start_dt + timedelta(days=i)).strftime('%Y-%m-%d')))
        mysql.connection.commit()
        return redirect(url_for('dashboard'))
    cur.execute("SELECT name FROM users u JOIN matches m ON (m.requester_id = u.id OR m.receiver_id = u.id) WHERE m.id = %s AND u.id != %s", (match_id, session['user_id']))
    partner = cur.fetchone()
    cur.close()
    return render_template('schedule.html', partner=partner, match_id=match_id)

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)