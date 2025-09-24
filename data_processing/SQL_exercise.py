import sqlite3
import pandas as pd

try:
    sqliteConnection = sqlite3.connect('D:/Pycharm Projects/ML/Day 2/databases/Chinook_Sqlite.sqlite')
    cursor = sqliteConnection.cursor()
    query = """
    SELECT c.*, COUNT(i.InvoiceId) as InvoiceCount
    FROM Customer c
    LEFT JOIN Invoice i ON c.CustomerId = i.CustomerId
    GROUP BY c.CustomerId
    HAVING COUNT(i.InvoiceId) >= ?
    ORDER BY InvoiceCount DESC
    """
    cursor.execute(query, (5,))
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(cursor.fetchall(), columns=columns)


except sqlite3.Error as error:
    print('Error occurred - ', error)

finally:
    if sqliteConnection:
        cursor.close()
        sqliteConnection.close()
        print('SQLite Connection closed')
print(df)
