import  sqlite3
import pandas as pd
try:
    sqliteConnection=sqlite3.connect('D:/Pycharm Projects/ML/Day 2/databases/Chinook_Sqlite.sqlite')
    cursor=sqliteConnection.cursor()
    print('DB Unit')
    query='SELECT * FROM InvoiceLine LIMIT 5;'
    cursor.execute("select * from Customer")
    df=pd.DataFrame(cursor.fetchall())
    print(df)
    cursor.close()
except sqlite3.Error as error:
    print('Error occurred - ',error)

finally:
    if sqliteConnection:
        sqliteConnection.close()
        print('SQLite Connection closed')