import sqlite3

def get_db_connection():
    conn = sqlite3.connect('pdf_chat_sessions.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS messages (
        message_id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_history_id TEXT NOT NULL,
        sender_type TEXT NOT NULL,
        message_type TEXT NOT NULL,
        text_content TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS pdf_uploads (
        pdf_id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_history_id TEXT NOT NULL,
        pdf_name TEXT NOT NULL,
        upload_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS session_names (
        chat_history_id TEXT PRIMARY KEY,
        display_name TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );                     
    """)
    conn.commit()
    conn.close()

def save_session_name(chat_history_id, display_name):
    conn = get_db_connection()
    conn.execute(
        'INSERT OR REPLACE INTO session_names (chat_history_id, display_name) VALUES (?, ?)',
        (chat_history_id, display_name)
    )
    conn.commit()
    conn.close()   

def get_session_name(chat_history_id):
    conn = get_db_connection()
    result = conn.execute(
        'SELECT display_name FROM session_names WHERE chat_history_id = ?',
        (chat_history_id,)
    ).fetchone()
    conn.close()
    return result['display_name'] if result else None     

def save_message(chat_history_id, sender_type, message_type, text_content):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO messages (chat_history_id, sender_type, message_type, text_content) VALUES (?, ?, ?, ?)',
        (chat_history_id, sender_type, message_type, text_content)
    )
    conn.commit()
    conn.close()

def save_pdf_upload(chat_history_id, pdf_name):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO pdf_uploads (chat_history_id, pdf_name) VALUES (?, ?)',
        (chat_history_id, pdf_name)
    )
    conn.commit()
    conn.close()

def get_messages(chat_history_id):
    conn = get_db_connection()
    messages = conn.execute(
        'SELECT sender_type, text_content FROM messages WHERE chat_history_id = ? ORDER BY message_id ASC',
        (chat_history_id,)
    ).fetchall()
    conn.close()
    return [{'sender': m['sender_type'], 'content': m['text_content']} for m in messages]

def get_pdf_uploads(chat_history_id):
    conn = get_db_connection()
    pdfs = conn.execute(
        'SELECT pdf_name FROM pdf_uploads WHERE chat_history_id = ? ORDER BY upload_timestamp ASC',
        (chat_history_id,)
    ).fetchall()
    conn.close()
    return [pdf['pdf_name'] for pdf in pdfs]

def get_all_chat_history_ids():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT m.chat_history_id, COALESCE(sn.display_name, m.chat_history_id) as display_name
        FROM (
            SELECT DISTINCT chat_history_id FROM messages
            UNION
            SELECT DISTINCT chat_history_id FROM pdf_uploads
        ) m
        LEFT JOIN session_names sn ON m.chat_history_id = sn.chat_history_id
        ORDER BY m.chat_history_id DESC
    """)
    results = cursor.fetchall()
    conn.close()
    return [{'id': row[0], 'name': row[1]} for row in results]

def delete_session(chat_history_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM messages WHERE chat_history_id = ?', (chat_history_id,))
    conn.execute('DELETE FROM pdf_uploads WHERE chat_history_id = ?', (chat_history_id,))
    conn.execute('DELETE FROM session_names WHERE chat_history_id = ?', (chat_history_id,))
    conn.commit()
    conn.close()