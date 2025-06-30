from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Koneksi ke Database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='db_flask'
)
cursor = conn.cursor(dictionary=True)

# -------------------------------
# INDEX: TAMPILKAN SEMUA DATA
# -------------------------------
@app.route('/')
def index():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template('index.html', users=users)

# -------------------------------
# ADD USER: TAMPILKAN FORM
# -------------------------------
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        return redirect(url_for('index'))
    return render_template('add_user.html')

# -------------------------------
# EDIT USER: TAMPILKAN FORM
# -------------------------------
@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cursor.execute("UPDATE users SET name=%s, email=%s WHERE id=%s", (name, email, id))
        conn.commit()
        return redirect(url_for('index'))
    else:
        cursor.execute("SELECT * FROM users WHERE id=%s", (id,))
        user = cursor.fetchone()
        if user:
            return render_template('edit_user.html', user=user)
        else:
            return 'User not found', 404

# -------------------------------
# DELETE USER: HAPUS DATA
# -------------------------------
@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    cursor.execute("DELETE FROM users WHERE id=%s", (id,))
    conn.commit()
    return redirect(url_for('index'))

# ===============================
# JSON API (Postman)
# ===============================
@app.route('/api/users', methods=['GET'])
def get_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return jsonify(users)

@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    cursor.execute("SELECT * FROM users WHERE id=%s", (id,))
    user = cursor.fetchone()
    return jsonify(user) if user else jsonify({'message': 'User not found'}), 404

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (data['name'], data['email']))
    conn.commit()
    return jsonify({'message': 'User created'}), 201

@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    cursor.execute("UPDATE users SET name=%s, email=%s WHERE id=%s", (data['name'], data['email'], id))
    conn.commit()
    return jsonify({'message': 'User updated'})

@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user_api(id):
    cursor.execute("DELETE FROM users WHERE id=%s", (id,))
    conn.commit()
    return jsonify({'message': 'User deleted'})

if __name__ == "__main__":
    app.run(debug=True)