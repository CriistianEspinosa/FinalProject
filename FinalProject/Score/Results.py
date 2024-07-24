import sqlite3

def view_results():
    conn = sqlite3.connect('Score/tic_tac_toe_results.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM results ORDER BY date DESC')
    results = cursor.fetchall()
    
    for row in results:
        print(f"ID: {row[0]}, Result: {row[1]}, Score X: {row[2]}, Score O: {row[3]}, Draws: {row[4]}, Date: {row[5]}")
    
    conn.close()

# Call the function to view results
view_results()