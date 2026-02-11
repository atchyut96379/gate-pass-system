import pyodbc

def get_connection():
    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=ATCHYUT;'
        'DATABASE=GatePassDB;'
        'UID=sa;'
        'PWD=Atchyut@2026#;'
    )
