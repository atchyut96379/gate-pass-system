import pyodbc

server = 'ATCHYUT'        # or your server name
database = 'GatePassDB'
username = 'sa'
password = 'Atchyut@2026#'   # keep it secret

conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
)

print("Connected to SQL Server using SQL Authentication!")

cursor = conn.cursor()
cursor.execute("SELECT UserId, Name, Role FROM Users")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
