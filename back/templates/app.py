from flask import Flask, render_template, request, redirect, url_for
import json
import os

# יצירת אפליקציית Flask
app = Flask(__name__)
# נתיב לקובץ המשתמשים (JSON)
users_file = 'users.json'

# פונקציה לטעינת משתמשים מקובץ JSON
def load_users():
    if not os.path.exists(users_file):
        return {}
    with open(users_file, 'r') as file:
        return json.load(file)

# פונקציה לשמירת משתמש חדש
def save_user(username, password):
    users = load_users()
    users[username] = password
    with open(users_file, 'w') as file:
        json.dump(users, file, indent=4)

# נתיב הבית - מפנה לדף התחברות
@app.route('/')
def home():
    return redirect(url_for('login'))

# נתיב התחברות
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if users.get(username) == password:
            return redirect(url_for('success'))
        else:
            return redirect(url_for('login', error="Invalid credentials"))
    return render_template('login.html')

# נתיב הרשמה
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['new_username']
        password = request.form['new_password']
        save_user(username, password)
        return redirect(url_for('login'))
    return render_template('signup.html')

# נתיב הצלחה
@app.route('/success')
def success():
    return render_template('success.html')

# נקודת כניסה לאפליקציה
if __name__ == '__main__':
    app.run(debug=True)
