# main.py

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Sukuriamas SQLite duomenų bazės prisijungimas
conn = sqlite3.connect('tasks.db', check_same_thread=False)
c = conn.cursor()

# Sukuriamas užduočių lentelė
c.execute('''CREATE TABLE IF NOT EXISTS tasks
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT,
              description TEXT,
              status TEXT,
              user TEXT)''')
conn.commit()

@app.route('/')
def index():
    # Gauname visas užduotis iš duomenų bazės
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        user = request.form['user']
        c.execute("INSERT INTO tasks (title, description, status, user) VALUES (?, ?, ?, ?)", (title, description, status, user))
        conn.commit()
        return redirect(url_for('index'))

@app.route('/edit_task/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    if request.method == 'GET':
        c.execute("SELECT * FROM tasks WHERE id=?", (id,))
        task = c.fetchone()
        return render_template('edit_task.html', task=task)
    elif request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        user = request.form['user']
        c.execute("UPDATE tasks SET title=?, description=?, status=?, user=? WHERE id=?", (title, description, status, user, id))
        conn.commit()
        return redirect(url_for('index'))

@app.route('/delete_task/<int:id>')
def delete_task(id):
    c.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    return redirect(url_for('index'))

@app.route('/tasks')
def all_tasks():
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    return render_template('all_tasks.html', tasks=tasks)


if __name__ == '__main__':
    app.run(debug=True)
