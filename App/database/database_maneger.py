import sqlite3
import os


DATABASE_PATH = "database/recruiter.db"


def get_connection():
    """
    Create SQLite connection
    """
    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DATABASE_PATH)

    return conn



def create_tables():

    conn = get_connection()

    cursor = conn.cursor()


    # Candidate storage table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        email TEXT,

        phone TEXT,

        skills TEXT,

        experience TEXT,

        education TEXT,

        resume_text TEXT,

        batch_id INTEGER,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    # Batch tracking table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS document_batches(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        batch_number INTEGER UNIQUE,

        start_candidate INTEGER,

        end_candidate INTEGER,

        document_name TEXT,

        status TEXT DEFAULT 'pending',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


    conn.commit()

    conn.close()


    print("Database tables created successfully")



if __name__ == "__main__":

    create_tables()