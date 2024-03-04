from http.client import HTTPException
import pyodbc
from Configuration import config

driver = config.DRIVER
server = config.SERVER
database = config.DATABASE
trust = config.TRUST
username = config.UID
password = config.PASSWORD


def connect_to_database():
    try:
        # Local system use it
        conn = pyodbc.connect(f"DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes")

        # production system use it
        # conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')

        return conn
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")
