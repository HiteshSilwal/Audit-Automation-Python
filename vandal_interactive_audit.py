"""
Project: Interactive Vandal Inventory Manager
Author: Hitesh Silwal (Junior @ University of Idaho)
Description: A dynamic tool that allows users to input their own 
audit data into a Python-managed SQLite database.
"""

import sqlite3
import pandas as pd

def setup_db():
    conn = sqlite3.connect('interactive_audit.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            item_name TEXT,
            stock_count INTEGER,
            unit_price REAL
        )
    ''')
    conn.commit()
    return conn

def get_user_input(conn):
    print("--- Vandal Inventory Input Portal ---")
    
    # Asking the user for their own values
    name = input("Enter the Item Name: ")
    try:
        count = int(input(f"How many {name} are in stock? "))
        price = float(input(f"What is the unit price for {name}? "))
        
        # Inserting the user's data into the database
        cursor = conn.cursor()
        cursor.execute("INSERT INTO inventory VALUES (?, ?, ?)", (name, count, price))
        conn.commit()
        print(f"\n✓ {name} has been successfully added to the audit database.")
        
    except ValueError:
        print("\n!!! ERROR: Please enter numbers for stock and price.")

def show_audit_report(conn):
    # Using Pandas to show the updated results
    df = pd.read_sql_query("SELECT *, (stock_count * unit_price) AS total_value FROM inventory", conn)
    print("\n--- CURRENT AUDIT REPORT ---")
    if df.empty:
        print("No data found.")
    else:
        print(df)

if __name__ == "__main__":
    connection = setup_db()
    
    # Loop to let the user add multiple items
    while True:
        get_user_input(connection)
        cont = input("\nAdd another item? (yes/no): ").lower()
        if cont != 'yes':
            break
            
    show_audit_report(connection)
    connection.close()
