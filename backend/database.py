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
    """)
    conn.commit()
    conn.close()

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
        SELECT DISTINCT chat_history_id FROM messages
        UNION
        SELECT DISTINCT chat_history_id FROM pdf_uploads
        ORDER BY chat_history_id DESC
    """)
    ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    return ids

def delete_session(chat_history_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM messages WHERE chat_history_id = ?', (chat_history_id,))
    conn.execute('DELETE FROM pdf_uploads WHERE chat_history_id = ?', (chat_history_id,))
    conn.commit()
    conn.close()