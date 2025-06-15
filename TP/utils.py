import os
import pyodbc
import pandas as pd


SQL_DIRPATH_ = os.path.abspath(os.path.join(os.path.dirname(__file__), "./sql/"))
assert os.path.isdir(SQL_DIRPATH_), f'El directorio "{SQL_DIRPATH_}" no existe.'

PLOTS_DIRPATH_ = os.path.abspath(os.path.join(os.path.dirname(__file__), "./graficos/"))
assert os.path.isdir(PLOTS_DIRPATH_), f'El directorio "{PLOTS_DIRPATH_}" no existe.'


class SQLConnection:
    # Datos de conexión
    server = "157.92.26.17,1443"  # IP y puerto
    database = "AdventureWorks2019"
    username = "Alumno"
    password = "mrcd2025"

    def __init__(self):
        self.conn = None
        self.create()

    def create(self):
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            f"UID={self.username};"
            f"PWD={self.password};"
        )
        self.conn = pyodbc.connect(conn_str)

    def run_query(self, sql_fn):
        fp = os.path.join(SQL_DIRPATH_, sql_fn)
        assert os.path.isfile(fp), f'El archivo "{fp}" no existe.'
        with open(fp, "r", encoding="utf-8") as f:
            query = f.read()
        return pd.read_sql_query(query, self.conn)

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            print("Conexión cerrada.")
        else:
            print("No hay conexión para cerrar.")
