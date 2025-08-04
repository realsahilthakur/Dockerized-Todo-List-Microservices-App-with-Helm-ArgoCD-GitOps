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
max_attempts = 10
retry_delay = 5  # seconds
for attempt in range(max_attempts):
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
        print(f"⏳ Attempt {attempt + 1}/{max_attempts}: Failed to connect to database: {e}")
        if attempt < max_attempts - 1:
            time.sleep(retry_delay)
        else:
            print("⚠️ Warning: Database connection unavailable. API will run but may fail on database operations.")

# Initialize todos table if connection is established
if db_pool:
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
else:
    print("⚠️ Skipping table creation due to database connection failure.")

# Root route for testing
@app.route('/')
def index():
    print("📡 Received request to /")
    return jsonify({'message': 'Todo API is running. Use /api/todos or /todos for endpoints.'})

# Modified get_todos to handle missing db_pool
@app.route('/api/todos', methods=['GET'])
@app.route('/todos', methods=['GET'])
def get_todos():
    print("📡 Received GET /api/todos or /todos")
    if not db_pool:
        print("❌ Database connection unavailable")
        return jsonify({'error': 'Database unavailable'}), 503
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

# ... (other routes similarly updated to check db_pool before operations)
# Example for create_todo
@app.route('/api/todos', methods=['POST'])
@app.route('/todos', methods=['POST'])
def create_todo():
    print("📡 Received POST /api/todos or /todos")
    if not db_pool:
        print("❌ Database connection unavailable")
        return jsonify({'error': 'Database unavailable'}), 503
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

# ... (update_todo and delete_todo similarly updated)

if __name__ == '__main__':
    print("🚀 Starting Flask app on port 9000")
    app.run(host='0.0.0.0', port=9000, debug=True)