import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('db.sqlite3.db')  # Replace with your database file
cursor = conn.cursor()

# Define the table name
table_name = 'notifications.notification'  # Replace with your table name

# Execute the DELETE command
cursor.execute(f'DELETE FROM {table_name};')

# Commit the changes
conn.commit()

# Close the connection
cursor.close()
conn.close()

print(f'All rows deleted from {table_name}.')
