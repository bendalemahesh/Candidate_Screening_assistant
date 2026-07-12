
import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_FOLDER = BASE_DIR

os.makedirs(DB_FOLDER, exist_ok=True)

DB_PATH = os.path.join(DB_FOLDER, "recruiter_ai.db")
print("DATABASE PATH:", DB_PATH)


conn = sqlite3.connect(DB_PATH)

print("Database created at:", DB_PATH)

cursor = conn.cursor()


# Your schema code below this line


conn.commit()
conn.close()




conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()


# Add resume_text column

try:
    cursor.execute(
        """
        ALTER TABLE candidates
        ADD COLUMN resume_text TEXT
        """
    )

    print("resume_text added")

except sqlite3.OperationalError:
    print("resume_text already exists")



# Add batch_id column

try:
    cursor.execute(
        """
        ALTER TABLE candidates
        ADD COLUMN batch_id INTEGER
        """
    )

    print("batch_id added")

except sqlite3.OperationalError:
    print("batch_id already exists")



conn.commit()

conn.close()


print("Schema update completed")