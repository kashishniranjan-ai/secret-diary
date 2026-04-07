from flask import Flask, render_template, request, redirect, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "secret123"

# folder for images
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

entries = []

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form['username']
    password = request.form['password']

    if username == "admin" and password == "1234":
        session['user'] = username
        return redirect('/dashboard')
    return "Invalid Login"

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template('dashboard.html', entries=entries)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    content = request.form['content']
    mood = request.form['mood']

    image = request.files.get('image')
    filename = ""

    if image and image.filename != "":
        filepath = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(filepath)
        filename = "uploads/" + image.filename

    date = datetime.now().strftime("%d %b %Y")

    entries.append({
        'title': title,
        'content': content,
        'date': date,
        'mood': mood,
        'image': filename
    })

    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)