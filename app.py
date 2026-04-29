from flask import Flask, request, jsonify, render_template, redirect, url_for, session, Response
import dbfunc
import pltit
import mood_rec
import cv2
from deepface import DeepFace
import sqlite3
from datetime import datetime
import base64
from datetime import datetime, timedelta


app = Flask(__name__)
app.secret_key = 'my_key'

# Database setup
DATABASE = 'HoneyPie0.db' 

dbfunc.init_db(app)

#main-login page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    data = request.get_json()  
    email = data.get('email')
    password = data.get('password')
    # email = request.form.get('email')
    # password = request.form.get('password')
    print(request.data)  # Raw body
    print(request.get_json())  # Parsed JSON

    print(f"Login attempt - Email: {email}, Password: {password}")

    user= dbfunc.get_user_bymail(email)
    print(f"User from DB: {user}")

    if user:  # Ideally, use hashed password checking
        stored_pass= user['password']
        print(f"Stored password: {stored_pass}")
        if password== stored_pass:
            print("Password correct")
            session['user_id'] = user['id']
            session['username'] = user['username']
            return jsonify({'success': True, 'username': user['username']})
        else:
            return jsonify({'message': 'Invalid email or password.'}), 401
    else:
        return jsonify({'message': 'User not registered.'}), 404

#sign up page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match!")
        try:
            cursor, conn = dbfunc.get_db_connection()
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                conn.close()
                return render_template('register.html', error="Email already registered.")

            cursor.execute('''
                INSERT INTO users (username, email, password) VALUES (?, ?, ?)
                ''', (username, email, password))
            conn.commit()
            conn.close()
            return render_template('register.html', success="Registration successful! Please login.")

        except sqlite3.IntegrityError as e:
            # Fallback just in case duplicate still happens (extra safety)
            return render_template('register.html', error="This email or username is already in use.")
        except Exception as e:
            return render_template('register.html', error=f"Unexpected error: {str(e)}")
    dbfunc.print_all_users()
    return render_template('register.html')

# mood rec funcs
def generate_frames(username):
    vdo_cap = cv2.VideoCapture(0)  # Open the webcam
    try:
        while True:
            ret, vdo = vdo_cap.read()
            print("Frame shape:", vdo.shape)
            if not ret:
                print("No frame")
                break
            
            # Detect mood and overlay text
            emo1, emo2 = mood_rec.detect_mood(username, vdo)
            print(f"Detected mood: {emo1}, {emo2}")
            # if emo1 and emo2:
            #     cv2.putText(vdo, f'{emo1} and {emo2}', (50, 50),
            #                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            _, buffer = cv2.imencode('.jpg', vdo)  # Convert frame to image format
            frame = buffer.tobytes()  # Convert to bytes for streaming
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Stream as MJPEG
    finally:
        vdo_cap.release()  # Release webcam resource

@app.route('/video_feed')
def video_feed():
    print("vdo feed requested")
    username= session.get('username', 'Guest')
    return Response(generate_frames(username), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/dashboard')
def mood_recognition():
    print("Session content:", session)
    username = session.get('username')
    if not username:
        return redirect(url_for('index'))  # Fallback if not logged in

    return render_template('dashboard.html', username=username)
# mood rec funcs end

#yearly emotions
@app.route('/yearly_emotions/<username>')
def yearly_emotions(username):
    chart_html = pltit.monthly_emotions(username)
    return render_template('moodhistory.html', chart_html=chart_html, username=username)

#daily emotions
@app.route('/weekly_emotions/<username>', methods=['GET', 'POST'])
def weekly_emotions(username):
    today = datetime.today().date()
    selected_date = today

    if request.method == 'POST':
        date_str = request.form.get('selected_date') or today.isoformat()
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()

        if 'prev' in request.form:
            selected_date -= timedelta(weeks=1)
        elif 'next' in request.form:
            selected_date += timedelta(weeks=1)

    chart_html = pltit.daily_emotions(username, selected_date)
    return render_template('emotion.html', chart_html=chart_html, selected_date=selected_date.isoformat(), username=username)



#logout 
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/index.html')
def index_alias():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)
    for rule in app.url_map.iter_rules():
        print(rule.endpoint)
