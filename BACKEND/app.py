from flask import Flask, jsonify, request
import psycopg2
from psycopg2 import pool
import os
import time
import uuid

app = Flask(__name__)

db_host = os.getenv("DB_HOST", "db")

# Database connection pool with retry logic
db_pool = None
for attempt in range(5):
    try:
        db_pool = psycopg2.pool.SimpleConnectionPool(
            1, 20,
            host=db_host,
            port="5432",
            database="mydb",
            user="user",
            password="pass"
        )
        print("✅ Connected to database.")
        break
    except Exception as e:
        print(f"⏳ Attempt {attempt + 1}: Failed to connect to database: {e}")
        time.sleep(3)

if not db_pool:
    print("❌ All retries failed. Database connection unavailable.")
    exit(1)

# Initialize todos table
try:
    conn = db_pool.getconn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id UUID PRIMARY KEY,
            text TEXT NOT NULL,
            completed BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()
    cur.close()
    db_pool.putconn(conn)
except Exception as e:
    print(f"❌ Failed to create todos table: {e}")
    exit(1)

# Root route for testing
@app.route('/')
def index():
    print("📡 Received request to /")
    return jsonify({'message': 'Todo API is running. Use /api/todos or /todos for endpoints.'})

# Get all todos
@app.route('/api/todos', methods=['GET'])
@app.route('/todos', methods=['GET'])
def get_todos():
    print("📡 Received GET /api/todos or /todos")
    try:
        conn = db_pool.getconn()
        cur = conn.cursor()
        cur.execute("SELECT id, text, completed FROM todos")
        todos = [{'_id': str(row[0]), 'text': row[1], 'completed': row[2]} for row in cur.fetchall()]
        cur.close()
        db_pool.putconn(conn)
        return jsonify(todos)
    except Exception as e:
        print(f"❌ Error in get_todos: {e}")
        return jsonify({'error': f'Server error: {e}'}), 500

# Create a todo
@app.route('/api/todos', methods=['POST'])
@app.route('/todos', methods=['POST'])
def create_todo():
    print("📡 Received POST /api/todos or /todos")
    try:
        data = request.get_json()
        if not data or not data.get('text'):
            print("❌ Bad request: text is required")
            return jsonify({'error': 'Bad request: text is required'}), 400
        todo_id = str(uuid.uuid4())
        conn = db_pool.getconn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO todos (id, text, completed) VALUES (%s, %s, %s) RETURNING id, text, completed",
            (todo_id, data['text'], False)
        )
        todo = cur.fetchone()
        conn.commit()
        cur.close()
        db_pool.putconn(conn)
        print(f"✅ Created todo: {todo}")
        return jsonify({'_id': str(todo[0]), 'text': todo[1], 'completed': todo[2]}), 201
    except Exception as e:
        print(f"❌ Error in create_todo: {e}")
        return jsonify({'error': f'Bad request: {e}'}), 400

# Update a todo
@app.route('/api/todos/<id>', methods=['PATCH'])
@app.route('/todos/<id>', methods=['PATCH'])
def update_todo(id):
    print(f"📡 Received PATCH /api/todos/{id} or /todos/{id}")
    try:
        data = request.get_json()
        if 'completed' not in data:
            print("❌ Bad request: completed field is required")
            return jsonify({'error': 'Bad request: completed field is required'}), 400
        conn = db_pool.getconn()
        cur = conn.cursor()
        cur.execute(
            "UPDATE todos SET completed = %s WHERE id = %s RETURNING id, text, completed",
            (data['completed'], id)
        )
        todo = cur.fetchone()
        conn.commit()
        cur.close()
        db_pool.putconn(conn)
        if not todo:
            print("❌ Todo not found")
            return jsonify({'error': 'Todo not found'}), 404
        print(f"✅ Updated todo: {todo}")
        return jsonify({'_id': str(todo[0]), 'text': todo[1], 'completed': todo[2]})
    except Exception as e:
        print(f"❌ Error in update_todo: {e}")
        return jsonify({'error': f'Bad request: {e}'}), 400

# Delete a todo
@app.route('/api/todos/<id>', methods=['DELETE'])
@app.route('/todos/<id>', methods=['DELETE'])
def delete_todo(id):
    print(f"📡 Received DELETE /api/todos/{id} or /todos/{id}")
    try:
        conn = db_pool.getconn()
        cur = conn.cursor()
        cur.execute("DELETE FROM todos WHERE id = %s RETURNING id", (id,))
        todo = cur.fetchone()
        conn.commit()
        cur.close()
        db_pool.putconn(conn)
        if not todo:
            print("❌ Todo not found")
            return jsonify({'error': 'Todo not found'}), 404
        print("✅ Todo deleted")
        return jsonify({'message': 'Todo deleted'})
    except Exception as e:
        print(f"❌ Error in delete_todo: {e}")
        return jsonify({'error': f'Bad request: {e}'}), 400

if __name__ == '__main__':
    print("🚀 Starting Flask app on port 9000")
    app.run(host='0.0.0.0', port=9000)