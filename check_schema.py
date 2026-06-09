
import db
import sys
import os

sys.path.append(os.getcwd())

def check_schema():
    try:
        conn = db.connection()
        cur = conn.cursor()
        cur.execute("DESCRIBE chat_messages")
        columns = cur.fetchall()
        
        with open("schema_info.txt", "w") as f:
            f.write(f"{'Field':<20} {'Type':<20} {'Null':<10} {'Key':<10} {'Default':<20} {'Extra':<20}\n")
            f.write("-" * 100 + "\n")
            for col in columns:
                f.write(f"{str(col[0]):<20} {str(col[1]):<20} {str(col[2]):<10} {str(col[3]):<10} {str(col[4]):<20} {str(col[5]):<20}\n")
            
        conn.close()
    except Exception as e:
        with open("schema_info.txt", "w") as f:
            f.write(f"Error: {e}")

if __name__ == "__main__":
    check_schema()
